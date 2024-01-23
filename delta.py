import json
from collections import defaultdict


def calculate_delta(
        card_data_segments=None
):
    if card_data_segments is None:
        card_data_segments = [
            "transformed_card_data/price_data_2024-01-18-22.json",
            "transformed_card_data/price_data_2024-01-22-22.json"
        ]
    with open(card_data_segments[0], 'r') as f:
        price_data_first = json.load(f)
    with open(card_data_segments[1], 'r') as f:
        price_data_second = json.load(f)

    prices = defaultdict(list)
    prices = populate_price_dict(price_data_first, prices)
    prices = populate_price_dict(price_data_second, prices)
    calculate_deltas(prices)


def calculate_deltas(prices):
    target_cards = []
    for card_id, price_list in prices.items():
        if len(price_list) <= 1:
            continue

        max_val = max(price_list)
        min_val = min(price_list)
        if min_val < 2:
            continue
        delta = price_list[1] / max_val - price_list[0] / max_val
        if abs(delta) > 0.15:
            target_cards.append({
                "card_id": card_id,
                "delta": delta,
                "original_price": price_list[0],
                "new_price": price_list[1]
            })
    max_offset = max([len(x["card_id"]) for x in target_cards])

    print("Card name".ljust(max_offset + 4) + "Delta".ljust(10) + "Old".ljust(6) + "".ljust(4) + "New".ljust(6))
    for card in target_cards:
        delta_formatted = "{:.3f}".format(card["delta"]).ljust(6)
        card_id_padded = card["card_id"].ljust(max_offset)
        new_price_formatted = str(card["new_price"]).ljust(6)
        original_price_formatted = str(card["original_price"]).ljust(6)
        print(f"{card_id_padded} -> {delta_formatted} // {original_price_formatted} -> {new_price_formatted}")


def populate_price_dict(raw_data, prices):
    for card_name, set_object in raw_data.items():
        for set_short, card_object in set_object.items():
            card_prices = card_object["prices"]
            for price_type, value in card_prices.items():
                if value is None:
                    continue
                if price_type == "tix":
                    continue
                prices[f"{card_name} / {card_object['set_name']} / {price_type}"].append(float(value))
    return prices


if __name__ == '__main__':
    calculate_delta()
