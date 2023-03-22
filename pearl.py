from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np
mid_pearl = [] #high score 852
class Trader:
    limit = 20
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        # Initialize the method output dict as an empty dict
        result = {}
        pearl_position = state.position.get('PEARLS', 0)
        for product in state.order_depths.keys():
            if product == 'PEARLS':
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                asks = []
                bids = []
                while len(order_depth.sell_orders) > 0:
                    asks.append({'price':min(order_depth.sell_orders.keys()),'vol':order_depth.sell_orders[min(order_depth.sell_orders.keys())]})
                    del order_depth.sell_orders[min(order_depth.sell_orders.keys())]
                while len(order_depth.buy_orders) != 0:
                    bids.append({'price':max(order_depth.buy_orders.keys()),'vol':order_depth.buy_orders[max(order_depth.buy_orders.keys())]})
                    del order_depth.buy_orders[max(order_depth.buy_orders.keys())]
                if len(asks) != 0:
                    if asks[0]['price'] < 10000 or (asks[0]['price'] == 10000 and pearl_position<-2):
                        if pearl_position - asks[0]['vol'] > Trader.limit:
                            asks[0]['vol'] = -(Trader.limit-pearl_position)
                            print('missed full trade')
                        orders.append(Order(product, asks[0]['price'], -asks[0]['vol']))
                        pearl_position -= asks[0]['vol']
                        print("BUY", str(-asks[0]['vol']) + "x", asks[0]['price'], 'pearl_positions:', pearl_position)
                    elif bids[0]['price'] > 10000 or (bids[0]['price'] == 10000 and pearl_position>-5):
                        if pearl_position - bids[0]['vol'] < -Trader.limit:
                            bids[0]['vol'] = pearl_position + Trader.limit
                            print('missed full trade')
                        orders.append(Order(product, bids[0]['price'], -bids[0]['vol']))
                        pearl_position -= bids[0]['vol']
                        print("SELL", str(bids[0]['vol']) + "x", bids[0]['price'], 'pearl_positions:', pearl_position)
                    elif pearl_position > 15:
                        orders.append(Order(product, 10002, -10))
                    elif pearl_position < -15:
                        orders.append(Order(product, 9998, 10))
                    elif pearl_position>0:
                        #orders.append(Order(product, 10002, -(Trader.limit-pearl_position)))
                        orders.append(Order(product, 10004, -10))
                        orders.append(Order(product, 9996, 5))
                    else:
                        orders.append(Order(product, 10004, -5))
                        orders.append(Order(product, 9996, 10))
                        #orders.append(Order(product, 9998, pearl_position + Trader.limit))


                    print(pearl_position)
                result[product] = orders

        return result