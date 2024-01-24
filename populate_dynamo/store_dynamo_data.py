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


def export_dynamodb(dynamodb_client, card, object_key):
    if len(card["multiverse_ids"]) != 1:
        print(f"No multiverse id for card: {card['name']} - {card['set_name']}")
        return
    dynamodb_client.put_item(
        TableName="pricing_data",
        Item={
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
    )


def handle_event(event, context):
    object_key = get_object_key(event)

    data = load_from_s3(object_key)

    dynamodb_client = client('dynamodb')

    for c_name, sets in data.items():
        for set_name, card in sets.items():
            export_dynamodb(dynamodb_client, card, object_key)
