import os
import json
from api.dex import fetch_tokens  # assume dex.py exposes a get_tokens() function
from apify_client import ApifyClient

def main():
    # 1) Scrape the data
    items = get_tokens(blockchain="Solana")  # or pass args from INPUT_SCHEMA
    
    # 2) Push into the default Apify dataset
    client = ApifyClient(os.getenv("APIFY_TOKEN"))
    dataset_id = os.getenv("APIFY_DEFAULT_DATASET_ID")
    client.dataset(dataset_id).push_items(items)
    
    print(f"Pushed {len(items)} items to dataset {dataset_id}")

if __name__ == "__main__":
    main()
