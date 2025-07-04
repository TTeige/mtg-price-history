import json
import logging
from collections import defaultdict

from boto3 import client

s3_client = client("s3")

logger = logging.getLogger()
logger.setLevel("INFO")
logger.info("Initialized extractor module")


def build_new_price_object(c):
    return {
        "multiverse_ids": c["multiverse_ids"],
        "name": c["name"],
        "set": c["set"],
        "set_name": c["set_name"],
        "prices": c["prices"],
        "purchase_uris": c["purchase_uris"]
    }


def lambda_handler(event=None, context=None):
    logger.info("Starting price data extraction")
    price_data = defaultdict(dict)  # Key is card_name and data is array of full objects as cards
    object_key = None
    print(f"Received event with {len(event['Records'])} number of records")
    for record in event["Records"]:
        object_key = record["s3"]["object"]["key"]
    if object_key is None:
        return

    logger.info(f"Processing object {object_key}")
    resp = s3_client.get_object(Bucket="mtg-pricing-data", Key=object_key)

    data = json.load(resp["Body"])
    for c in data:
        if c["prices"]["usd"] is None or len(c["multiverse_ids"]) == 0:
            continue
        if c["prices"]["eur"] is None or len(c["multiverse_ids"]) == 0:
            continue
        price_data[c["name"]][c["set"]] = build_new_price_object(c)

    f_out_date_string = object_key.split("-")[-1].split(".")[0]
    year, month, day, hour = f_out_date_string[0:4], f_out_date_string[4:6], f_out_date_string[6:8], f_out_date_string[
                                                                                                     8:10]
    logger.info(f"Found {len(price_data.keys())} number of cards")
    f_out = f"prices/price_data_{year}-{month}-{day}-{hour}.json"

    s3_client.put_object(
        Body=json.dumps(price_data), Bucket="mtg-pricing-data", Key=f_out
    )

    return f_out
