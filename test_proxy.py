"""
Test script to verify proxies are working correctly
"""
import asyncio
from playwright.async_api import async_playwright
from utils.proxy_manager import get_proxy_manager

async def test_proxy():
    """Test if proxy is actually being used"""
    proxy_manager = get_proxy_manager()
    
    # Load proxies
    primary = r"C:\Users\dj\Downloads\Webshare 10 proxies.txt"
    backup = r"C:\Users\dj\Downloads\proxyscrape_premium_http_proxies.txt"
    
    proxy_manager.load_proxies_from_file(primary)
    proxy_manager.load_backup_proxies(backup)
    
    print(f"\n{'='*70}")
    print("🧪 Testing Proxy Connection")
    print(f"{'='*70}\n")
    
    # Test without proxy
    print("📍 Test 1: Without Proxy")
    print("-" * 70)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            await page.goto("https://api.ipify.org?format=json", timeout=15000)
            content = await page.content()
            print(f"Your actual IP: {content}")
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()
    
    print()
    
    # Test with proxy
    print("📍 Test 2: With Proxy")
    print("-" * 70)
    proxy_config = proxy_manager.get_proxy_for_playwright()
    
    if proxy_config:
        print(f"Using proxy: {proxy_config['server']}")
        print()
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # Build context with proxy
            context_args = {'proxy': {'server': proxy_config['server']}}
            
            if proxy_config.get('username') and proxy_config.get('password'):
                context_args['proxy']['username'] = proxy_config['username']
                context_args['proxy']['password'] = proxy_config['password']
            
            context = await browser.new_context(**context_args)
            page = await context.new_page()
            
            try:
                await page.goto("https://api.ipify.org?format=json", timeout=15000)
                content = await page.content()
                print(f"Proxy IP showing: {content}")
                
                # Extract IP from server string
                server = proxy_config['server']
                if '@' in server:
                    proxy_ip = server.split('@')[1].split(':')[0]
                else:
                    proxy_ip = server.replace('http://', '').split(':')[0]
                
                if proxy_ip in content:
                    print(f"✅ SUCCESS! Proxy is working correctly")
                else:
                    print(f"⚠️  WARNING: Proxy IP ({proxy_ip}) not detected in response")
                
            except Exception as e:
                print(f"❌ Error: {e}")
            
            await browser.close()
    else:
        print("❌ No proxy available")
    
    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    asyncio.run(test_proxy())
