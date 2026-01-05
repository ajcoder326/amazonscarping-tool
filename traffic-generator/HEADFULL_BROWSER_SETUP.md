# 🌐 Headfull Browser Configuration

## What Changed

The traffic simulator has been optimized for **headfull (visible) browser mode** with enhanced visibility settings.

### Browser Launch Configuration

```python
browser = await p.chromium.launch(
    headless=False,                    # ✅ Visible browser window
    args=[
        '--disable-blink-features=AutomationControlled',
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-extensions',        # ✅ Clean interface (no extensions)
        '--disable-plugins',           # ✅ No plugin clutter
        '--disable-images',            # ✅ Faster loading (optional)
        '--disable-component-extensions-with-background-pages',
    ],
    slow_mo=50,                        # ✅ Slow down 50ms for visibility
)
```

### Context Configuration

```python
context = await browser.new_context(
    user_agent=user_agent,
    viewport=viewport,
    locale='en-IN',
    timezone_id='Asia/Kolkata',
    ignore_https_errors=True,         # ✅ Better compatibility
)
```

## 🎯 Key Features

| Setting | Purpose |
|---------|---------|
| `headless=False` | Shows visible browser window during execution |
| `slow_mo=50` | Slows down all actions by 50ms (visible automation) |
| `--disable-extensions` | Cleaner browser interface |
| `--disable-plugins` | Removes plugin clutter |
| `--disable-images` | Optional: faster page loads |
| `ignore_https_errors=True` | Better HTTPS compatibility |

## 📊 When Running

You will see:
✅ A visible Chrome browser window opening  
✅ Real-time mouse movements  
✅ Scrolling actions  
✅ Button clicks and interactions  
✅ All actions slowed down for visibility (50ms delays)  
✅ Complete automation flow visible  

## 🚀 Example Commands

```powershell
# Run with visible browser
"C:/Program Files/Python312/python.exe" run_traffic.py -file "asins.xlsx" -limit 3

# Watch the automation happen in real-time!
```

## 💡 Tips

- The `slow_mo=50` setting makes all actions 50ms slower for better visibility
- Increase to `slow_mo=100` or `slow_mo=200` for even slower execution
- You can watch mouse movements, scrolling, and clicks in real-time
- Browser window will stay open until the simulation completes
- Perfect for debugging and understanding the automation flow

## 📝 Modify slow_mo Value

To adjust the slow-motion speed, edit this line in `traffic_simulator.py`:

```python
slow_mo=50,  # Change 50 to a higher value for slower execution
```

Examples:
- `slow_mo=0` - Normal speed (fast)
- `slow_mo=50` - Default (medium, 50ms delays)
- `slow_mo=100` - Slow (100ms delays)
- `slow_mo=200` - Very slow (200ms delays)

---

**Status**: ✅ Headfull browser mode is fully configured and ready to use!
