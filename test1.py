from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        self.starfruit_prices = []

    def calculate_moving_average(self, period: int) -> float:
        if len(self.starfruit_prices) < period:
            return None
        else:
            return sum(self.starfruit_prices[-period:]) / period

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {"AMETHYSTS": [], "STARFRUIT": []}

        # Extracting order depths for AMETHYSTS and STARFRUIT
        amethysts_orders = state.order_depths.get("AMETHYSTS", None)
        starfruit_orders = state.order_depths.get("STARFRUIT", None)

        if amethysts_orders and starfruit_orders:
            # Determine the current position in AMETHYSTS
            amethysts_position = state.position.get("AMETHYSTS", 0)

            # Determine the current position in STARFRUIT
            starfruit_position = state.position.get("STARFRUIT", 0)

            # Update starfruit_prices with the latest price
            latest_price = starfruit_orders.last_price
            self.starfruit_prices.append(latest_price)

            # Calculate the moving average over a period of 5 time steps
            moving_average = self.calculate_moving_average(5)

            if moving_average is not None:
                # Check if we can buy more STARFRUIT
                if starfruit_position < 20 and latest_price < moving_average:
                    # Look at the top buy order for STARFRUIT
                    best_bid_starfruit = max(starfruit_orders.buy_orders.keys())

                    # Check if the best bid is acceptable
                    if best_bid_starfruit < 10:
                        # Calculate how much STARFRUIT we can buy
                        max_buy_starfruit = min(
                            20 - starfruit_position,
                            starfruit_orders.buy_orders[best_bid_starfruit],
                        )

                        # Place the buy order for STARFRUIT
                        result["STARFRUIT"].append(
                            Order("STARFRUIT", best_bid_starfruit, max_buy_starfruit)
                        )

                # Check if we can sell some STARFRUIT
                if starfruit_position > -20 and latest_price > moving_average:
                    # Look at the top sell order for STARFRUIT
                    best_ask_starfruit = min(starfruit_orders.sell_orders.keys())

                    # Check if the best ask is acceptable
                    if best_ask_starfruit > 10:
                        # Calculate how much STARFRUIT we can sell
                        max_sell_starfruit = min(
                            starfruit_position + 20,
                            starfruit_orders.sell_orders[best_ask_starfruit],
                        )

                        # Place the sell order for STARFRUIT
                        result["STARFRUIT"].append(
                            Order("STARFRUIT", best_ask_starfruit, -max_sell_starfruit)
                        )

        return result
