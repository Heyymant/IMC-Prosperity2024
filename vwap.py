from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import numpy as np
import statistics


class Trader:

    def calculate_sma(self, prices, window):
        if len(prices) < window:
            return sum(prices) / len(prices)
        else:
            return sum(prices[-window:]) / window

    def mean(self, prices):
        return np.mean(prices)

    def accept_amy(self, price_1, order_depth):
        am_prices_sell = min(list(order_depth.sell_orders.keys()))
        am_prices_buy = max(list(order_depth.buy_orders.keys()))
        a_price = (am_prices_buy + am_prices_sell) / 2
        price_1.append(a_price)

    def accept_star(self, price_2, order_depth):
        star_prices_sell = min(list(order_depth.sell_orders.keys()))
        star_prices_buy = max(list(order_depth.buy_orders.keys()))
        s_price = (star_prices_buy + star_prices_sell) / 2
        price_2.append(s_price)

    def calculate_vwap(self, order_depth: OrderDepth) -> float:
        total_value = 0
        total_volume = 0

        # For buy orders
        for price, volume in order_depth.buy_orders.items():
            total_value += price * volume
            total_volume += volume

        # For sell orders
        for price, volume in order_depth.sell_orders.items():
            total_value += price * abs(
                volume
            )  # Using abs() since sell volumes are negative
            total_volume += abs(volume)

        if total_volume > 0:
            return total_value / total_volume
        else:
            return None

    def run(self, state):
        result = {}
        price_1 = []
        price_2 = []

        for product in state.order_depths:
            order_depth = state.order_depths[product]
            orders = []
            vwap = self.calculate_vwap(order_depth)
            acceptable_price = vwap if vwap else 10
            # if product == "AMETHYSTS":
            #     self.accept_amy(price_1, order_depth=order_depth)
            #     acceptable_price = self.mean(price_1)

            # elif product == "STARFRUIT":
            #     self.accept_star(price_2, order_depth=order_depth)
            #     acceptable_price = self.calculate_sma(price_2, window=5)

            # checking for buy signals
            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if int(best_ask) < acceptable_price:
                    # state.position[product] += abs(int(best_ask_amount))
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))

            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if int(best_bid) > acceptable_price:
                    # state.position[product] -= abs(int(best_bid_amount))
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_amount))

            result[product] = orders

        traderData = ""
        conversions = 1

        return result, conversions, traderData
