import json
import os
import logging
from collections import defaultdict

from boto3 import client

import requests

local = os.getenv("local")

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def fetch_card_data():
    base_url = "https://api.scryfall.com"

    logger.info("Retrieving file metadata")
    resp = requests.get(f"{base_url}/bulk-data/default_cards")
    if resp.status_code != 200:
        logger.info(f"Unable to retrieve bulk metadata. Error code: {resp.status_code} - {resp.reason}")
        raise ValueError
    download_uri = resp.json()["download_uri"]

    logger.info("Initializing download")
    resp = requests.get(download_uri)
    if resp.status_code != 200:
        logger.info(f"Unable to retrieve bulk data. Error code: {resp.status_code} - {resp.reason}")
        raise ValueError

    logger.info("File downloaded")
    fp = f"raw-data/{download_uri.split('/')[-1]}"

    data = resp.json()

    if local is None and not local:
        logger.info("Writing to s3")
        s3_client = client("s3")

        s3_client.put_object(Body=json.dumps(data), Bucket="mtg-pricing-data", Key=fp)
        logger.info("Completed writing raw data to S3")

        transform_card_data(data, s3_client, fp)
    else:
        logger.info("Writing to disk")
        with open(f"../{fp}", "w") as f:
            json.dump(data, f)

    return fp


def build_new_price_object(c):
    return {
        "multiverse_ids": c["multiverse_ids"],
        "name": c["name"],
        "set": c["set"],
        "set_name": c["set_name"],
        "prices": c["prices"],
        "purchase_uris": c["purchase_uris"],
        "image_uri": c["image_uris"]["normal"] if "image_uris" in c else None,
        "scryfall_id": c["id"],
        "cardmarket_id": c["cardmarket_id"] if "cardmarket_id" in c else None,
    }


def transform_card_data(data, s3_client, file_name):
    price_data = defaultdict(dict)
    logger.info("Transforming card data")
    for c in data:
        if c["oversized"] is True:
            continue
        if "games" not in c:
            continue
        if "paper" not in c["games"]:
            continue
        price_data[c["name"]][c["set"]] = build_new_price_object(c)

    f_out_date_string = file_name.split("-")[-1].split(".")[0]
    year, month, day, hour = f_out_date_string[0:4], f_out_date_string[4:6], f_out_date_string[6:8], f_out_date_string[
                                                                                                     8:10]
    logger.info(f"Found {len(price_data.keys())} number of cards")
    f_out = f"prices/price_data_{year}-{month}-{day}-{hour}.json"

    if local is None and not local:
        s3_client.put_object(
            Body=json.dumps(price_data), Bucket="mtg-pricing-data", Key=f_out
        )
    else:
        logger.info(price_data)


if __name__ == '__main__':
    fetch_card_data()
