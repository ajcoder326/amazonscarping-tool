# runner_linux.py

import sys
import os
from datetime import datetime

# ----------------- Multiprocessing spawn -----------------
from multiprocessing import set_start_method
try:
    set_start_method("spawn")
except RuntimeError:
    pass

# ----------------- Detect main process -----------------
def is_main_process():
    """
    Returns True if this is the main user process.
    Skip internal multiprocessing children (resource_tracker, forked processes).
    """
    # Multiprocessing children add --multiprocessing-fork or resource_tracker flags
    return not any(
        arg.startswith("--multiprocessing") or "resource_tracker" in arg
        for arg in sys.argv
    )

# ----------------- Import your modules -----------------
if is_main_process():
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from main_linux import run_browser, read_file, MAX_BROWSERS
    from multiprocessing import Manager, Value
else:
    # In children, imports that don't need CLI args
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from main_linux import run_browser, MAX_BROWSERS

# ----------------- Main function -----------------
def main():
    if not is_main_process():
        return  # Skip argument parsing in child processes

    import argparse
    import time

    parser = argparse.ArgumentParser(description="Run Amazon Scraper")
    parser.add_argument("-file", type=str, required=True, help="Path to input Excel/CSV file")
    parser.add_argument("-limit", type=int, default=None, help="Limit number of ASINs to process (for testing)")
    parser.add_argument("-batch", type=int, default=1000, help="Batch size (default: 1000)")
    parser.add_argument("-wait", type=int, default=60, help="Wait time between batches in seconds (default: 60)")
    args = parser.parse_args()

    input_file = args.file
    if not os.path.isabs(input_file):
        input_file = os.path.abspath(input_file)

    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)

    # ----------------- Read ASINs -----------------
    file_name, asin_list = read_file(input_file)

    # Limit ASINs if specified
    if args.limit:
        asin_list = asin_list[:args.limit]
        print(f"🔹 TESTING MODE: Limited to {args.limit} ASINs")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_FILE = os.path.expanduser(f'~/Documents/Audited_files/{file_name}_{timestamp}.csv')

    total_asins = len(asin_list)
    batch_size = args.batch
    wait_time = args.wait
    total_batches = (total_asins + batch_size - 1) // batch_size
    
    print(f"\n{'='*70}")
    print(f"🚀 AMAZON AUDIT - BATCH MODE")
    print(f"{'='*70}")
    print(f"📊 Total ASINs to process: {total_asins}")
    print(f"📦 Batch size: {batch_size}")
    print(f"🔢 Total batches: {total_batches}")
    print(f"🔧 Parallel browsers: {MAX_BROWSERS}")
    print(f"⏱️  Wait between batches: {wait_time // 60} minutes")
    print(f"🍪 Cookies: Enabled")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")

    # Initialize proxy manager with primary and backup proxy files
    print("🌐 Loading proxies...")
    from utils.proxy_manager import get_proxy_manager
    proxy_manager = get_proxy_manager()
    
    # Load only Proxyscrape proxies
    proxyscrape_file = r"C:\Users\dj\Downloads\proxyscrape_premium_http_proxies.txt"
    proxy_manager.load_proxies_from_file(proxyscrape_file)
    
    total_proxies = len(proxy_manager.proxies)
    print(f"🔄 Total proxy pool: {total_proxies} Proxyscrape proxies")
    print()

    # Start timing
    overall_start_time = time.time()
    
    # Create temp file for progress tracking
    import tempfile
    progress_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    progress_file.write('0')
    progress_file.close()
    progress_file_path = progress_file.name
    
    # Process in batches
    for batch_num in range(total_batches):
        batch_start_time = time.time()
        
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_asins)
        batch_asins = asin_list[start_idx:end_idx]
        
        print(f"\n{'='*70}")
        print(f"🎯 BATCH {batch_num + 1}/{total_batches}")
        print(f"{'='*70}")
        print(f"📍 Processing ASINs: {start_idx + 1} to {end_idx} ({len(batch_asins)} ASINs)")
        print(f"⏰ Batch start: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*70}\n")
        
        # Reset progress counter for this batch
        with open(progress_file_path, 'w') as f:
            f.write('0')
        
        batch_start_time = time.time()
        
        items = [(str(a), OUTPUT_FILE, start_idx, len(batch_asins)) for a in batch_asins]
        
        # Proxy file path (only Proxyscrape)
        proxyscrape_file = r"C:\Users\dj\Downloads\proxyscrape_premium_http_proxies.txt"
        
        # ----------------- Multiprocessing -----------------
        from multiprocessing import Pool
        from main_linux import init_worker
        with Pool(processes=MAX_BROWSERS, initializer=init_worker, initargs=(progress_file_path, batch_start_time, total_asins, proxyscrape_file, None)) as pool:
            pool.map(run_browser, items)
        
        batch_elapsed = time.time() - batch_start_time
        batch_rate = len(batch_asins) / batch_elapsed * 3600 if batch_elapsed > 0 else 0
        
        print(f"\n{'='*70}")
        print(f"✅ BATCH {batch_num + 1}/{total_batches} COMPLETED!")
        print(f"{'='*70}")
        print(f"⏱️  Batch time: {batch_elapsed // 60:.0f}m {batch_elapsed % 60:.0f}s")
        print(f"📈 Batch rate: {batch_rate:.0f} ASINs/hour")
        print(f"📊 Progress: {end_idx}/{total_asins} ({end_idx/total_asins*100:.1f}%)")
        print(f"{'='*70}\n")
        
        # Wait before next batch (except for last batch)
        if batch_num < total_batches - 1:
            next_start = end_idx + 1
            next_end = min(end_idx + batch_size, total_asins)
            
            print(f"⏸️  COOLDOWN PERIOD")
            print(f"{'='*70}")
            print(f"⏳ Waiting {wait_time // 60} minutes before next batch...")
            print(f"🔜 Next: Batch {batch_num + 2}/{total_batches} (ASINs {next_start}-{next_end})")
            print(f"💤 Cooling down to avoid rate limiting...")
            
            # Show countdown
            for remaining in range(wait_time, 0, -60):
                mins = remaining // 60
                print(f"   ⏱️  {mins} minutes remaining...")
                time.sleep(60)
            
            print(f"{'='*70}\n")

    # End timing
    end_time = time.time()
    total_time = end_time - overall_start_time
    
    # Calculate statistics
    print("\n" + "=" * 70)
    print(f"🎉 ALL BATCHES COMPLETED!")
    print("=" * 70)
    print(f"⏰ End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Statistics:")
    print(f"   • Total ASINs processed: {total_asins}")
    print(f"   • Total batches: {total_batches}")
    print(f"   • Total time: {total_time // 3600:.0f}h {(total_time % 3600) // 60:.0f}m {total_time % 60:.0f}s")
    print(f"   • Average time per ASIN: {total_time/total_asins:.2f} seconds")
    print(f"   • Overall rate: {total_asins/(total_time/3600):.0f} ASINs/hour")
    print(f"   • Parallel browsers: {MAX_BROWSERS}")
    print(f"   • Output file: {OUTPUT_FILE}")
    print("=" * 70)
    
    # Cleanup progress file
    try:
        os.remove(progress_file_path)
    except:
        pass

# ----------------- Entry -----------------
if __name__ == "__main__":
    main()
