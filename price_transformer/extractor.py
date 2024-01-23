import json
from collections import defaultdict

from boto3 import client


def build_new_price_object(c):
    return {
        "multiverse_ids": c["multiverse_ids"],
        "name": c["name"],
        "set": c["set"],
        "set_name": c["set_name"],
        "prices": c["prices"],
        "purchase_uris": c["purchase_uris"]
    }


def extract_data(event=None, context=None):
    price_data = defaultdict(dict)  # Key is card_name and data is array of full objects as cards
    object_key = None
    for record in event["Records"]:
        object_key = record[0]["s3"]["object"]["key"]
    if object_key is None:
        return

    s3_client = client("s3")
    resp = s3_client.get_object(Bucket="mtg-pricing-data", Key=object_key)

    data = json.load(resp["Body"])
    for c in data:
        if c["legalities"]["commander"] == "not_legal":
            continue
        if c["prices"]["usd"] is None:
            continue
        price_data[c["name"]][c["set"]] = build_new_price_object(c)

    f_out_date_string = object_key.split("-")[-1].split(".")[0]
    year, month, day, hour = f_out_date_string[0:4], f_out_date_string[4:6], f_out_date_string[6:8], f_out_date_string[
                                                                                                     8:10]
    f_out = f"prices/price_data_{year}-{month}-{day}-{hour}.json"

    s3_client.put_object(
        Body=json.dumps(price_data), Bucket="mtg-pricing-data", Key=f_out
    )

    return f_out


if __name__ == '__main__':
    f_name = "raw_card_data/default-cards-20240118100432.json"
    extract_data()
