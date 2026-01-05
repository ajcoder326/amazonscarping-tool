"""
Quick test script to verify cookies are loaded correctly and check expiration
"""
import os
import json
from datetime import datetime

cookie_file = "cookies/amazon_cookies.json"

print("="*60)
print("🧪 Cookie Configuration Test")
print("="*60)

if os.path.exists(cookie_file):
    print(f"✅ Cookie file found: {cookie_file}")
    
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    
    print(f"✅ Total cookies: {len(cookies)}")
    
    # Check for expired cookies
    import time
    current_time = time.time()
    expired_count = 0
    valid_count = 0
    
    print("\n📋 Cookie Expiration Status:")
    print("-" * 70)
    print(f"{'Cookie Name':<25} {'Domain':<25} {'Expires':<20}")
    print("-" * 70)
    
    for cookie in cookies:
        name = cookie.get('name', 'Unknown')
        domain = cookie.get('domain', 'Unknown')
        expires = cookie.get('expirationDate', cookie.get('expires', 0))
        
        # Check if cookie is expired
        if expires and expires > 0:
            is_expired = expires < current_time
            if is_expired:
                expired_count += 1
                status = "❌ EXPIRED"
                expiry_date = datetime.fromtimestamp(expires).strftime('%Y-%m-%d %H:%M')
            else:
                valid_count += 1
                status = "✅ Valid"
                expiry_date = datetime.fromtimestamp(expires).strftime('%Y-%m-%d %H:%M')
        else:
            valid_count += 1
            status = "✅ Session"
            expiry_date = "Session cookie"
        
        print(f"{name:<25} {domain:<25} {status}")
        print(f"{'':25} {'':25} {expiry_date}")
    
    print("-" * 70)
    print(f"\n📊 Summary:")
    print(f"  ✅ Valid cookies: {valid_count}")
    print(f"  ❌ Expired cookies: {expired_count}")
    
    # Check critical cookies
    critical_cookies = ['session-id', 'session-token', 'at-acbin', 'ubid-acbin']
    print("\n🔑 Critical Cookies Status:")
    print("-" * 70)
    
    cookie_dict = {c.get('name'): c for c in cookies}
    all_critical_valid = True
    
    for cname in critical_cookies:
        if cname in cookie_dict:
            cookie = cookie_dict[cname]
            expires = cookie.get('expirationDate', cookie.get('expires', 0))
            
            if expires and expires > 0:
                is_expired = expires < current_time
                if is_expired:
                    expiry_str = datetime.fromtimestamp(expires).strftime('%Y-%m-%d')
                    print(f"  ❌ {cname} - EXPIRED on {expiry_str}")
                    all_critical_valid = False
                else:
                    days_left = int((expires - current_time) / 86400)
                    print(f"  ✅ {cname} - Valid ({days_left} days remaining)")
            else:
                print(f"  ✅ {cname} - Session cookie")
        else:
            print(f"  ❌ {cname} - MISSING!")
            all_critical_valid = False
    
    print("\n" + "="*70)
    if expired_count > 0:
        print("⚠️  WARNING: Some cookies have expired!")
        print("   Please update your cookies from a fresh Amazon login session")
    elif not all_critical_valid:
        print("⚠️  WARNING: Some critical cookies are missing or expired!")
        print("   Please export fresh cookies from Amazon.in")
    else:
        print("✅ All cookies are valid and ready to use!")
    print("="*70)
    
else:
    print(f"❌ Cookie file NOT found: {cookie_file}")
    print("Please create cookies/amazon_cookies.json with your Amazon cookies")
    print("="*70)
