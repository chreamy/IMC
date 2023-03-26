from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order, ProsperityEncoder, Symbol
import numpy as np
from typing import Any
import json

class Logger:
    def __init__(self) -> None:
        self.logs = ""

    def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
        self.logs += sep.join(map(str, objects)) + end

    def flush(self, state: TradingState, orders: dict[Symbol, list[Order]]) -> None:
        print(json.dumps({
            "state": state,
            "orders": orders,
            "logs": self.logs,
        }, cls=ProsperityEncoder, separators=(",", ":"), sort_keys=True))

        self.logs = ""

logger = Logger()

mid_banana =    [] #high score 591
mid_pearl =     [] #high score 852
mid_coco =      []
mid_pina =      []
ratio = []
mid_diving= []
ratio_diving = []

class Trader:
    profit = 0
    limit = 20
    coco_limit = 600
    pina_limit = 300
    diving_limit = 50
    # limit = {"PEARLS": 20, "BANANAS": 20, "COCONUTS": 600, "PINA_COLADAS": 300}
    banana_bal = 0
    ema = 5000
    last_trend = 0
    last_trend_pina = 0
    crits = [{'price': 8000, 'state': 'none'}]
    crits_pina = [{'price': 15000, 'state': 'none'}]
    

    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
##############################################################################################################################
        #GET POSITIONS
        result = {}
        pearl_position = state.position.get('PEARLS', 0)
        banana_position = state.position.get('BANANAS', 0)
        coco_position = state.position.get('COCONUTS', 0)
        pina_position = state.position.get('PINA_COLADAS', 0)
        berry_position = state.position.get('BERRIES', 0)
        diving_position = state.position.get('DIVING_GEAR', 0)
        for product in state.order_depths.keys():
###############################################################################################################################            
            # PEARLS HERE
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
##############################################################################################################################
            # BANANAS HERE
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
                factor = int(0.1*spread)
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
                elif banana_position > 0:
                    # orders.append(Order(product, 10002, -(Trader.limit-pearl_position)))
                    orders.append(Order(product, acceptable_price+factor, -18))
                    orders.append(Order(product, acceptable_price-factor, 9))
                else:
                    orders.append(Order(product, acceptable_price+factor, -9))
                    orders.append(Order(product, acceptable_price-factor, 18))
                result[product] = orders
##############################################################################################################################
            #DIVING GEAR HERE
            if product == 'DIVING_GEAR':
                order_depth_diving: OrderDepth = state.order_depths['DIVING_GEAR']
                if len(order_depth_diving.sell_orders) > 0 and len(order_depth_diving.buy_orders) > 0:
                    mid_diving.append((max(order_depth_diving.buy_orders.keys()) + min(order_depth_diving.sell_orders.keys())) / 2)

                dolphin_sighting = state.observations['DOLPHIN_SIGHTINGS']
                orders_diving: list[Order] = []

                asks = []
                bids = []
                spread = min(order_depth_diving.sell_orders.keys()) - max(order_depth_diving.buy_orders.keys())
                while len(order_depth_diving.sell_orders) > 0:
                    asks.append({'price': min(order_depth_diving.sell_orders.keys()),
                                 'vol': order_depth_diving.sell_orders[min(order_depth_diving.sell_orders.keys())]})
                    del order_depth_diving.sell_orders[min(order_depth_diving.sell_orders.keys())]
                while len(order_depth_diving.buy_orders) != 0:
                    bids.append({'price': max(order_depth_diving.buy_orders.keys()),
                                 'vol': order_depth_diving.buy_orders[max(order_depth_diving.buy_orders.keys())]})
                    del order_depth_diving.buy_orders[max(order_depth_diving.buy_orders.keys())]

                best_ask_volume_diving = asks[0]['vol']
                best_ask_diving = asks[0]['price']
                sellable_volume_diving = Trader.diving_limit + diving_position
                best_bid_volume_diving = bids[0]['vol']
                best_bid_diving = bids[0]['price']
                buyable_volume_diving = 50 - diving_position

                window_diving = 60
                ratio_diving.append(mid_diving[-1] / dolphin_sighting)
                ratio_zscore_diving = (np.mean(ratio_diving[-1:]) - np.mean(ratio_diving[-window_diving:])) / np.std(
                    ratio_diving[-window_diving:])
                zscore_diving = (np.mean(mid_diving[-1:]) - np.mean(mid_diving[-window_diving:])) / np.std(
                    mid_diving[-window_diving:])
                current_diving_ratio = ratio_diving[-1]
                if ratio_zscore_diving > 1.25 and zscore_diving > 1.25:
                    #  Sell diving

                    volume_diving_sell = min(best_bid_volume_diving, sellable_volume_diving)
                    orders_diving.append(Order('DIVING_GEAR', best_bid_diving, -volume_diving_sell))

                    print("SELL DIVING", -volume_diving_sell, "x", best_ask_diving)
                if ratio_zscore_diving < -1.25 and zscore_diving < -1.25:
                    # Buy divinng

                    volume_diving_buy = min(-best_ask_volume_diving, buyable_volume_diving)
                    orders_diving.append(Order('DIVING_GEAR', best_ask_diving, volume_diving_buy))
                    print("BUY DIVINNG", volume_diving_buy, "x", best_bid_diving)

                result['DIVING_GEAR'] = orders_diving
#############################################################################################################################
            # COCONUTS AND PINA PAIR TRADING HERE
        order_depth_coco: OrderDepth = state.order_depths['COCONUTS']
        if len(order_depth_coco.sell_orders) > 0 and len(order_depth_coco.buy_orders) > 0:
            mid_coco.append((max(order_depth_coco.buy_orders.keys()) + min(order_depth_coco.sell_orders.keys())) / 2)
        order_depth_pina: OrderDepth = state.order_depths['PINA_COLADAS']
        if len(order_depth_pina.sell_orders) > 0 and len(order_depth_pina.buy_orders) > 0:
            mid_pina.append((max(order_depth_pina.buy_orders.keys()) + min(order_depth_pina.sell_orders.keys())) / 2)
        orders_coco: list[Order] = []
        orders_pina: list[Order] = []
        asks = [] #for coconut
        bids = [] #for coconut
        asks_pina = []
        bids_pina = []
        while len(order_depth_coco.sell_orders) > 0: #get coco order data
            asks.append({'price': min(order_depth_coco.sell_orders.keys()),
                         'vol': order_depth_coco.sell_orders[min(order_depth_coco.sell_orders.keys())]})
            del order_depth_coco.sell_orders[min(order_depth_coco.sell_orders.keys())]
        while len(order_depth_coco.buy_orders) != 0:
            bids.append({'price': max(order_depth_coco.buy_orders.keys()),
                         'vol': order_depth_coco.buy_orders[max(order_depth_coco.buy_orders.keys())]})
            del order_depth_coco.buy_orders[max(order_depth_coco.buy_orders.keys())]
        while len(order_depth_pina.sell_orders) > 0: #get pina order data
            asks_pina.append({'price': min(order_depth_pina.sell_orders.keys()),
                         'vol': order_depth_pina.sell_orders[min(order_depth_pina.sell_orders.keys())]})
            del order_depth_pina.sell_orders[min(order_depth_pina.sell_orders.keys())]
        while len(order_depth_pina.buy_orders) != 0:
            bids_pina.append({'price': max(order_depth_pina.buy_orders.keys()),
                         'vol': order_depth_pina.buy_orders[max(order_depth_pina.buy_orders.keys())]})
            del order_depth_pina.buy_orders[max(order_depth_pina.buy_orders.keys())]
        best_ask_volume_coconut = asks[0]['vol'];best_ask_coconut = asks[0]['price'];sellable_volume_coconut = 600 +coco_position;best_bid_volume_pina = bids_pina[0]['vol'];best_bid_pina = bids_pina[0]['price'];buyable_volume_pina = 300 -pina_position;best_bid_volume_coconut = bids[0]['vol'];best_ask_volume_pina = asks_pina[0]['vol'];buyable_volume_coconut = 600 -coco_position;sellable_volume_pina = 300 +pina_position;best_bid_coconut = bids[0]['price'];best_ask_pina = asks_pina[0]['price']
        window = 50
        zfactor = 1.6
        ratio.append(mid_coco[-1] / np.mean(mid_pina[-5:])) #history of ratios
        zscore = (np.mean(ratio[-1:]) - np.mean(ratio[-window:])) / np.std(ratio[-window:]) #ratio zscore
        cocozscore = (np.mean(mid_coco[-1:]) - np.mean(mid_coco[-window:])) / np.std(mid_coco[-window:])
        pinazscore = (np.mean(mid_pina[-1:]) - np.mean(mid_pina[-window:])) / np.std(mid_pina[-window:])
        print('Zscore', zscore, 'Ratio', ratio[-1])
        current_ratio = ratio[-1] #latest ratio
        print('cocopos',coco_position,'pinapos',pina_position,'sellablecoco',sellable_volume_coconut,'buyablecoco',buyable_volume_coconut)
        print(best_bid_volume_coconut,best_ask_volume_pina)
        if zscore > zfactor:
            #Coco Value > Pina
            #Sell Coco, Buy Pina
            max_coconut_sell = min(best_bid_volume_coconut, sellable_volume_coconut)
            max_pina_buy = min(-best_ask_volume_pina, buyable_volume_pina)
            if max_coconut_sell > max_pina_buy / current_ratio:
                volume_coconut_sell = round(max_pina_buy / current_ratio)
                volume_pina_buy = max_pina_buy
            else:
                volume_coconut_sell = max_coconut_sell
                volume_pina_buy = round(max_coconut_sell * current_ratio)
            if cocozscore>zfactor:
                orders_coco.append(Order('COCONUTS', best_bid_coconut, -volume_coconut_sell))
            if pinazscore<-zfactor:
                orders_pina.append(Order('PINA_COLADAS', best_ask_pina, volume_pina_buy))
        elif zscore < -zfactor:
            # Pina Value > Coco
            # Sell pina, Buy coconut
            max_coconut_buy = min(-best_ask_volume_coconut, buyable_volume_coconut)
            max_pina_sell = min(best_bid_volume_pina, sellable_volume_pina)
            if max_coconut_buy > max_pina_sell / current_ratio:
                volume_coconut_buy = round(max_pina_sell / current_ratio)
                volume_pina_sell = max_pina_sell
            else:
                volume_coconut_buy = max_coconut_buy
                volume_pina_sell = round(max_coconut_buy * current_ratio)
            if cocozscore<-zfactor:
                orders_coco.append(Order('COCONUTS', best_ask_coconut, volume_coconut_buy))
            if pinazscore>zfactor:
                orders_pina.append(Order('PINA_COLADAS', best_bid_pina, -volume_pina_sell))
        result['COCONUTS'] = orders_coco
        result['PINA_COLADAS'] = orders_pina
##############################################################################################################################
        #BERRIES HERE (NEEDS UPDATE)
        orders_berry: list[Order] = []
        order_depth_berry: OrderDepth = state.order_depths['BERRIES']
        if 100000 < state.timestamp < 110000:
            orders_berry.append(Order('BERRIES', min(order_depth_berry.sell_orders.keys()), 250 -berry_position))
        if 500000 < state.timestamp < 510000:
            orders_berry.append(Order('BERRIES', max(order_depth_berry.buy_orders.keys()), -(250 +berry_position)))
        result['BERRIES'] = orders_berry
##############################################################################################################################
        #EXPORT
        logger.flush(state, orders)
        return result
    