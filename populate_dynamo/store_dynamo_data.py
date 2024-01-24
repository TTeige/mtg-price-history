import json

from boto3 import client


def load_from_s3(object_key):
    s3_client = client('s3')
    return json.loads(s3_client.get_object(Bucket="mtg-pricing-data", Key=object_key)["Body"])


def get_object_key(event):
    object_key = None
    for record in event["Records"]:
        object_key = record["s3"]["object"]["key"]
    if object_key is None:
        return
    return object_key


def export_dynamodb(dynamodb_client, card, object_key):
    dynamodb_client.put_item(
        TableName="pricing_data",
        Item={
            "multiverse_id": {"S": card["multiverse_ids"][0]},
            "date": {"S": object_key.split("_")[-1].split(".")[0]},
            "set": {"S": card["set"]},
            "set_name": {"S": card["set_name"]},
            "usd": {"S": card["prices"]["usd"]},
            "usd_foil": {"S": card["prices"]["usd_foil"]},
            "eur": {"S": card["prices"]["eur"]},
            "eur_foil": {"S": card["prices"]["eur_foil"]},
            "usd_etched": {"S": card["prices"]["usd_etched"]},
        }
    )


def handle_event(event, context):
    object_key = get_object_key(event)

    data = load_from_s3(object_key)

    dynamodb_client = client('dynamodb')

    for c_name, sets in data.items():
        for set_name, card in sets.items():
            export_dynamodb(dynamodb_client, card, object_key)
