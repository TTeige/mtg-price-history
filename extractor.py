import json
import os
from collections import defaultdict


def build_new_price_object(c):
    return {
        "multiverse_ids": c["multiverse_ids"],
        "name": c["name"],
        "set": c["set"],
        "set_name": c["set_name"],
        "prices": c["prices"],
        "purchase_uris": c["purchase_uris"]
    }


def extract_data(file_name):
    price_data = defaultdict(dict)  # Key is card_name and data is array of full objects as cards

    with open(file_name, "r", encoding="utf8") as f:
        data = json.load(f)
        for c in data:
            if c["legalities"]["commander"] == "not_legal":
                continue
            if c["prices"]["usd"] is None:
                continue
            price_data[c["name"]][c["set"]] = build_new_price_object(c)

    f_out_date_string = file_name.split("-")[-1].split(".")[0]
    year, month, day, hour = f_out_date_string[0:4], f_out_date_string[4:6], f_out_date_string[6:8], f_out_date_string[
                                                                                                     8:10]
    f_out = f"transformed_card_data/price_data_{year}-{month}-{day}-{hour}.json"
    with open(f_out, "w") as f_w:
        json.dump(price_data, f_w)
        print(os.stat(f_out))

    return f_out


if __name__ == '__main__':
    f_name = "raw_card_data/default-cards-20240118100432.json"
    extract_data(f_name)
