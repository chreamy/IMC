from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np
mid_banana = [5000] #high score 591
mid_pearl = [] #high score 852
class Trader:
    profit = 0
    limit = 19
    banana_bal = 0
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        # Initialize the method output dict as an empty dict
        result = {}

        pearl_position = state.position.get('PEARLS', 0)
        banana_position = state.position.get('BANANAS', 0)
        for product in state.order_depths.keys():
            if product == 'PEARLS':
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                acceptable_price = 10000
                while len(order_depth.sell_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    if pearl_position - best_ask_volume > Trader.limit:
                        best_ask_volume = -(Trader.limit-pearl_position) -1
                    if (best_ask < acceptable_price or (pearl_position<0and best_ask == acceptable_price)):
                        Trader.profit += best_ask_volume * best_ask
                        orders.append(Order(product, best_ask, -best_ask_volume))
                        pearl_position -= best_ask_volume
                        print("BUY", str(-best_ask_volume) + "x", best_ask, 'pearl_positions:',pearl_position, 'balance:',Trader.profit,'profit:',Trader.profit+pearl_position*10000+banana_position*mid_banana[-1])
                    del order_depth.sell_orders[best_ask]
                while len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if pearl_position - best_bid_volume < -Trader.limit:
                        best_bid_volume = (pearl_position+Trader.limit) +1
                    if (best_bid > acceptable_price or (pearl_position>0and best_bid == acceptable_price)):
                        Trader.profit += best_bid_volume * best_bid
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        pearl_position -= best_bid_volume
                        print("SELL", str(best_bid_volume) + "x", best_bid, 'pearl_positions:',pearl_position,'balance:',Trader.profit, 'profit:',Trader.profit+pearl_position*10000+banana_position*mid_banana[-1])
                    del order_depth.buy_orders[best_bid]
                result[product] = orders

            if product == 'BANANAS':
                order_depth: OrderDepth = state.order_depths[product]
                if len(order_depth.sell_orders) > 0 and len(order_depth.buy_orders) > 0:
                    mid_banana.append((max(order_depth.buy_orders.keys())+min(order_depth.sell_orders.keys()))/2)
                orders: list[Order] = []
                avg_window = 5
                acceptable_price = np.mean(mid_banana[-avg_window:])
                a50 = np.mean(mid_banana[-50:])
                a200 = np.mean(mid_banana[-200:])
                std = np.std(mid_banana[-avg_window:])
                trend_index = a50 - a200
                factor = 0.1
                acceptable_price += trend_index*factor
                print('factor',trend_index*factor)
                if trend_index>0:
                    hold = 2
                else:
                    hold = -2
                if state.timestamp<600:
                    break
                if banana_position != 0:
                    price = Trader.banana_bal/banana_position
                for best_ask in sorted(order_depth.sell_orders):
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    if best_ask_volume<-Trader.limit:
                        best_ask_volume=-Trader.limit
                    if banana_position - best_ask_volume > Trader.limit:
                        best_ask_volume = -(Trader.limit - banana_position) - 1
                    if ((best_ask < acceptable_price) or (banana_position <-15 and best_ask < price)):
                        Trader.profit += best_ask_volume * best_ask
                        Trader.banana_bal += best_ask_volume * best_ask
                        orders.append(Order(product, best_ask, -best_ask_volume))
                        banana_position -= best_ask_volume
                        print("BUY", str(-best_ask_volume) + "x", best_ask,'current_market',mid_banana[-1],'banana_positions:',banana_position,'balance:',Trader.profit, 'profit:',Trader.profit+pearl_position*10000+banana_position*mid_banana[-1],'std:',std)
                    else:
                        break
                    order_depth.sell_orders[best_ask]
                for best_bid in sorted(order_depth.buy_orders, reverse=True):
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid_volume>Trader.limit:
                        best_bid_volume=Trader.limit
                    if banana_position - best_bid_volume < -Trader.limit:
                        best_bid_volume = (banana_position + Trader.limit) + 1
                    if ((best_bid > acceptable_price) or (banana_position>15 and best_bid > price)):
                        Trader.profit += best_bid_volume * best_bid
                        Trader.banana_bal += best_bid_volume * best_bid
                        banana_position -= best_bid_volume
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        print("SELL", str(best_bid_volume) + "x", best_bid,'current_market',mid_banana[-1],'banana_positions:',banana_position,'balance:',Trader.profit, 'profit:',Trader.profit+pearl_position*10000+banana_position*mid_banana[-1],'std:',std)
                    else:
                        break
                    order_depth.buy_orders.pop(best_bid)

                result[product] = orders
        return result