"""
CLI Runner for Traffic Simulator
Run from command line with Excel/CSV file input
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from traffic_simulator import run_simulator
import pandas as pd
import argparse

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
            # If no ASIN column found, use first column
            asin_column = df.columns[0]
            print(f"⚠️  No 'ASIN' column found, using first column: {asin_column}")
        
        asins = df[asin_column].dropna().astype(str).tolist()
        return asins
    
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Amazon Traffic Simulator - Simulate real user behavior')
    parser.add_argument('-file', type=str, required=True, help='Path to Excel/CSV file with ASINs')
    parser.add_argument('-limit', type=int, default=None, help='Limit number of ASINs to process')
    parser.add_argument('-delay', type=int, default=None, help='Delay between ASINs in seconds (default: random 10-30s)')
    
    args = parser.parse_args()
    
    # Read ASINs
    print(f"📂 Reading ASINs from: {args.file}")
    asins = read_asins_from_file(args.file)
    
    if args.limit:
        asins = asins[:args.limit]
        print(f"🔹 Limited to first {args.limit} ASINs")
    
    print(f"✅ Found {len(asins)} ASINs to simulate")
    
    # Run simulator
    run_simulator(asins, delay=args.delay)

if __name__ == "__main__":
    main()
