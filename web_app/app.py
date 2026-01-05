"""
Amazon Audit Tool - Web Application
Multi-user web interface for running ASIN audits
"""
import os
import sys
import uuid
import json
import asyncio
import threading
from datetime import datetime
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs')
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_ASINS = None  # No limit on ASINs
MAX_CONCURRENT_JOBS = 3  # Max simultaneous audits

# Create folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'amazon-audit-secret-key-2024'

# Job tracking
jobs = {}  # {job_id: {status, progress, total, filename, output_file, error, created_at}}
job_lock = threading.Lock()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_asins_from_file(filepath):
    """Read ASINs from uploaded file"""
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        # Find ASIN column
        asin_column = None
        for col in df.columns:
            if 'asin' in col.lower():
                asin_column = col
                break
        
        if asin_column is None:
            asin_column = df.columns[0]
        
        asins = df[asin_column].dropna().astype(str).tolist()
        # Clean ASINs
        asins = [a.strip() for a in asins if a.strip() and len(a.strip()) == 10]
        return asins
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")


def run_audit_job(job_id, asins, output_file):
    """Run the audit job in background - SMOOTH PROGRESS UPDATES"""
    import asyncio
    import random
    import gc
    
    try:
        from playwright.async_api import async_playwright
        from features.entry_point import entry
    except ImportError as e:
        with job_lock:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['error'] = f"Import error: {str(e)}"
        return
    
    # User agents pool
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]
    
    VIEWPORTS = [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1536, 'height': 864},
    ]
    
    async def process_single_asin(asin, output_file, browser, user_agent, queue):
        """Process a single ASIN"""
        # Check if stopped
        with job_lock:
            if jobs[job_id]['status'] == 'stopped':
                return False
        
        try:
            context = await browser.new_context(
                user_agent=user_agent,
                viewport=random.choice(VIEWPORTS),
                locale='en-IN',
                timezone_id='Asia/Kolkata',
            )
            
            page = await context.new_page()
            
            # Anti-detection
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            """)
            
            # Block unnecessary resources for speed
            await page.route("**/*", lambda route: route.abort() 
                if route.request.resource_type in ["image", "stylesheet", "font", "media"] 
                else route.continue_())
            
            url = f"https://www.amazon.in/dp/{asin}"
            await page.goto(url, timeout=20000, wait_until="domcontentloaded")
            
            await entry(page, asin, output_file, "Server")
            
            await context.close()
            return True
            
        except Exception as e:
            print(f"Error {asin}: {str(e)[:30]}")
            try:
                await context.close()
            except:
                pass
            return False
    
    async def worker(browser, queue, user_agents):
        """Worker that processes ASINs from queue one by one"""
        while True:
            try:
                asin = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            
            # Check if stopped
            with job_lock:
                if jobs[job_id]['status'] == 'stopped':
                    break
            
            user_agent = random.choice(user_agents)
            await process_single_asin(asin, output_file, browser, user_agent, queue)
            
            # Update progress immediately after EACH ASIN
            with job_lock:
                jobs[job_id]['progress'] += 1
                jobs[job_id]['status'] = 'running'
    
    async def run_all_asins():
        """Process ASINs using worker pattern for smooth progress"""
        NUM_WORKERS = 10  # 10 parallel workers = smoother updates
        
        total = len(asins)
        
        # Create async queue with all ASINs
        queue = asyncio.Queue()
        for asin in asins:
            await queue.put(asin)
        
        async with async_playwright() as p:
            # Create one browser per worker
            browsers = []
            for _ in range(NUM_WORKERS):
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox',
                        '--disable-gpu',
                        '--disable-images',
                        '--disable-extensions',
                    ]
                )
                browsers.append(browser)
            
            try:
                # Start all workers - each processes one ASIN at a time
                workers = [worker(browsers[i], queue, USER_AGENTS) for i in range(NUM_WORKERS)]
                await asyncio.gather(*workers)
                
            finally:
                # Close all browsers
                for browser in browsers:
                    try:
                        await browser.close()
                    except:
                        pass
            
            gc.collect()
        
        # Mark completed
        with job_lock:
            if jobs[job_id]['status'] != 'stopped':
                jobs[job_id]['status'] = 'completed'
                jobs[job_id]['progress'] = total
    
    try:
        asyncio.run(run_all_asins())
    except Exception as e:
        with job_lock:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['error'] = str(e)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', max_asins=MAX_ASINS)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and start audit job"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use CSV or Excel files.'}), 400
    
    # Check concurrent jobs
    running_jobs = sum(1 for j in jobs.values() if j['status'] == 'running')
    if running_jobs >= MAX_CONCURRENT_JOBS:
        return jsonify({'error': f'Server busy. Maximum {MAX_CONCURRENT_JOBS} concurrent jobs allowed. Please try again later.'}), 429
    
    try:
        # Generate unique job ID
        job_id = str(uuid.uuid4())[:8]
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_filename = f"{job_id}_{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        file.save(filepath)
        
        # Read and validate ASINs
        asins = read_asins_from_file(filepath)
        
        if len(asins) == 0:
            os.remove(filepath)
            return jsonify({'error': 'No valid ASINs found in file'}), 400
        
        # No limit on ASINs - removed check
        
        # Create output file
        output_filename = f"audit_{job_id}_{timestamp}.csv"
        output_file = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Initialize job
        with job_lock:
            jobs[job_id] = {
                'status': 'queued',
                'progress': 0,
                'total': len(asins),
                'filename': filename,
                'output_file': output_file,
                'output_filename': output_filename,
                'error': None,
                'created_at': datetime.now().isoformat(),
                'start_time': datetime.now().timestamp(),
            }
        
        # Start background thread
        thread = threading.Thread(target=run_audit_job, args=(job_id, asins, output_file))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'total_asins': len(asins),
            'message': f'Audit started for {len(asins)} ASINs'
        })
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/status/<job_id>')
def job_status(job_id):
    """Get job status with ETA"""
    with job_lock:
        if job_id not in jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job = jobs[job_id].copy()
    
    # Calculate ETA
    if job['progress'] > 0 and job['status'] == 'running':
        elapsed = datetime.now().timestamp() - job.get('start_time', datetime.now().timestamp())
        rate = job['progress'] / elapsed  # ASINs per second
        remaining = job['total'] - job['progress']
        eta_seconds = remaining / rate if rate > 0 else 0
        job['eta_seconds'] = int(eta_seconds)
        job['elapsed_seconds'] = int(elapsed)
        job['rate_per_minute'] = round(rate * 60, 1)
    else:
        job['eta_seconds'] = 0
        job['elapsed_seconds'] = 0
        job['rate_per_minute'] = 0
    
    return jsonify(job)


@app.route('/stop/<job_id>', methods=['POST'])
def stop_job(job_id):
    """Stop a running job"""
    with job_lock:
        if job_id not in jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job = jobs[job_id]
        
        if job['status'] not in ['running', 'queued']:
            return jsonify({'error': 'Job is not running'}), 400
        
        # Mark job as stopped
        jobs[job_id]['status'] = 'stopped'
        jobs[job_id]['error'] = 'Stopped by user'
    
    return jsonify({
        'success': True,
        'message': 'Job stopped. You can download partial results.',
        'progress': job['progress'],
        'total': job['total']
    })


@app.route('/download/<job_id>')
def download_file(job_id):
    """Download completed or partial audit file"""
    with job_lock:
        if job_id not in jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job = jobs[job_id]
        
        # Allow download for completed, stopped, or error states
        if job['status'] not in ['completed', 'stopped', 'error']:
            return jsonify({'error': 'Job still running. Stop it first to download partial results.'}), 400
        
        output_file = job['output_file']
        output_filename = job['output_filename']
    
    if not os.path.exists(output_file):
        return jsonify({'error': 'Output file not found. No ASINs were processed yet.'}), 404
    
    return send_file(
        output_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name=output_filename
    )


@app.route('/jobs')
def list_jobs():
    """List all jobs (for admin)"""
    with job_lock:
        job_list = [
            {
                'job_id': jid,
                **{k: v for k, v in job.items() if k != 'output_file'}
            }
            for jid, job in jobs.items()
        ]
    
    return jsonify(job_list)


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'active_jobs': sum(1 for j in jobs.values() if j['status'] == 'running'),
        'max_concurrent': MAX_CONCURRENT_JOBS,
        'max_asins': MAX_ASINS
    })


if __name__ == '__main__':
    print("="*60)
    print("🚀 Amazon Audit Tool - Web Server")
    print("="*60)
    print(f"📊 Max ASINs per file: Unlimited")
    print(f"👥 Max concurrent jobs: {MAX_CONCURRENT_JOBS}")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"📁 Output folder: {OUTPUT_FOLDER}")
    print("="*60)
    print("🌐 Starting server on http://localhost:5000")
    print("💡 Use ngrok to expose: ngrok http 5000")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
