from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import numpy as np
import statistics
import collections
import copy

# empty_dict = {"STARTFRUIT": [], "AMETHYSTS": []}


class Trader:
    # prices = {"STARTFRUIT": [], "AMETHYSTS": []}
    # prices = copy.deepcopy(empty_dict)

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

    # Calculating the VWAP of the prices to trade on the exchange

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

        # price[product].append(total_value)
        if total_volume > 0:
            return total_value / total_volume
        else:
            return None

    def run(self, state: TradingState):
        result = {}

        for product in state.order_depths:
            order_depth = state.order_depths[product]
            orders = []
            position_limit = 20  # Assuming a position limit of ±20 for all products

            vwap = self.calculate_vwap(order_depth)  # Calculate VWAP

            acceptable_price = vwap if vwap else 10000
            current_position = state.position.get(product, 0)  # Get current position

            # Calculate the maximum buy and sell quantities allowed to stay within position limits
            max_buy_quantity = max(position_limit - current_position, 0)
            max_sell_quantity = max(current_position + position_limit, 0)

            # Check for buy signals
            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(
                    sorted(order_depth.sell_orders.items())
                )[0]
                if int(best_ask) <= acceptable_price:
                    # Adjust buy quantity to stay within position limits
                    buy_quantity = min(-best_ask_amount, max_buy_quantity)
                    if buy_quantity > 0:
                        print("BUY", str(-buy_quantity) + "x", best_ask)
                        orders.append(Order(product, best_ask, -buy_quantity))

            # Check for sell signals
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(
                    sorted(order_depth.buy_orders.items())
                )[-1]
                if int(best_bid) >= acceptable_price:
                    # Adjust sell quantity to stay within position limits
                    sell_quantity = min(best_bid_amount, max_sell_quantity)
                    if sell_quantity > 0:
                        print("SELL", str(sell_quantity) + "x", best_bid)
                        orders.append(Order(product, best_bid, -sell_quantity))

            result[product] = orders

        traderData = ""
        conversions = None

        return result, conversions, traderData
