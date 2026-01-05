# 🍪 Using Amazon Cookies with Traffic Simulator

## Overview

The traffic simulator now supports using Amazon session cookies. This allows you to:
- ✅ **Skip login prompts** - Bypass the Amazon login requirement
- ✅ **Faster automation** - No need to authenticate during each simulation
- ✅ **Persistent sessions** - Use authenticated Amazon sessions
- ✅ **More realistic behavior** - Browse as an authenticated user

---

## Quick Start

### Step 1: Prepare Cookies File

I've created `amazon_cookies.json` with your cookies. You can also:
- Export cookies from your browser as JSON
- Use the existing `amazon_cookies.json` file

### Step 2: Run with Cookies

```powershell
# Basic usage with Excel file and cookies
"C:/Program Files/Python312/python.exe" run_with_cookies.py -file "C:\Users\dj\Downloads\381.xlsx" -cookies "amazon_cookies.json"

# With limit
"C:/Program Files/Python312/python.exe" run_with_cookies.py -file "C:\Users\dj\Downloads\381.xlsx" -cookies "amazon_cookies.json" -limit 5

# With custom delay
"C:/Program Files/Python312/python.exe" run_with_cookies.py -file "C:\Users\dj\Downloads\381.xlsx" -cookies "amazon_cookies.json" -delay 20

# All options combined
"C:/Program Files/Python312/python.exe" run_with_cookies.py -file "C:\Users\dj\Downloads\381.xlsx" -cookies "amazon_cookies.json" -limit 5 -delay 20
```

---

## Using Cookies Programmatically

### Option 1: From JSON File

```python
import json
from traffic_simulator import run_simulator

# Load cookies from JSON
with open('amazon_cookies.json', 'r') as f:
    data = json.load(f)
    cookies = data['cookies']

# Run simulator with cookies
asins = ["B0DK317TDD", "B0CYPLPZRQ", "B0CW5YN5HX"]
run_simulator(asins, delay=15, cookies=cookies)
```

### Option 2: Direct Cookie List

```python
from traffic_simulator import run_simulator

cookies = [
    {
        "domain": ".amazon.in",
        "name": "session-id",
        "path": "/",
        "value": "520-6228500-5361519",
        "secure": True,
    },
    # ... more cookies
]

run_simulator("B0DK317TDD", cookies=cookies)
```

---

## How to Export Cookies from Browser

### From Chrome/Chromium:

1. Open Amazon.in in your browser
2. Login to your Amazon account
3. Install a cookie export extension (e.g., "EditThisCookie")
4. Click the extension icon
5. Export cookies as JSON
6. Save as `amazon_cookies.json`

### From Firefox:

1. Open Developer Tools (F12)
2. Go to Storage > Cookies > amazon.in
3. Manually copy relevant cookies
4. Format as JSON following the structure in `amazon_cookies.json`

---

## Cookie Requirements

Playwright accepts cookies with these properties:

| Property | Type | Required | Purpose |
|----------|------|----------|---------|
| `name` | string | ✅ Yes | Cookie name |
| `value` | string | ✅ Yes | Cookie value |
| `domain` | string | ✅ Yes | Domain (.amazon.in or www.amazon.in) |
| `path` | string | ✅ Yes | Path (usually "/") |
| `secure` | boolean | No | HTTPS only |
| `httpOnly` | boolean | No | HTTP only |
| `expires` | int | No | Expiration timestamp |
| `sameSite` | string | No | SameSite attribute |

---

## Benefits of Using Cookies

### ✅ Pros:
- Skips Amazon login page
- Faster automation (no authentication needed)
- Can use saved preferences
- More realistic user behavior
- No captcha issues from repeated logins

### ⚠️ Cons:
- Cookies may expire
- Account detection risks if overused
- Requires valid session cookies
- Geographic/device changes may invalidate cookies

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Cookies expired** | Re-export fresh cookies from your browser |
| **Login still appears** | Cookies may be invalid; try new ones |
| **JSON format error** | Validate JSON at jsonlint.com |
| **Cookies not loading** | Check file path is correct and absolute |
| **Access denied errors** | Cookies might be from different Amazon account |

---

## Files Included

- `amazon_cookies.json` - Your Amazon session cookies (pre-filled)
- `run_with_cookies.py` - CLI runner for using cookies
- `traffic_simulator.py` - Core simulator (updated to support cookies)

---

## Example: Full Workflow

```bash
# 1. Navigate to project
cd "f:\audit updated v1\traffic-generator"

# 2. Run with cookies and limit to 3 ASINs
"C:/Program Files/Python312/python.exe" run_with_cookies.py \
  -file "C:\Users\dj\Downloads\381.xlsx" \
  -cookies "amazon_cookies.json" \
  -limit 3 \
  -delay 15

# Browser will open with authenticated Amazon session
# No login prompts
# Faster automation
# More realistic behavior
```

---

## 🎯 Status

✅ **Cookies support integrated**  
✅ **CLI runner created (`run_with_cookies.py`)**  
✅ **Cookie file prepared (`amazon_cookies.json`)**  
✅ **Ready to use!**

---

**Next Step**: Run the command above with your `381.xlsx` file!
