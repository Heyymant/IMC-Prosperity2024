from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List


class Trader:

    def calculate_sma(self, prices: List[float], window_size: int) -> float:
        if len(prices) < window_size:
            return sum(prices) / len(prices)
        else:
            return sum(prices[-window_size:]) / window_size

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
                # Mean-reversion strategy for STARFRUIT using SMA
                prices = list(order_depth.sell_orders.keys())
                sma = self.calculate_sma(
                    prices, window_size=5
                )  # Adjust window size as needed

                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if best_ask > sma:
                        # Sell if price is below SMA
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
                    if best_bid < sma:
                        # Buy if price is above SMA
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
