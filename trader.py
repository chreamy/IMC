from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np
mid_banana = [5000] #high score 591
mid_pearl = [] #high score 852
class Trader:
    profit = 0
    limit = 20
    banana_bal = 0
    ema = 5000
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        # Initialize the method output dict as an empty dict
        result = {}
        pearl_position = state.position.get('PEARLS', 0)
        banana_position = state.position.get('BANANAS', 0)
        for product in state.order_depths.keys():
            for product in state.order_depths.keys():
                if product == 'PEARLS':
                    order_depth: OrderDepth = state.order_depths[product]
                    orders: list[Order] = []
                    asks = []
                    bids = []
                    while len(order_depth.sell_orders) > 0:
                        asks.append({'price': min(order_depth.sell_orders.keys()),
                                     'vol': order_depth.sell_orders[min(order_depth.sell_orders.keys())]})
                        del order_depth.sell_orders[min(order_depth.sell_orders.keys())]
                    while len(order_depth.buy_orders) != 0:
                        bids.append({'price': max(order_depth.buy_orders.keys()),
                                     'vol': order_depth.buy_orders[max(order_depth.buy_orders.keys())]})
                        del order_depth.buy_orders[max(order_depth.buy_orders.keys())]
                    if len(asks) != 0:
                        if asks[0]['price'] < 10000 or (asks[0]['price'] == 10000 and pearl_position < -2):
                            if pearl_position - asks[0]['vol'] > Trader.limit:
                                asks[0]['vol'] = -(Trader.limit - pearl_position)
                                print('missed full trade')
                            orders.append(Order(product, asks[0]['price'], -asks[0]['vol']))
                            pearl_position -= asks[0]['vol']
                            print("BUY", str(-asks[0]['vol']) + "x", asks[0]['price'], 'pearl_positions:',
                                  pearl_position)
                        elif bids[0]['price'] > 10000 or (bids[0]['price'] == 10000 and pearl_position > -5):
                            if pearl_position - bids[0]['vol'] < -Trader.limit:
                                bids[0]['vol'] = pearl_position + Trader.limit
                                print('missed full trade')
                            orders.append(Order(product, bids[0]['price'], -bids[0]['vol']))
                            pearl_position -= bids[0]['vol']
                            print("SELL", str(bids[0]['vol']) + "x", bids[0]['price'], 'pearl_positions:',
                                  pearl_position)
                        elif pearl_position > 15:
                            orders.append(Order(product, 10002, -10))
                        elif pearl_position < -15:
                            orders.append(Order(product, 9998, 10))
                        elif pearl_position > 0:
                            # orders.append(Order(product, 10002, -(Trader.limit-pearl_position)))
                            orders.append(Order(product, 10004, -10))
                            orders.append(Order(product, 9996, 5))
                        else:
                            orders.append(Order(product, 10004, -5))
                            orders.append(Order(product, 9996, 10))
                            # orders.append(Order(product, 9998, pearl_position + Trader.limit))

                        print(pearl_position)
                    result[product] = orders

            if product == 'BANANAS':
                order_depth: OrderDepth = state.order_depths[product]
                if len(order_depth.sell_orders) > 0 and len(order_depth.buy_orders) > 0:
                    mid_banana.append((max(order_depth.buy_orders.keys())+min(order_depth.sell_orders.keys()))/2)
                #n = 10
                #Trader.ema = Trader.ema + (2 / n + 1) * (mid_banana[-1] - Trader.ema)
                orders: list[Order] = []
                avg_window = 5
                acceptable_price = np.mean(mid_banana[-avg_window:])
                a10 = np.mean(mid_banana[-50:])
                a100 = np.mean(mid_banana[-200:])
                std = np.std(mid_banana[-avg_window:])
                price = acceptable_price
                spread = min(order_depth.sell_orders.keys())-max(order_depth.buy_orders.keys())
                buy = (a10 - a100) >0
                if buy:
                    print('buy')
                else:
                    print('sell')
                factor = -0*spread
                buffer = 0
                if state.timestamp<600:
                    break
                if banana_position != 0:
                    price = Trader.banana_bal/banana_position
                for best_ask in sorted(order_depth.sell_orders):
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    if best_ask_volume<-Trader.limit:
                        best_ask_volume=-Trader.limit
                    if banana_position - best_ask_volume > Trader.limit:
                        best_ask_volume = -(Trader.limit - banana_position)
                    if (best_ask < acceptable_price+buffer) or (banana_position <-15 and best_ask < price) or (best_ask < acceptable_price+factor and buy):
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
                        best_bid_volume = (banana_position + Trader.limit)
                    if (best_bid > acceptable_price-buffer) or (banana_position>15 and best_bid > price) or (best_bid > acceptable_price-factor and not buy):
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