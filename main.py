import math
import multiprocessing

from cryptofeed import FeedHandler
from cryptofeed import defines as callbacks
from cryptofeed.backends import redis
from cryptofeed.exchanges import EXCHANGE_MAP


class MarketDataAggregator:
    def __init__(
        self,
        exchanges: list = None,
        pairs: list = None,
        ref_currency: str = None,
        max_cpu_amount: int = None,
    ):
        self.cpu_amount = (
            max_cpu_amount if max_cpu_amount else multiprocessing.cpu_count() - 1
        )
        self.exchanges = (
            {exchange: EXCHANGE_MAP[exchange] for exchange in exchanges}
            if exchanges
            else EXCHANGE_MAP
        )
        self.pairs = pairs
        self.ref_currency = ref_currency
        self.markets = self.get_markets()

    def get_markets(self) -> dict:
        markets = dict()
        for exchange_name, exchange_object in self.exchanges.items():
            pairs = exchange_object.symbols()
            filtered_pairs = list()
            for pair in pairs:
                if not self.pairs or pair in self.pairs:
                    _, quote = pair.split("-")
                    if "PINDEX" not in pair and (
                        not self.ref_currency or quote == self.ref_currency
                    ):
                        filtered_pairs.append(pair)
            if filtered_pairs:
                markets[exchange_name] = filtered_pairs
        return markets

    def break_down_pairs_per_cpu(self) -> list:
        total_amount_of_pairs = 0
        for pairs in self.markets.values():
            total_amount_of_pairs += len(pairs)
        symbols_per_process = math.ceil(total_amount_of_pairs / self.cpu_amount)
        current_sub_dict = dict()
        sub_lists = list()
        for exchange, exchange_pairs in self.markets.items():
            for pair in exchange_pairs:
                total_amount_of_pairs = sum(
                    len(values) for values in current_sub_dict.values()
                )
                if total_amount_of_pairs >= symbols_per_process:
                    sub_lists.append(current_sub_dict)
                    current_sub_dict = dict()
                if exchange not in current_sub_dict:
                    current_sub_dict[exchange] = list()
                current_sub_dict[exchange].append(pair)
        sub_lists.append(current_sub_dict)
        return sub_lists

    def run_process(self, markets: dict):
        f = FeedHandler()
        all_callbacks = {
            callbacks.L2_BOOK: redis.BookStream(host='redis'),
            callbacks.TRADES: redis.TradeStream(host='redis'),
            # callbacks.FUNDING: redis.FundingStream,
            # callbacks.TICKER: redis.TickerStream,
            # callbacks.OPEN_INTEREST: redis.OpenInterestStream,
            # callbacks.LIQUIDATIONS: redis.LiquidationsStream,
            # callbacks.CANDLES: redis.CandlesStream,
        }
        for exchange, exchange_pairs in markets.items():
            f.add_feed(
                EXCHANGE_MAP[exchange](
                    channels=list(all_callbacks.keys()),
                    symbols=exchange_pairs,
                    callbacks=all_callbacks,
                )
            )
        f.run()

    def start_all_feeds(self):
        sub_markets = self.break_down_pairs_per_cpu()
        processes = list()
        for markets in sub_markets:
            process = multiprocessing.Process(target=self.run_process, args=(markets,))
            processes.append(process)
            process.start()


if __name__ == "__main__":
    aggregator = MarketDataAggregator(exchanges=["COINBASE"], ref_currency='USD')
    aggregator.start_all_feeds()
    while True:
        pass
