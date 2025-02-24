from nexustrader.constants import settings
from nexustrader.config import (
    Config,
    PublicConnectorConfig,
    PrivateConnectorConfig,
    BasicConfig,
)
from nexustrader.strategy import Strategy
from nexustrader.constants import ExchangeType, OrderSide, OrderType
from nexustrader.exchange.binance import BinanceAccountType
from nexustrader.schema import BookL1, Order
from nexustrader.engine import Engine
from nexustrader.core.log import SpdLog
from nexustrader.constants import KlineInterval
SpdLog.initialize(level="INFO", file_name="tp_sl_order", production_mode=True)

BINANCE_API_KEY = settings.BINANCE.FUTURE.TESTNET_1.API_KEY
BINANCE_SECRET = settings.BINANCE.FUTURE.TESTNET_1.SECRET


class Demo(Strategy):
    def __init__(self):
        super().__init__()
        self.signal = True
        self.order_id = None

    def on_start(self):
        self.subscribe_bookl1(symbols=["BTCUSDT-PERP.BINANCE"])
        self.schedule(self.query_position, trigger="interval", seconds=1)
    
    def query_position(self):
        positions_dict = self.cache.get_all_positions(exchange=ExchangeType.BINANCE)
        
        pos = positions_dict["BTCUSDT-PERP.BINANCE"]
        
        print(pos.amount, pos.symbol, pos.side, type(pos.amount))
            
           
        
    def on_canceled_order(self, order: Order):
        print(order, "\n")

    def on_failed_order(self, order: Order):
        print(order, "\n")

    def on_partially_filled_order(self, order: Order):
        print(order, "\n")

    def on_pending_order(self, order: Order):
        print(order, "\n")

    def on_accepted_order(self, order: Order):
        print(order, "\n")

    def on_filled_order(self, order: Order):
        print(order, "\n")

    def on_bookl1(self, bookl1: BookL1):
        if self.signal:
            self.create_adp_maker(
                symbol=bookl1.symbol,
                side=OrderSide.BUY,
                amount=0.002,
                duration=10,
                wait=8,
                trigger_tp_ratio=0.1,
                trigger_sl_ratio=0.1,
                sl_tp_duration=10,
                account_type=BinanceAccountType.USD_M_FUTURE_TESTNET,
            )
            self.signal = False

config = Config(
    strategy_id="tp_sl_order",
    user_id="user_test",
    strategy=Demo(),
    basic_config={
        ExchangeType.BINANCE: BasicConfig(
            api_key=BINANCE_API_KEY,
            secret=BINANCE_SECRET,
            testnet=True,
        )
    },
    public_conn_config={
        ExchangeType.BINANCE: [
            PublicConnectorConfig(
                account_type=BinanceAccountType.USD_M_FUTURE_TESTNET,
            )
        ]
    },
    private_conn_config={
        ExchangeType.BINANCE: [
            PrivateConnectorConfig(
                account_type=BinanceAccountType.USD_M_FUTURE_TESTNET,
            )
        ]
    },
)

engine = Engine(config)

if __name__ == "__main__":
    try:
        engine.start()
    finally:
        engine.dispose()
