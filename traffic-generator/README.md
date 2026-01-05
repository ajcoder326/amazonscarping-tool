# Amazon Traffic Generator

## Description
This tool simulates **real human user behavior** on Amazon product pages to generate traffic and engagement.

## Features
- ✅ Visits Amazon homepage first (randomly)
- ✅ Opens product pages
- ✅ Simulates mouse movements
- ✅ Scrolls like a human reading
- ✅ Views product images
- ✅ Reads product details
- ✅ **Clicks "Buy Now" button**
- ✅ Stays on page for realistic timing
- ✅ Uses real browser (visible)
- ✅ Anti-detection measures

## Installation
```bash
# Install required packages (if not already installed)
pip install playwright pandas openpyxl
pip install playwright-stealth

# Install Playwright browsers
playwright install chromium
```

## Usage

### Method 1: Run with Excel/CSV file
```bash
# Basic usage
python run_traffic.py -file "path/to/your/asins.xlsx"

# Limit to first 10 ASINs
python run_traffic.py -file "path/to/your/asins.xlsx" -limit 10

# Custom delay between ASINs (20 seconds)
python run_traffic.py -file "path/to/your/asins.xlsx" -delay 20
```

### Method 2: Use in Python code
```python
from traffic_simulator import run_simulator

# Single ASIN
run_simulator("B0DK317TDD")

# Multiple ASINs
asins = ["B0DK317TDD", "B0CYPLPZRQ", "B0CW5YN5HX"]
run_simulator(asins, delay=15)
```

## Example
```bash
# Simulate traffic for first 5 ASINs with 20 second delays
python run_traffic.py -file "C:\Users\dj\Downloads\Pending Asin 15128.xlsx" -limit 5 -delay 20
```

## What It Does

For each ASIN, the simulator:

1. **Optional Homepage Visit** (30% chance)
   - Visits amazon.in
   - Scrolls around
   - Simulates browsing

2. **Product Page Visit**
   - Opens product page
   - Waits for page load

3. **Human-like Interaction**
   - Random mouse movements (3-6 times)
   - Scrolling up and down
   - Hovering over elements

4. **Product Exploration**
   - Views product images
   - Reads feature bullets
   - Checks product description
   - Views product details

5. **Buy Now Click** 🎯
   - Finds Buy Now button
   - Hovers before clicking
   - Clicks the button
   - Waits for page response

6. **Realistic Timing**
   - Stays on page 3-6 seconds after click
   - Total session: ~15-30 seconds per ASIN

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-file` | Path to Excel/CSV with ASINs | Required |
| `-limit` | Max ASINs to process | All |
| `-delay` | Seconds between ASINs | Random 10-30s |

## Notes
- **Visible browser** - You'll see Chrome windows opening
- **Realistic behavior** - Designed to look like real users
- **No data extraction** - Only generates traffic
- **Login prompt** - Buy Now may show login (that's normal)
- **Rate limiting** - Use reasonable delays to avoid detection

## File Format
Your Excel/CSV should have an `ASIN` column:
```
ASIN
B0DK317TDD
B0CYPLPZRQ
B0CW5YN5HX
```

## Timing Estimates
- **Per ASIN**: ~20-30 seconds
- **10 ASINs**: ~4-6 minutes
- **100 ASINs**: ~40-60 minutes

## Tips
1. Start with small batches (5-10 ASINs)
2. Use realistic delays (15-30 seconds between ASINs)
3. Don't run too many sessions simultaneously
4. Monitor for any detection/blocking
