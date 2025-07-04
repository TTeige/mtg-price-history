from raw_data_loader.card_fetcher import fetch_card_data
from price_transformer.extractor import lambda_handler


def run():
    f_raw = fetch_card_data()
    f_extracted = lambda_handler(f_raw)

if __name__ == '__main__':
    run()
