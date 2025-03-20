import json
import os
import requests
from datetime import datetime
import sys
import re

def load_existing_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"entries": []}

def clean_jsonp(jsonp_string):
    # Remove the JSONP callback wrapper and get pure JSON
    # Typical JSONP format: callback({...})
    try:
        # Extract the JSON part from JSONP
        json_str = re.search(r'\{.*\}', jsonp_string).group()
        return json.loads(json_str)
    except (AttributeError, json.JSONDecodeError) as e:
        print(f"Error parsing JSONP: {e}")
        sys.exit(1)

def fetch_new_data():
    base_url = "http://akz.imgfarm.com/pub/feeds/giphy/redditgif.jsonp"
    # Add timestamp to prevent caching
    url = f"{base_url}?v={int(datetime.utcnow().timestamp() * 1000)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Clean JSONP response to get pure JSON
        json_data = clean_jsonp(response.text)
        return json_data
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

def main():
    # Load existing data
    data = load_existing_data()
    
    # Fetch new data
    new_data = fetch_new_data()
    
    # Add timestamp to new data
    entry = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "data": new_data
    }
    
    # Append new data
    data["entries"].append(entry)
    
    # Save updated data
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()