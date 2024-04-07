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

    def run(self, state):
        # empty dictionary to later store the results and trades
        result = {}
        totalPnl = 0
        price_data_1 = []
        price_data_2 = []

        for product in state.order_depths:
            order_depth = state.order_depths[product]
            orders = []
            pnl = 0

            if product == "AMETHYSTS":
                am_prices_sell = min(list(order_depth.sell_orders.keys()))
                am_prices_buy = max(list(order_depth.buy_orders.keys()))
                a_price = (am_prices_buy + am_prices_sell) / 2
                price_data_1.append(a_price)

                mean = self.mean(price_data_1)

                if len(order_depth.sell_orders) != 0:
                    best_ask = min(
                        order_depth.sell_orders, key=order_depth.sell_orders.get
                    )
                    best_ask_amount = order_depth.sell_orders[best_ask]

                    # buy orders
                    if best_ask < mean and state.position[product] < 20:
                        state.position[product] = (
                            state.position[product] - best_ask_amount
                        )
                        orders.append(Order(product, best_ask, -best_ask_amount))
                        pnl -= best_ask * best_ask_amount  # Subtract from pnl

                if len(order_depth.buy_orders) != 0:
                    best_bid = max(
                        order_depth.buy_orders, key=order_depth.buy_orders.get
                    )
                    best_bid_amount = order_depth.buy_orders[best_bid]

                    # the buying amount of the asset is more than sma
                    # means we can sell it at lower price
                    # so we place a sell order

                    if int(best_bid) > mean and state.position[product] > 0:
                        state.position[product] = (
                            state.position[product] - best_bid_amount
                        )
                        orders.append(Order(product, best_bid, -best_bid_amount))
                        pnl += best_bid * best_bid_amount  # Add to pnl

            if product == "STARFRUIT":
                star_prices_sell = min(list(order_depth.sell_orders.keys()))
                star_prices_buy = max(list(order_depth.buy_orders.keys()))
                s_price = (star_prices_buy + star_prices_sell) / 2
                price_data_2.append(s_price)
                sma = self.calculate_sma(price_data_2, window=5)

                if len(order_depth.sell_orders) != 0:
                    best_ask = min(
                        order_depth.sell_orders, key=order_depth.sell_orders.get
                    )
                    best_ask_amount = order_depth.sell_orders[best_ask]

                    # the selling amount of the asset is less than sma
                    # means we can buy it at lower price
                    # so we place a buy order

                    if int(best_ask) < sma and state.position["STARFRUIT"] < 20:
                        state.position["STARFRUIT"] = (
                            state.position["STARFRUIT"] - best_ask_amount
                        )
                        orders.append(Order("STARFRUIT", best_ask, -best_ask_amount))
                        pnl -= best_ask * best_ask_amount  # Subtract from pnl

                # Generating sell signal
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(
                        order_depth.buy_orders, key=order_depth.buy_orders.get
                    )
                    best_bid_amount = order_depth.buy_orders[best_bid]

                    # the buying amount of the asset is more than sma
                    # means we can sell it at lower price
                    # so we place a sell order

                    if best_bid > sma and state.position["STARFRUIT"] > 0:
                        state.position["STARFRUIT"] = (
                            state.position["STARFRUIT"] - best_bid_amount
                        )
                        orders.append(Order("STARFRUIT", best_bid, -best_bid_amount))
                        pnl += best_bid * best_bid_amount  # Add to pnl

            result[product] = orders
            totalPnl += pnl
            traderData = ""
            conversions = 1

        return result, conversions, traderData
