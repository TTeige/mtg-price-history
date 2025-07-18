import json
import os
import logging

from boto3 import client

import requests

logger = logging.getLogger()

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

    local = os.getenv("local")

    if local is None and not local:
        logger.info("Writing to s3")
        s3_client = client("s3")
        resp = s3_client.put_object(Body=json.dumps(resp.json()), Bucket="mtg-pricing-data", Key=fp)
        logger.info("Completed writing raw data to S3")

        transform_card_data(resp.json(), s3_client, fp)
    else:
        logger.info("Writing to disk")
        with open(f"../{fp}", "w") as f:
            json.dump(resp.json(), f)

    return fp

def build_new_price_object(c):
    return {
        "multiverse_ids": c["multiverse_ids"],
        "name": c["name"],
        "set": c["set"],
        "set_name": c["set_name"],
        "prices": c["prices"],
        "purchase_uris": c["purchase_uris"]
    }


def transform_card_data(data, s3_client, file_name):
    price_data = {}
    logger.info("Transforming card data")
    for c in data:
        if c["prices"]["usd"] is None or len(c["multiverse_ids"]) == 0:
            continue
        if c["prices"]["eur"] is None or len(c["multiverse_ids"]) == 0:
            continue
        price_data[c["name"]][c["set"]] = build_new_price_object(c)

    f_out_date_string = file_name.split("-")[-1].split(".")[0]
    year, month, day, hour = f_out_date_string[0:4], f_out_date_string[4:6], f_out_date_string[6:8], f_out_date_string[
                                                                                                     8:10]
    logger.info(f"Found {len(price_data.keys())} number of cards")
    f_out = f"prices/price_data_{year}-{month}-{day}-{hour}.json"

    s3_client.put_object(
        Body=json.dumps(price_data), Bucket="mtg-pricing-data", Key=f_out
    )


if __name__ == '__main__':
    fetch_card_data()
