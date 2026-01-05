# 🎁 SHARE THIS EXACT INSTRUCTION WITH USERS

## How to Use Amazon Traffic Simulator

### Download
Download this file:
```
Amazon_Traffic_Simulator.exe (93.1 MB)
```

### That's It for Setup!
- No installation needed
- No Python required  
- Just double-click the EXE

---

## Quick Start (3 Steps)

### Step 1: Create ASIN File
Create an Excel file (.xlsx) or CSV file with your Amazon product codes:

**File name**: `asins.xlsx` (or any name)

**Content**:
```
ASIN
B0DK317TDD
B0CYPLPZRQ
B0CW5YN5HX
```

**Important**: 
- Column header must be named "ASIN"
- One ASIN per row
- Use Excel or any spreadsheet program

### Step 2: Export Cookies
From your Amazon account, export cookies as JSON:

1. Go to amazon.in
2. Login with your account
3. Open Chrome/Edge → Right-click → Inspect (or F12)
4. Install "EditThisCookie" extension OR use "Cookie Editor" extension
5. Export cookies as JSON
6. Save as `cookies.json`

**File format should look like**:
```json
{
  "cookies": [
    {
      "domain": ".amazon.in",
      "name": "session-id",
      "value": "your-session-id",
      "path": "/",
      "secure": true
    }
  ]
}
```

### Step 3: Run the Application

1. **Double-click** `Amazon_Traffic_Simulator.exe`
2. **GUI window opens** - Clean interface appears
3. **Click "Browse ASIN File"** - Select your `asins.xlsx`
4. **Click "Browse Cookie File"** - Select your `cookies.json`
5. **Optional Settings**:
   - Leave "Limit ASINs" as 0 for all
   - Leave "Delay" as 0 for random delays
6. **Click "▶️ START SIMULATION"** - Green button
7. **Watch it work!**:
   - Chrome opens automatically
   - Real-time log shows activity
   - Progress bar fills up
   - Success message when done

---

## What It Does

For each ASIN in your file:
1. ✅ Visits Amazon product page
2. ✅ Simulates human browsing (scrolling, mouse movements)
3. ✅ Views product details and images
4. ✅ Clicks "Buy Now" button
5. ✅ Waits realistic time
6. ✅ Moves to next ASIN

**Total time**: ~4 minutes per 10 ASINs

---

## Settings Explained

### Limit ASINs
- **0** = Process ALL ASINs in your file (default)
- **5** = Process only first 5 ASINs
- **100** = Process only first 100 ASINs

*Use 5-10 for testing, then run full batch*

### Delay Between ASINs
- **0** = Random delay 10-30 seconds (default)
- **15** = Fixed 15 seconds between each
- **30** = Fixed 30 seconds between each

*Use longer delays (30+) for larger batches*

---

## Real-time Progress

While running, you'll see:

```
📊 OUTPUT LOG:
✅ ASIN file loaded: 100 items
🍪 Cookies loaded: 13 cookies
[1/100] Processing ASIN: B0DK317TDD
📱 Visiting Amazon homepage...
✅ Homepage visited
📦 Opening product page...
✅ Product page loaded
🖱️  Simulating mouse movements...
📜 Scrolling through details...
🛒 Clicking Buy Now...
✅ Buy Now clicked!
⏸️ Waiting 15s before next...
[2/100] Processing ASIN: B0CYPLPZRQ
...
```

---

## Estimated Times

| Number of ASINs | Time | Notes |
|---|---|---|
| 10 | ~4 minutes | Quick test |
| 50 | ~21 minutes | Standard |
| 100 | ~42 minutes | Typical session |
| 500 | ~3.5 hours | Large batch |
| 1000 | ~7 hours | Overnight run |

*Varies by internet speed and delay setting*

---

## ⚠️ Important Notes

### Cookies
- ✅ Keep your cookies secure - don't share them
- ✅ Use cookies from your own verified account only
- ✅ Cookies expire - refresh monthly
- ✅ Don't share cookies with others

### Best Practices
- ✅ Test with 5-10 ASINs first
- ✅ Use realistic delays (not too fast)
- ✅ Monitor the first run
- ✅ Check output log for any errors

### Troubleshooting
- **"File not found"** → Use full path (C:\Users\Name\file.xlsx)
- **"Invalid JSON"** → Check cookies.json at jsonlint.com
- **No browser opens** → Check internet, disable VPN
- **Stops running** → Check output log for error details
- **Cookies expired** → Export fresh cookies from Amazon

---

## FAQ

**Q: Do I need Python installed?**
A: No! Python is bundled inside the EXE.

**Q: Will this work on my computer?**
A: Yes! Works on Windows 7, 8, 10, 11 (4GB RAM minimum).

**Q: Can I process 1000s of ASINs?**
A: Yes! Just set the limit and let it run overnight.

**Q: What if I get an error?**
A: Check the green output log - it shows exactly what went wrong.

**Q: How fast is it?**
A: About 4 minutes per 10 ASINs (realistic human speed).

**Q: Can I change the delay?**
A: Yes! Set "Delay Between ASINs" to any seconds.

**Q: Is it safe?**
A: Yes! Runs locally, no data collection, transparent code.

**Q: Can I use it multiple times?**
A: Yes! Run it as many times as you want.

---

## Support

If you have issues:

1. **Check the output log** (green text during execution)
   - It shows exactly what went wrong
   - Error messages are clear

2. **Validate your files**
   - ASIN file: Open in Excel, verify "ASIN" column
   - Cookie file: Check at jsonlint.com for valid JSON

3. **Verify cookies aren't expired**
   - Re-export from Amazon if needed
   - Make sure they're recent

4. **Check basics**
   - Internet connection active?
   - VPN disabled?
   - File paths correct?
   - Antivirus not blocking?

---

## System Requirements

- **OS**: Windows 7 or later
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 100MB free space
- **Internet**: Active connection required
- **Admin**: Not required

---

## Quick Checklist

Before running:

- [ ] Downloaded Amazon_Traffic_Simulator.exe
- [ ] Created ASIN file (Excel/CSV with ASIN column)
- [ ] Exported cookies from amazon.in as JSON
- [ ] Both files are valid format
- [ ] Internet connection is active
- [ ] Have 1-2 hours for test run or plan for overnight

---

## Success!

Once everything is set up:

1. Double-click the EXE
2. Select your files
3. Click START
4. Watch it automate
5. Check results when done

That's it! 🎉

---

## Need Help?

- Check the output log for errors
- Verify JSON cookies at jsonlint.com
- Make sure ASIN file has "ASIN" column
- Ensure cookies aren't expired
- Try with small batch (5 ASINs) first
- Check file paths are correct

---

## Questions?

Review the included guides:
- `USER_GUIDE.md` - Complete user manual
- `COOKIES_GUIDE.md` - Cookie export details
- `QUICK_REFERENCE.txt` - Quick reference

---

**You're ready to go! 🚀**

Download, prepare your files, and run!
