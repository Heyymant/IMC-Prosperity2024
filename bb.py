from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import numpy as np


class Trader:

    def calculate_bollinger_bands(
        self, prices: List[float], window_size: int, num_std_dev: int
    ) -> (float, float):
        if len(prices) < window_size:
            return None, None

        sma = np.mean(prices[-window_size:])
        std_dev = np.std(prices[-window_size:])
        upper_band = sma + num_std_dev * std_dev
        lower_band = sma - num_std_dev * std_dev

        return upper_band, lower_band

    def run(self, state: TradingState):
        result = {}

        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []

            if product == "AMETHYSTS":
                # Buy and hold AMETHYSTS
                if state.position.get("AMETHYSTS", 0) < 20:
                    orders.append(
                        Order("AMETHYSTS", 10, 20 - state.position.get("AMETHYSTS", 0))
                    )

            elif product == "STARFRUIT":
                # Bollinger Bands strategy for STARFRUIT
                prices = list(order_depth.sell_orders.keys())
                upper_band, lower_band = self.calculate_bollinger_bands(
                    prices, window_size=20, num_std_dev=2
                )

                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if best_ask <= lower_band:
                        # Buy when price touches or falls below the lower band
                        if state.position.get("STARFRUIT", 0) < 20:
                            orders.append(
                                Order(
                                    "STARFRUIT",
                                    best_ask,
                                    20 - state.position.get("STARFRUIT", 0),
                                )
                            )

                if len(order_depth.buy_orders) != 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if best_bid >= upper_band:
                        # Sell when price touches or rises above the upper band
                        if state.position.get("STARFRUIT", 0) > 0:
                            orders.append(
                                Order(
                                    "STARFRUIT",
                                    best_bid,
                                    -state.position.get("STARFRUIT", 0),
                                )
                            )

            result[product] = orders

        traderData = "SAMPLE"  # Update with any trader data as needed

        conversions = 1  # Update with any conversions as needed

        return result, conversions, traderData
