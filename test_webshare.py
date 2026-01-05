from utils.proxy_manager import get_proxy_manager

pm = get_proxy_manager()
pm.load_proxies_from_file(r'C:\Users\dj\Downloads\Webshare 10 proxies.txt')
pm.load_backup_proxies(r'C:\Users\dj\Downloads\proxyscrape_premium_http_proxies.txt')

print("\nTesting 10 random proxy selections:")
print("="*70)
for i in range(10):
    p = pm.get_proxy_for_playwright()
    has_auth = 'username' in p and p['username']
    proxy_type = "Webshare (auth)" if has_auth else "Proxyscrape (no auth)"
    print(f"Test {i+1}: {proxy_type} | {p['server'][:60]}")
