from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np
mid_banana = [5000] #high score 776
mid_pearl = [] #high score 591

class Trader:
    profit = 0
    limit = 20
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        # Initialize the method output dict as an empty dict
        result = {}
        pearl_position = state.position.get('PEARLS', 0)
        banana_position = state.position.get('BANANAS', 0)
        for product in state.order_depths.keys():
            """if product == 'PEARLS':
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                acceptable_price = 10000
                if len(order_depth.sell_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    if best_ask < acceptable_price and abs(pearl_position -best_ask_volume) <= Trader.limit:
                        Trader.profit += best_ask_volume * best_ask
                        orders.append(Order(product, best_ask, -best_ask_volume))
                        pearl_position -= best_ask_volume
                        print("BUY", str(-best_ask_volume) + "x", best_ask, 'pearl_positions:',pearl_position, 'balance:',Trader.profit,'profit:',Trader.profit+pearl_position*10000+banana_position*mid_banana[-1])


                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > acceptable_price and abs(pearl_position - best_bid_volume) <= Trader.limit:
                        Trader.profit += best_bid_volume * best_bid
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        pearl_position -= best_bid_volume
                        print("SELL", str(best_bid_volume) + "x", best_bid, 'pearl_positions:',pearl_position,'balance:',Trader.profit, 'profit:',Trader.profit+pearl_position*10000+banana_position*mid_banana[-1])


                result[product] = orders"""

            if product == 'BANANAS':
                order_depth: OrderDepth = state.order_depths[product]
                if len(order_depth.sell_orders) > 0 and len(order_depth.buy_orders) > 0:
                    mid_banana.append((max(order_depth.buy_orders.keys())+min(order_depth.sell_orders.keys()))/2)
                orders: list[Order] = []
                avg_window = 5
                acceptable_price = sum(mid_banana[-avg_window:])/len(mid_banana[-avg_window:])
                position = state.position.get(product, 0)
                std = 7.95 #needs change
                factor = 0

                if len(order_depth.sell_orders) > 0:

                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    if best_ask < acceptable_price-std*factor and abs(banana_position - best_ask_volume) <= Trader.limit:
                        Trader.profit += best_ask_volume * best_ask
                        orders.append(Order(product, best_ask, -best_ask_volume))
                        banana_position -= best_ask_volume
                        print("BUY", str(-best_ask_volume) + "x", best_ask,'current_market',mid_banana[-1],'banana_positions:',banana_position,'balance:',Trader.profit, 'profit:',Trader.profit+pearl_position*10000+banana_position*mid_banana[-1])

                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > acceptable_price+std*factor and abs(banana_position - best_bid_volume) <= Trader.limit:
                        Trader.profit += best_bid_volume * best_bid
                        banana_position -= best_bid_volume
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        print("SELL", str(best_bid_volume) + "x", best_bid,'current_market',mid_banana[-1],'banana_positions:',banana_position,'balance:',Trader.profit, 'profit:',Trader.profit+pearl_position*10000+banana_position*mid_banana[-1])


                result[product] = orders
        return result