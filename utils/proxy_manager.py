"""
Proxy manager with support for custom proxy files
Supports both authenticated (ip:port:user:pass) and non-authenticated (ip:port) proxies
"""
import random
import os

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.backup_proxies = []
        self.proxy_file = None
        self.backup_file = None
        
    def load_proxies_from_file(self, filepath):
        """Load proxies from a file in format: ip:port:username:password or ip:port"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                
                proxies = []
                for line in lines:
                    line = line.strip()
                    if line and ':' in line:
                        parts = line.split(':')
                        if len(parts) == 4:
                            # Authenticated proxy: ip:port:username:password
                            ip, port, username, password = parts
                            proxy_url = f"http://{username}:{password}@{ip}:{port}"
                            proxies.append({
                                'server': proxy_url,
                                'username': username,
                                'password': password
                            })
                        elif len(parts) == 2:
                            # Non-authenticated proxy: ip:port
                            ip, port = parts
                            proxy_url = f"http://{ip}:{port}"
                            proxies.append({
                                'server': proxy_url,
                                'username': None,
                                'password': None
                            })
                
                if proxies:
                    self.proxies = proxies
                    self.proxy_file = filepath
                    print(f"✅ Loaded {len(proxies)} proxies from {os.path.basename(filepath)}")
                    return True
                else:
                    print(f"⚠️ No valid proxies found in {filepath}")
                    return False
            else:
                print(f"⚠️ Proxy file not found: {filepath}")
                return False
                
        except Exception as e:
            print(f"⚠️ Error loading proxies: {e}")
            return False
    
    def load_backup_proxies(self, filepath):
        """Load backup proxies from file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                
                proxies = []
                for line in lines:
                    line = line.strip()
                    if line and ':' in line:
                        parts = line.split(':')
                        if len(parts) == 4:
                            ip, port, username, password = parts
                            proxy_url = f"http://{username}:{password}@{ip}:{port}"
                            proxies.append({
                                'server': proxy_url,
                                'username': username,
                                'password': password
                            })
                        elif len(parts) == 2:
                            ip, port = parts
                            proxy_url = f"http://{ip}:{port}"
                            proxies.append({
                                'server': proxy_url,
                                'username': None,
                                'password': None
                            })
                
                if proxies:
                    self.backup_proxies = proxies
                    self.backup_file = filepath
                    print(f"✅ Loaded {len(proxies)} backup proxies from {os.path.basename(filepath)}")
                    return True
                else:
                    print(f"⚠️ No valid backup proxies found in {filepath}")
                    return False
            else:
                print(f"⚠️ Backup proxy file not found: {filepath}")
                return False
                
        except Exception as e:
            print(f"⚠️ Error loading backup proxies: {e}")
            return False
    
    def get_proxy_for_playwright(self):
        """Get proxy in Playwright format, prioritizing primary proxies"""
        # Prioritize primary (Webshare) proxies, use backup as fallback
        proxy_pool = self.proxies if self.proxies else self.backup_proxies
        
        if proxy_pool:
            proxy_data = random.choice(proxy_pool)
            result = {'server': proxy_data['server']}
            
            # Add authentication if available
            if proxy_data['username'] and proxy_data['password']:
                result['username'] = proxy_data['username']
                result['password'] = proxy_data['password']
            
            return result
        return None

# Global proxy manager instance
_proxy_manager = None

def get_proxy_manager():
    """Get or create global proxy manager"""
    global _proxy_manager
    if _proxy_manager is None:
        _proxy_manager = ProxyManager()
    return _proxy_manager
