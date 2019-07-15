# This algorithm uses the talib Bollinger Bands function to determine entry entry 
# points for long and short positions.



import talib
import numpy as np
import pandas as pd
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.factors import CustomFactor

# From https://www.quantopian.com/data/quandl/bundesbank_bbk01_wt5511
# Data available from 01 Apr 1968 - Ongoing
from quantopian.pipeline.data.quandl import bundesbank_bbk01_wt5511 as gold
class Gold(CustomFactor):
    inputs = [gold.value]
    window_length = 1

    def compute(self, today, assets, out, gold):
        out[:] = gold
def initialize(context):
    # SPY
    context.spy = sid(8554)
    context.gold=[]
    pipe = Pipeline()
    pipe.add(Gold(), 'gold')
    attach_pipeline(pipe, 'gold')
    #que haga el rebalanceo de cada dia
    schedule_function(rebalance, date_rules.every_day(), time_rules.market_open())

# Rebalance daily.
def rebalance(context, data):
    context.results = pipeline_output('gold')
    if len(context.gold)>0 :
        context.gold=[context.gold[-1]]
    context.gold.append(context.results['gold'].unique()[0])
 
    factor_inversion=0.9;
    if len(context.gold)>1 and context.gold[-1]>=context.gold[-2]:
        factor_inversion+=0.2
    elif len(context.gold)>1 :
        factor_inversion-=0.3
        
        
        
        
    
 
    #al multiplicar por 1/3 reduce el porcentaje de perdida
    current_position = context.portfolio.positions[context.spy].amount*0.333
    price=data.current(context.spy, 'price')
    
    # Load historical data for the stocks
    prices = data.history(context.spy, 'price', 15, '1d')
    
    upper, middle, lower = talib.BBANDS(
        prices, 
        timeperiod=10,
        # number of non-biased standard deviations from the mean
        nbdevup=2,
        nbdevdn=2,
        # Moving average type: simple moving average here
        matype=0)
    
    # If price is below the recent lower band and we have
    # no long positions then invest the entire
    # portfolio value into SPY
    if price <= lower[-1] and current_position <= 0 and data.can_trade(context.spy):
        order_target_percent(context.spy, factor_inversion)
    
    # If price is above the recent upper band and we have
    # no short positions then invest the entire
    # portfolio value to short SPY
    elif price >= upper[-1] and current_position >= 0 and data.can_trade(context.spy):
        order_target_percent(context.spy, -factor_inversion)
        
    record(upper=upper[-1],
           lower=lower[-1],
           mean=middle[-1],
           price=price,
           position_size=current_position)
