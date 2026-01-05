"""
Run traffic simulator with Amazon cookies
Usage: python run_with_cookies.py -file "path/to/asins.xlsx" -cookies "path/to/cookies.json"
"""
import sys
import os
import json
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from traffic_simulator import run_simulator
import pandas as pd

def read_asins_from_file(filepath):
    """Read ASINs from Excel or CSV file"""
    try:
        if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            df = pd.read_excel(filepath)
        elif filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            raise ValueError("File must be .xlsx, .xls, or .csv")
        
        # Look for ASIN column (case insensitive)
        asin_column = None
        for col in df.columns:
            if 'asin' in col.lower():
                asin_column = col
                break
        
        if asin_column is None:
            asin_column = df.columns[0]
            print(f"⚠️  No 'ASIN' column found, using first column: {asin_column}")
        
        asins = df[asin_column].dropna().astype(str).tolist()
        return asins
    
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

def read_cookies_from_json(filepath):
    """Read cookies from JSON file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Handle different JSON formats
        if isinstance(data, dict) and 'cookies' in data:
            cookies = data['cookies']
        elif isinstance(data, list):
            cookies = data
        else:
            raise ValueError("JSON must contain 'cookies' array or be an array of cookies")
        
        print(f"✅ Loaded {len(cookies)} cookies from {filepath}")
        return cookies
    
    except Exception as e:
        print(f"❌ Error reading cookies: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Amazon Traffic Simulator with Cookies')
    parser.add_argument('-file', type=str, required=True, help='Path to Excel/CSV file with ASINs')
    parser.add_argument('-cookies', type=str, required=True, help='Path to JSON file with cookies')
    parser.add_argument('-limit', type=int, default=None, help='Limit number of ASINs to process')
    parser.add_argument('-delay', type=int, default=None, help='Delay between ASINs in seconds')
    
    args = parser.parse_args()
    
    # Read ASINs
    print(f"📂 Reading ASINs from: {args.file}")
    asins = read_asins_from_file(args.file)
    
    # Read cookies
    print(f"🍪 Reading cookies from: {args.cookies}")
    cookies = read_cookies_from_json(args.cookies)
    
    if args.limit:
        asins = asins[:args.limit]
        print(f"🔹 Limited to first {args.limit} ASINs")
    
    print(f"✅ Found {len(asins)} ASINs to simulate\n")
    
    # Run simulator with cookies
    run_simulator(asins, delay=args.delay, cookies=cookies)

if __name__ == "__main__":
    main()
