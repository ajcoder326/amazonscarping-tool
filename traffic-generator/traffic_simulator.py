"""
Amazon Traffic Simulator - Simulates real user behavior
Clicks Buy Now button and interacts like a human
"""
import asyncio
import random
import sys
import os
from playwright.async_api import async_playwright

# Add parent directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from playwright_stealth import stealth_async
    HAS_STEALTH = True
except ImportError:
    HAS_STEALTH = False

# User agents pool
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

VIEWPORTS = [
    {'width': 1920, 'height': 1080},
    {'width': 1366, 'height': 768},
    {'width': 1536, 'height': 864},
    {'width': 1440, 'height': 900},
]

async def simulate_human_mouse_movement(page):
    """Simulate random mouse movements like a human"""
    for _ in range(random.randint(3, 6)):
        x = random.randint(100, 1200)
        y = random.randint(100, 800)
        await page.mouse.move(x, y, steps=random.randint(10, 30))
        await asyncio.sleep(random.uniform(0.1, 0.5))

async def simulate_scrolling(page):
    """Simulate human-like scrolling behavior"""
    # Scroll down in chunks like a human reading
    scroll_positions = [300, 600, 900, 1200, 1500]
    random.shuffle(scroll_positions)
    
    for position in scroll_positions[:random.randint(2, 4)]:
        await page.evaluate(f"window.scrollTo(0, {position})")
        await asyncio.sleep(random.uniform(0.8, 2.5))
        
        # Random mouse movements while scrolling
        if random.random() > 0.5:
            await simulate_human_mouse_movement(page)
    
    # Scroll back to top occasionally
    if random.random() > 0.6:
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(random.uniform(0.5, 1.5))

async def visit_product_and_interact(asin, cookies=None):
    """
    Visit product page and simulate real user behavior including Buy Now click
    
    Args:
        asin: Product ASIN to visit
        cookies: List of cookies to use (optional)
    """
    user_agent = random.choice(USER_AGENTS)
    viewport = random.choice(VIEWPORTS)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Visible browser for traffic simulation
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-extensions',  # Disable extensions for cleaner view
                '--disable-plugins',     # Disable plugins
                '--disable-images',      # Optional: faster loading
                '--disable-component-extensions-with-background-pages',
            ],
            slow_mo=50,  # Slow down actions by 50ms for visibility
        )
        
        context = await browser.new_context(
            user_agent=user_agent,
            viewport=viewport,
            locale='en-IN',
            timezone_id='Asia/Kolkata',
            ignore_https_errors=True,  # Better compatibility
        )
        
        # Add cookies if provided
        if cookies:
            # Fix cookie format for Playwright
            fixed_cookies = []
            for cookie in cookies:
                # Fix sameSite value
                if 'sameSite' in cookie:
                    same_site = cookie.get('sameSite', 'None')
                    if same_site == 'unspecified' or same_site not in ['Strict', 'Lax', 'None']:
                        cookie['sameSite'] = 'None'
                else:
                    cookie['sameSite'] = 'None'
                
                # Remove invalid fields for Playwright
                for key in ['hostOnly', 'storeId', 'session']:
                    cookie.pop(key, None)
                
                fixed_cookies.append(cookie)
            
            await context.add_cookies(fixed_cookies)
            print(f"🍪 Cookies loaded: {len(fixed_cookies)} cookies added")
        
        page = await context.new_page()
        
        # Apply stealth
        if HAS_STEALTH:
            await stealth_async(page)
        
        # Anti-detection scripts
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-IN', 'en-US', 'en']});
            window.chrome = {runtime: {}};
        """)
        
        try:
            print(f"\n{'='*70}")
            print(f"🎯 Simulating user visit for ASIN: {asin}")
            print(f"{'='*70}")
            
            # Step 1: Visit Amazon homepage first (30% chance)
            if random.random() < 0.3:
                print("📱 Step 1: Visiting Amazon homepage...")
                await page.goto("https://www.amazon.in/", wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(random.uniform(2, 4))
                await simulate_scrolling(page)
                print("✅ Homepage visited")
            
            # Step 2: Go to product page
            print(f"📦 Step 2: Opening product page...")
            url = f"https://www.amazon.in/dp/{asin}"
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(random.uniform(2, 4))
            print(f"✅ Product page loaded: {url}")
            
            # Step 3: Random mouse movements (simulate reading)
            print("🖱️  Step 3: Simulating mouse movements...")
            await simulate_human_mouse_movement(page)
            await asyncio.sleep(random.uniform(1, 2))
            
            # Step 4: Scroll and read product details
            print("📜 Step 4: Scrolling through product details...")
            await simulate_scrolling(page)
            await asyncio.sleep(random.uniform(1, 3))
            
            # Step 5: View product images (hover over thumbnails)
            print("🖼️  Step 5: Viewing product images...")
            try:
                image_thumbnails = await page.query_selector_all('img[src*="images-amazon"]')
                if image_thumbnails and len(image_thumbnails) > 1:
                    for i in range(min(3, len(image_thumbnails))):
                        img = image_thumbnails[random.randint(0, len(image_thumbnails)-1)]
                        await img.hover()
                        await asyncio.sleep(random.uniform(0.5, 1.5))
            except:
                pass
            
            # Step 6: Check product details sections
            print("📋 Step 6: Reading product information...")
            sections_to_check = ['#feature-bullets', '#productDescription', '#productDetails_feature_div']
            for selector in sections_to_check:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        await element.scroll_into_view_if_needed()
                        await asyncio.sleep(random.uniform(1, 2.5))
                        # Random mouse movement near the element
                        box = await element.bounding_box()
                        if box:
                            await page.mouse.move(box['x'] + random.randint(10, 100), 
                                                 box['y'] + random.randint(10, 50))
                            await asyncio.sleep(random.uniform(0.3, 0.8))
                except:
                    pass
            
            # Step 7: Click Buy Now button
            print("🛒 Step 7: Looking for Buy Now button...")
            buy_now_selectors = [
                '#buy-now-button',
                'input[name="submit.buy-now"]',
                'input#buy-now-button',
                '#buyNow',
                '[data-feature-name="buyNow"]',
            ]
            
            buy_now_clicked = False
            for selector in buy_now_selectors:
                try:
                    buy_button = await page.query_selector(selector)
                    if buy_button and await buy_button.is_visible():
                        # Scroll to button
                        await buy_button.scroll_into_view_if_needed()
                        await asyncio.sleep(random.uniform(0.5, 1.5))
                        
                        # Hover before click (human-like)
                        await buy_button.hover()
                        await asyncio.sleep(random.uniform(0.3, 0.8))
                        
                        # Click Buy Now
                        print(f"✅ Clicking Buy Now button...")
                        await buy_button.click()
                        buy_now_clicked = True
                        
                        # Wait for page navigation/login prompt
                        await asyncio.sleep(random.uniform(2, 4))
                        
                        print(f"✅ Buy Now clicked! Current URL: {page.url}")
                        break
                except Exception as e:
                    continue
            
            if not buy_now_clicked:
                print("⚠️  Buy Now button not found - checking Add to Cart...")
                # Try Add to Cart as fallback
                cart_selectors = [
                    '#add-to-cart-button',
                    'input[name="submit.add-to-cart"]',
                    '#add-to-cart',
                ]
                
                for selector in cart_selectors:
                    try:
                        cart_button = await page.query_selector(selector)
                        if cart_button and await cart_button.is_visible():
                            await cart_button.scroll_into_view_if_needed()
                            await asyncio.sleep(random.uniform(0.5, 1))
                            await cart_button.hover()
                            await asyncio.sleep(random.uniform(0.3, 0.7))
                            await cart_button.click()
                            print(f"✅ Add to Cart clicked!")
                            await asyncio.sleep(random.uniform(2, 3))
                            break
                    except:
                        continue
            
            # Step 8: Stay on page for a bit longer (realistic)
            print("⏱️  Step 8: Staying on page for realistic timing...")
            await asyncio.sleep(random.uniform(3, 6))
            
            # Step 9: Random final actions
            if random.random() > 0.5:
                print("🔄 Step 9: Additional browsing...")
                await simulate_scrolling(page)
                await asyncio.sleep(random.uniform(1, 2))
            
            print(f"\n{'='*70}")
            print(f"✅ Traffic simulation completed for {asin}")
            print(f"⏱️  Total session time: ~{random.randint(15, 30)} seconds")
            print(f"{'='*70}\n")
            
        except Exception as e:
            print(f"❌ Error during simulation: {str(e)[:100]}")
        
        finally:
            await asyncio.sleep(2)  # Keep window open briefly
            await browser.close()

async def simulate_traffic_for_asins(asin_list, delay_between=None, cookies=None):
    """
    Run traffic simulation for a list of ASINs
    
    Args:
        asin_list: List of ASINs to visit
        delay_between: Delay between each ASIN visit (default: random 10-30s)
        cookies: List of cookies to use for authentication (optional)
    """
    print(f"\n{'#'*70}")
    print(f"🚀 AMAZON TRAFFIC SIMULATOR - STARTING")
    print(f"{'#'*70}")
    print(f"📊 Total ASINs to simulate: {len(asin_list)}")
    print(f"🕐 Estimated time: ~{len(asin_list) * 25 / 60:.1f} minutes")
    if cookies:
        print(f"🍪 Using {len(cookies)} cookies for authentication")
    print(f"{'#'*70}\n")
    
    for idx, asin in enumerate(asin_list, 1):
        print(f"\n[{idx}/{len(asin_list)}] Processing ASIN: {asin}")
        
        await visit_product_and_interact(asin, cookies=cookies)
        
        # Delay before next ASIN
        if idx < len(asin_list):
            if delay_between is None:
                wait_time = random.uniform(10, 30)
            else:
                wait_time = delay_between
            
            print(f"⏸️  Waiting {wait_time:.1f}s before next ASIN...\n")
            await asyncio.sleep(wait_time)
    
    print(f"\n{'#'*70}")
    print(f"✅ ALL TRAFFIC SIMULATIONS COMPLETED!")
    print(f"{'#'*70}\n")

def run_simulator(asins, delay=None, cookies=None):
    """
    Run the traffic simulator
    
    Args:
        asins: List of ASINs or single ASIN string
        delay: Delay between ASINs in seconds (default: random 10-30s)
        cookies: List of cookies for authentication (optional)
    """
    if isinstance(asins, str):
        asins = [asins]
    
    asyncio.run(simulate_traffic_for_asins(asins, delay, cookies))

if __name__ == "__main__":
    # Example usage
    test_asins = [
        "B0DK317TDD",
        "B0CYPLPZRQ",
        "B0CW5YN5HX",
    ]
    
    print("="*70)
    print("Amazon Traffic Simulator")
    print("="*70)
    print("This tool simulates real user behavior on Amazon product pages")
    print("Including: scrolling, mouse movements, and Buy Now clicks")
    print("="*70)
    
    run_simulator(test_asins, delay=15)
