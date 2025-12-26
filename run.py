#!/usr/bin/env python3
"""
Main runner script for the review scraper
Run from VS Code terminal or command line
"""

import os
import sys
import json
from datetime import datetime, timedelta
import subprocess

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def run_scraper(company, start_date, end_date, source, output_file):
    """Run the scraper with given parameters"""
    cmd = [
        sys.executable, "src/scraper.py",
        "--company", company,
        "--start", start_date,
        "--end", end_date,
        "--source", source,
        "--output", output_file,
        "--verbose"
    ]
    
    print(f"\nRunning: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Success! Output saved to {output_file}")
        
        # Show sample of output
        try:
            with open(output_file, 'r') as f:
                data = json.load(f)
                print(f"Total reviews: {data['metadata']['total_reviews']}")
        except:
            pass
    else:
        print(f"✗ Failed: {result.stderr}")
    
    return result.returncode

def main():
    """Main runner function"""
    print_header("PRODUCT REVIEW SCRAPER - VS CODE EDITION")
    print("Built with Visual Studio Code - Complete 2-hour implementation")
    
    # Create necessary directories
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("data/cache", exist_ok=True)
    
    # Example runs
    examples = [
        {
            "name": "Example 1: Slack on G2",
            "company": "Slack",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "source": "g2",
            "output": "outputs/slack_g2.json"
        },
        {
            "name": "Example 2: Zoom on Capterra",
            "company": "Zoom",
            "start_date": "2023-06-01",
            "end_date": "2023-12-31",
            "source": "capterra",
            "output": "outputs/zoom_capterra.json"
        },
        {
            "name": "Example 3: Microsoft Teams on all sources",
            "company": "Microsoft Teams",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "source": "g2,capterra,softwareadvice",
            "output": "outputs/teams_all.json"
        },
        {
            "name": "Example 4: Notion with SoftwareAdvice (Bonus)",
            "company": "Notion",
            "start_date": "2023-07-01",
            "end_date": "2023-12-31",
            "source": "softwareadvice",
            "output": "outputs/notion_softwareadvice.json"
        }
    ]
    
    print("\nAvailable Examples:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['name']}")
    
    print("\nSelect example to run (1-4), or 'all' to run all:")
    choice = input("Your choice: ").strip().lower()
    
    if choice == 'all':
        for example in examples:
            print_header(example['name'])
            run_scraper(**example)
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        example = examples[int(choice) - 1]
        print_header(example['name'])
        run_scraper(**example)
    else:
        print("Running custom scrape...")
        company = input("Company name: ").strip()
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        end_date = input("End date (YYYY-MM-DD): ").strip()
        source = input("Source (g2, capterra, softwareadvice, or comma-separated): ").strip()
        output = input("Output file [default: outputs/custom.json]: ").strip()
        
        if not output:
            output = "outputs/custom.json"
        
        run_scraper(company, start_date, end_date, source, output)
    
    print_header("ALL DONE!")
    print("Check the 'outputs' folder for your JSON files.")
    print("Open 'scraper.log' for detailed logging information.")

if __name__ == "__main__":
    main()