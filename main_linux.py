
# main_linux.py
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
import gc
import os
import json
import random
from playwright.async_api import async_playwright
from utils.read_file import read_file
from features.entry_point import entry
from utils.proxy_manager import get_proxy_manager
import sys

try:
    from playwright_stealth import stealth_async
    HAS_STEALTH = True
except ImportError:
    HAS_STEALTH = False
    print("⚠️ playwright-stealth not installed. Install with: pip install playwright-stealth")

# Pool of real user agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

# ----------------- Config -----------------
MAX_BROWSERS = 30  # 30 parallel browsers with proxy rotation
# ----------------- Helper -----------------
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_chromium_path(playwright):
    """
    Returns the path to Chromium executable:
    - Uses PyInstaller bundled folder if frozen
    - Otherwise, uses Playwright-installed Chromium
    """
    if getattr(sys, "frozen", False):
        # inside the exe, Chromium is copied to 'chromium' folder
        return resource_path(os.path.join("chromium", "chrome"))
    else:
        # Use Playwright's installed Chromium
        return playwright.chromium.executable_path

# ----------------- Cookie Loading -----------------
async def load_cookies(context):
    """Load Amazon cookies into browser context"""
    cookie_file = os.path.join(os.path.dirname(__file__), "cookies", "amazon_cookies.json")
    if os.path.exists(cookie_file):
        try:
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
                await context.add_cookies(cookies)
                print("🍪 Cookies loaded")
        except Exception as e:
            print(f"⚠️ Cookie error: {e}")

# ----------------- Async browser task -----------------
async def run_browser_async(asin, output_file):
    import time
    start_time = time.time()
    
    # Random delay to simulate human behavior (2-5 seconds)
    await asyncio.sleep(random.uniform(2, 5))
    
    # Proxy disabled - running without proxy
    proxy_config = None
    proxy_ip = "No Proxy"
    
    # Random user agent
    user_agent = random.choice(USER_AGENTS)
    
    try:
        async with async_playwright() as p:
            # Launch browser with aggressive anti-detection
            launch_args = {
                'headless': False,  # REAL BROWSER MODE - visible Chrome
                'args': [
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--disable-images',
                    '--blink-settings=imagesEnabled=false',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--disable-site-isolation-trials',
                    '--disable-web-security',
                    '--flag-switches-begin --disable-site-isolation-trials --flag-switches-end',
                    '--user-agent=' + user_agent,
                ]
            }
            
            browser = await p.chromium.launch(**launch_args)
            
            # Randomized viewport sizes
            viewports = [
                {'width': 1920, 'height': 1080},
                {'width': 1366, 'height': 768},
                {'width': 1536, 'height': 864},
                {'width': 1440, 'height': 900},
                {'width': 1600, 'height': 900},
            ]
            
            # Create context with proxy if available
            context_args = {
                'user_agent': user_agent,
                'viewport': random.choice(viewports),
                'java_script_enabled': True,
                'locale': 'en-IN',
                'timezone_id': 'Asia/Kolkata',
            }
            
            if proxy_config:
                # Build proxy config for Playwright
                playwright_proxy = {'server': proxy_config['server']}
                
                if proxy_config.get('username') and proxy_config.get('password'):
                    playwright_proxy['username'] = proxy_config['username']
                    playwright_proxy['password'] = proxy_config['password']
                
                context_args['proxy'] = playwright_proxy
                
                # Extract IP:port for display
                server = proxy_config['server']
                if '@' in server:
                    display_proxy = server.split('@')[1]
                else:
                    display_proxy = server.replace('http://', '')
                print(f"🌐 Proxy: {display_proxy}")
            
            context = await browser.new_context(**context_args)
            
            # Cookie loading disabled - using proxy-only approach
            # await load_cookies(context)
            
            await context.set_extra_http_headers({
                'Accept-Language': 'en-US,en-IN;q=0.9,en;q=0.8',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
            })
            
            page = await context.new_page()
            
            # Apply playwright-stealth if available
            if HAS_STEALTH:
                await stealth_async(page)
            
            # Inject advanced anti-detection scripts
            await page.add_init_script("""
                // Remove webdriver property
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                
                // Mock plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {name: 'Chrome PDF Plugin', description: 'Portable Document Format', filename: 'internal-pdf-viewer'},
                        {name: 'Chrome PDF Viewer', description: '', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                        {name: 'Native Client', description: '', filename: 'internal-nacl-plugin'}
                    ]
                });
                
                // Set proper languages
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en-IN', 'en']});
                
                // Add chrome object
                window.chrome = {runtime: {}, loadTimes: function(){}, csi: function(){}};
                
                // Mock permissions
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
                
                // Randomize canvas fingerprint
                const getImageData = CanvasRenderingContext2D.prototype.getImageData;
                CanvasRenderingContext2D.prototype.getImageData = function() {
                    const imageData = getImageData.apply(this, arguments);
                    for (let i = 0; i < imageData.data.length; i++) {
                        imageData.data[i] = imageData.data[i] ^ Math.floor(Math.random() * 2);
                    }
                    return imageData;
                };
            """)
            
            # Block unnecessary resources for speed
            await page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "stylesheet", "font", "media"] else route.continue_())
            
            url = f"https://www.amazon.in/kuber/dp/{asin}"
            await page.goto(url, timeout=20_000, wait_until="domcontentloaded")

            await entry(page, asin, output_file, proxy_ip)
            await context.close()
            await browser.close()
            gc.collect()
        
        elapsed_time = time.time() - start_time
        print(f"✅ {asin} | {elapsed_time:.1f}s | IP: {proxy_ip}")
    except asyncio.TimeoutError:
        elapsed_time = time.time() - start_time
        print(f"⏱️ {asin} | {elapsed_time:.1f}s | Timeout | IP: {proxy_ip}")
        # Still save with timeout status
        try:
            await entry(page, asin, output_file, proxy_ip)
        except:
            pass
        gc.collect()
    except Exception as e:
        elapsed_time = time.time() - start_time
        error_msg = str(e)[:50]  # Truncate error message
        print(f"❌ {asin} | {elapsed_time:.1f}s | {error_msg} | IP: {proxy_ip}")
        gc.collect()

# ----------------- Multiprocessing wrapper -----------------
import os
import tempfile

# Global variables for progress tracking and proxy config
_progress_file = None
_batch_start_time = None
_total_asins = None
_primary_proxy_file = None
_backup_proxy_file = None

def init_worker(progress_file, batch_start_time, total_asins, primary_proxy_file, backup_proxy_file):
    """Initialize worker process with shared progress file and proxy files"""
    global _progress_file, _batch_start_time, _total_asins, _primary_proxy_file, _backup_proxy_file
    _progress_file = progress_file
    _batch_start_time = batch_start_time
    _total_asins = total_asins
    _primary_proxy_file = primary_proxy_file
    _backup_proxy_file = backup_proxy_file
    
    # Load proxies in this worker process
    proxy_manager = get_proxy_manager()
    if primary_proxy_file:
        proxy_manager.load_proxies_from_file(primary_proxy_file)
    if backup_proxy_file:
        proxy_manager.load_backup_proxies(backup_proxy_file)

def run_browser(asin_output_tuple):
    """
    Multiprocessing wrapper. Each child gets a clean sys.argv.
    """
    global _progress_file, _batch_start_time, _total_asins
    
    asin, output_file, start_idx, total_in_batch = asin_output_tuple

    # Clear sys.argv so Playwright doesn't pick up CLI args
    sys.argv = [sys.argv[0]]

    asyncio.run(run_browser_async(asin, output_file))
    
    # Update counter using file-based approach (cross-process safe on Windows)
    if _progress_file and os.path.exists(_progress_file):
        try:
            import time as time_module
            # Try to read and update the counter with retry logic
            for attempt in range(10):
                try:
                    # Read current count
                    with open(_progress_file, 'r') as f:
                        completed = int(f.read().strip() or '0')
                    
                    completed += 1
                    
                    # Write updated count
                    with open(_progress_file, 'w') as f:
                        f.write(str(completed))
                    
                    # Show progress every 50 ASINs
                    if completed % 50 == 0 or completed == total_in_batch:
                        elapsed_time = time_module.time() - _batch_start_time
                        remaining = total_in_batch - completed
                        avg_time_per_asin = elapsed_time / completed if completed > 0 else 0
                        eta_seconds = remaining * avg_time_per_asin
                        eta_minutes = eta_seconds / 60
                        
                        overall_progress = start_idx + completed
                        
                        print(f"\n{'='*70}")
                        print(f"📊 PROGRESS UPDATE")
                        print(f"{'='*70}")
                        print(f"✅ Completed in this batch: {completed}/{total_in_batch}")
                        print(f"⏳ Pending in this batch: {remaining}")
                        print(f"📈 Overall ASINs processed: {overall_progress}/{_total_asins}")
                        print(f"⏱️  Average time per ASIN: {avg_time_per_asin:.1f}s")
                        print(f"🕐 ETA for this batch: {eta_minutes:.1f} minutes")
                        print(f"{'='*70}\n")
                    break
                except Exception as e:
                    if attempt < 9:
                        time_module.sleep(0.05)
                    continue
        except:
            pass

