import os
import logging
from dotenv import load_dotenv
from bitcoinrpc.authproxy import AuthServiceProxy


def config_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d (%(levelname)s): %(message)s",
        datefmt="%y-%m-%d %H:%M:%S"
    )

    logging.getLogger().setLevel(logging.INFO)


if __name__ == '__main__':
    config_logging()
    load_dotenv()
    btc_rpc_user = os.environ['btc_rpc_user']
    btc_rpc_password = os.environ['btc_rpc_password']

    rpc_conn = AuthServiceProxy(f"http://{btc_rpc_user}:{btc_rpc_password}@127.0.0.1:8332")
    best_btc_block_hash = rpc_conn.getbestblockhash()
    logging.info(f"current best bitcoin block hash: {best_btc_block_hash}")

    while True:
        current_block_hash = rpc_conn.getbestblockhash()
        if current_block_hash != best_btc_block_hash:
            best_btc_block_hash = current_block_hash
            logging.info(f">>>>>>>>>>>>> find new btc block: {best_btc_block_hash}")
