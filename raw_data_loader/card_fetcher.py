import json
import os

from boto3 import client

import requests


def fetch_card_data(event=None, context=None):
    base_url = "https://api.scryfall.com"

    print("Retrieving file metadata")
    resp = requests.get(f"{base_url}/bulk-data/default_cards")
    if resp.status_code != 200:
        print(f"Unable to retrieve bulk metadata. Error code: {resp.status_code} - {resp.reason}")
        raise ValueError
    download_uri = resp.json()["download_uri"]

    print("Initializing download")
    resp = requests.get(download_uri)
    if resp.status_code != 200:
        print(f"Unable to retrieve bulk data. Error code: {resp.status_code} - {resp.reason}")
        raise ValueError

    print("File downloaded")
    fp = f"raw-data/{download_uri.split('/')[-1]}"

    local = os.getenv("local")

    if local is None and not local:
        print("Writing to s3")
        s3_client = client("s3")
        resp = s3_client.put_object(Body=json.dumps(resp.json()), Bucket="mtg-pricing-data", Key=fp)
    else:
        print("Writing to disk")
        with open(f"../{fp}", "w") as f:
            json.dump(resp.json(), f)

    return fp


if __name__ == '__main__':
    fetch_card_data()
