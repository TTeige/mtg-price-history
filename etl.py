from raw_data_loader.card_fetcher import fetch_card_data
from extractor import extract_data


def run():
    f_raw = fetch_card_data()
    f_extracted = extract_data(f_raw)

if __name__ == '__main__':
    run()
