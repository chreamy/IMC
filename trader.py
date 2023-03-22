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
                orders: list[Order] = []
                asks = []
                bids = []
                spread = min(order_depth.sell_orders.keys()) - max(order_depth.buy_orders.keys())
                while len(order_depth.sell_orders) > 0:
                    asks.append({'price': min(order_depth.sell_orders.keys()),
                                'vol': order_depth.sell_orders[min(order_depth.sell_orders.keys())]})
                    del order_depth.sell_orders[min(order_depth.sell_orders.keys())]
                while len(order_depth.buy_orders) != 0:
                    bids.append({'price': max(order_depth.buy_orders.keys()),
                                'vol': order_depth.buy_orders[max(order_depth.buy_orders.keys())]})
                    del order_depth.buy_orders[max(order_depth.buy_orders.keys())]
                avg_window = 5
                acceptable_price = np.mean(mid_banana[-avg_window:])
                a10 = np.mean(mid_banana[-50:])
                a100 = np.mean(mid_banana[-200:])
                std = np.std(mid_banana[-avg_window:])
                buy = (a10 - a100) >0
                if buy:
                    print('buy')
                else:
                    print('sell')
                factor = int(0.5*spread)
                if state.timestamp<600:
                    break
                if asks[0]['price'] < acceptable_price or (asks[0]['price'] == acceptable_price and banana_position < -2):
                    if banana_position - asks[0]['vol'] > Trader.limit:
                        asks[0]['vol'] = -(Trader.limit - banana_position)
                        print('missed full trade')
                    orders.append(Order(product, asks[0]['price'], -asks[0]['vol']))
                    banana_position -= asks[0]['vol']
                    print("BUY", str(-asks[0]['vol']) + "x", asks[0]['price'], 'banana_positions:',banana_position)
                elif bids[0]['price'] > acceptable_price or (bids[0]['price'] == acceptable_price and banana_position > -5):
                    if banana_position - bids[0]['vol'] < -Trader.limit:
                        bids[0]['vol'] = banana_position + Trader.limit
                        print('missed full trade')
                    orders.append(Order(product, bids[0]['price'], -bids[0]['vol']))
                    banana_position -= bids[0]['vol']
                    print("SELL", str(bids[0]['vol']) + "x", bids[0]['price'], 'banana_positions:',
                        banana_position)
                elif banana_position > 15:
                    orders.append(Order(product, acceptable_price+factor/2, -10))
                elif banana_position < -15:
                    orders.append(Order(product, acceptable_price-factor/2, 10))
                elif banana_position > 0:
                    # orders.append(Order(product, 10002, -(Trader.limit-pearl_position)))
                    orders.append(Order(product, acceptable_price+factor, -10))
                    orders.append(Order(product, acceptable_price-factor, 5))
                else:
                    orders.append(Order(product, acceptable_price+factor, -5))
                    orders.append(Order(product, acceptable_price-factor, 10))
                result[product] = orders
        return result