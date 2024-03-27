import os
from dotenv import load_dotenv
from redis import Redis

load_dotenv()

REDIS = Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    decode_responses=True,
)


def test_live_data(exchange: str, pair: str, channel: str):
    while True:
        key = f"{channel}-{exchange.upper()}-{pair.upper()}"
        data = REDIS.xread(streams={"{real-time}-" + key: "$"}, block=0)
        data = data[0][1]
        print(data)


if __name__ == "__main__":
    test_live_data("COINBASE", "BTC-USD", "trades")
