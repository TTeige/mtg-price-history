import json
import os

from boto3 import client

import requests


def fetch_card_data(event=None, context=None):
    base_url = "https://api.scryfall.com"

    resp = requests.get(f"{base_url}/bulk-data/default_cards")
    if resp.status_code != 200:
        print(f"Unable to retrieve bulk metadata. Error code: {resp.status_code} - {resp.reason}")
        raise ValueError
    download_uri = resp.json()["download_uri"]

    resp = requests.get(download_uri)
    if resp.status_code != 200:
        print(f"Unable to retrieve bulk data. Error code: {resp.status_code} - {resp.reason}")
        raise ValueError

    fp = f"raw-data/{download_uri.split('/')[-1]}"

    local = os.getenv("local")

    if local is None and not local:
        print("File downloaded, writing to s3")
        s3_client = client("s3")
        resp = s3_client.put_object(Body=resp.json(), Bucket="mtg-pricing-data", Key=fp)
    else:
        with open(fp, "w") as f:
            json.dump(resp.json(), f)

        print(os.stat(fp))

    return fp


if __name__ == '__main__':
    fetch_card_data()
