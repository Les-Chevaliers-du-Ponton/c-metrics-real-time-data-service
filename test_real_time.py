from redis import Redis

REDIS = Redis(
    host="cmetrics-cache-0001-001.w3yveh.0001.use1.cache.amazonaws.com",
    port=6379,
    decode_responses=True,
)


def test_live_data(exchange: str, pair: str, channel: str):
    while True:
        key = f"{channel}-{exchange.upper()}-{pair.upper()}"
        data = REDIS.xread(streams={"{real-time}-" + key: "$"}, block=0)
        data = data[0][1][0][1]
        print(f'{data["side"]} {data["amount"]} @ {data["price"]}')


if __name__ == "__main__":
    test_live_data("COINBASE", "BTC-USD", "trades")
