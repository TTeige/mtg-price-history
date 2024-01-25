import json

from boto3 import client


def load_from_s3(object_key):
    s3_client = client('s3')
    resp = s3_client.get_object(Bucket="mtg-pricing-data", Key=object_key)
    return json.load(resp["Body"])


def get_object_key(event):
    object_key = None
    for record in event["Records"]:
        object_key = record["s3"]["object"]["key"]
    if object_key is None:
        return
    return object_key


def default_to_string(v):
    return "" if v is None else v


def chunk_list(l, chunk_size):
    for i in range(0, len(l), chunk_size):
        yield l[i:i + chunk_size]


def handle_event(event, context):
    object_key = get_object_key(event)

    data = load_from_s3(object_key)

    dynamodb_client = client('dynamodb')

    items_to_export = []

    print(f"Found {len(data.keys())} card names, uploading all")

    i = 0

    for c_name, sets in data.items():
        for set_name, card in sets.items():
            if len(card["multiverse_ids"]) != 1:
                print(f"No multiverse id for card: {card['name']} - {card['set_name']}")
                continue
            i += 1
            items_to_export.append(
                {
                    "PutRequest": {
                        "Item": {
                            "multiverse_id": {"S": str(card["multiverse_ids"][0])},
                            "date": {"S": object_key.split("_")[-1].split(".")[0]},
                            "set": {"S": card["set"]},
                            "set_name": {"S": card["set_name"]},
                            "usd": {"S": default_to_string(card["prices"]["usd"])},
                            "usd_foil": {"S": default_to_string(card["prices"]["usd_foil"])},
                            "eur": {"S": default_to_string(card["prices"]["eur"])},
                            "eur_foil": {"S": default_to_string(card["prices"]["eur_foil"])},
                            "usd_etched": {"S": default_to_string(card["prices"]["usd_etched"])},
                        }
                    }
                }
            )
    print(f"Found {i} cards in the file, sending all to dynamodb")
    items_to_export = chunk_list(items_to_export, 25)
    print(f"Sending chunks")
    for i, chunk in enumerate(items_to_export):
        print(f"Sending chunk number: {i}")
        resp = dynamodb_client.batch_write_item(
            RequestItem={
                "pricing_data": chunk
            }
        )

        print("Success for chunk")
