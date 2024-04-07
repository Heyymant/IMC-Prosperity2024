from typing import Dict, List
from datamodel import (
    Order,
    TradingState,
    Trade,
    OrderDepth,
    UserId,
    Observation,
    ObservationValue,
    ConversionObservation,
)


class TutorialTrader:
    def __init__(self):
        self.position_limits = {"AMETHYSTS": 20, "STARFRUIT": 20}
        self.price_history = {"STARFRUIT": []}

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        traderData = ""

        # Update price history with trades
        self.update_price_history(state.market_trades.get("STARFRUIT", []))

        for product, order_depth in state.order_depths.items():
            orders = []

            if product == "AMETHYSTS":
                continue  # Skip AMETHYSTS since it's constant

            # Calculate moving average of historical prices for STARFRUIT
            moving_avg = self.calculate_moving_average("STARFRUIT")

            # Set buy and sell prices based on moving average
            buy_price = round(moving_avg * 0.95)  # Buy at 5% below moving average
            sell_price = round(moving_avg * 1.05)  # Sell at 5% above moving average

            # Create buy order if position allows and buy price is lower than best ask
            if self.check_position_limit(
                state, product, 1
            ) and buy_price < self.get_best_ask(order_depth):
                orders.append(Order(product, buy_price, 1))

            # Create sell order if position allows and sell price is higher than best bid
            if self.check_position_limit(
                state, product, -1
            ) and sell_price > self.get_best_bid(order_depth):
                orders.append(Order(product, sell_price, -1))

            result[product] = orders

        return result, conversions, traderData

    def calculate_moving_average(self, product: str) -> float:
        """Calculates the moving average of historical prices for the given product."""
        history = self.price_history[product]
        if history:
            return sum(history) / len(history)
        else:
            return 0  # If no history, return 0

    def update_price_history(self, trades: List[Trade]):
        """Updates the price history based on the trades."""
        for trade in trades:
            if trade.symbol == "STARFRUIT":
                self.price_history["STARFRUIT"].append(trade.price)

    def get_best_ask(self, order_depth: OrderDepth) -> int:
        """Returns the best ask price from the order depth."""
        if order_depth.sell_orders:
            return min(order_depth.sell_orders.keys())
        else:
            return float("inf")  # Return infinity if no asks

    def get_best_bid(self, order_depth: OrderDepth) -> int:
        """Returns the best bid price from the order depth."""
        if order_depth.buy_orders:
            return max(order_depth.buy_orders.keys())
        else:
            return float("-inf")  # Return negative infinity if no bids

    def check_position_limit(
        self, state: TradingState, product: str, additional_quantity: int
    ) -> bool:
        """Checks if placing additional_quantity of orders respects position limits."""
        current_position = state.position.get(product, 0)
        position_limit = self.position_limits.get(product, 0)
        return abs(current_position + additional_quantity) <= position_limit


# Sample usage
if __name__ == "__main__":
    # Create an instance of TutorialTrader
    trader = TutorialTrader()

    # Sample usage with a TradingState object
    # Create a TradingState object with mock data
    starfruit_order_depth = OrderDepth()
    starfruit_order_depth.sell_orders = {20: 8, 21: 4}
    starfruit_order_depth.buy_orders = {18: 3, 19: 6}

    order_depths = {"STARFRUIT": starfruit_order_depth}
    position = {"AMETHYSTS": 10, "STARFRUIT": -5}
    observations = Observation({}, {})
    market_trades = {
        "STARFRUIT": [Trade("STARFRUIT", 20, 8), Trade("STARFRUIT", 21, 4)]
    }
    trading_state = TradingState(
        "Mock Trader Data",
        1000,
        {},
        order_depths,
        {},
        market_trades,
        position,
        observations,
    )

    # Run the trading algorithm
    result, conversions, traderData = trader.run(trading_state)

    # Print the resulting orders
    for product, orders in result.items():
        print(f"Orders for {product}: {orders}")
