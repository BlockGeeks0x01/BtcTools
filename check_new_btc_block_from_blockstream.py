import requests
import logging
import time


def config_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d (%(levelname)s): %(message)s",
        datefmt="%y-%m-%d %H:%M:%S"
    )

    logging.getLogger().setLevel(logging.INFO)


if __name__ == '__main__':
    config_logging()
    api_end_point = "https://blockstream.info/api/"
    session = requests.session()

    best_btc_block_hash = session.get(f"{api_end_point}/blocks/tip/hash").content.decode('utf-8')
    logging.info(f"current best bitcoin block hash: {best_btc_block_hash}")

    while True:
        current_block_hash = session.get(f"{api_end_point}/blocks/tip/hash").content.decode('utf-8')
        if current_block_hash != best_btc_block_hash:
            best_btc_block_hash = current_block_hash
            logging.info(f">>>>>>>>>>>>> find new btc block: {best_btc_block_hash}")
            block_header = session.get(f"{api_end_point}/block/{best_btc_block_hash}/header").content.decode('utf-8')
            logging.info("finish get block header")
            block_tx_list = session.get(f"{api_end_point}/block/{best_btc_block_hash}/txids").json()
            logging.info("finish get block tx list")
            coinbase_tx = session.get(f"{api_end_point}/tx/{block_tx_list[0]}/hex").content.decode('utf-8')
            logging.info("finish get coinbase tx")
        time.sleep(0.5)
