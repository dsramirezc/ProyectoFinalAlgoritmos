# This initialize function sets any data or variables that you'll use in
# your algorithm.
def initialize(context):
    context.stock = symbol('BA')  # Boeing
    context.registro_precios=[]
    # Since record() only works on a daily resolution, record our price at the end
    # of each day.
    schedule_function(record_vars,
                      date_rule=date_rules.every_day(),
                      time_rule=time_rules.market_close(hours=1))
    
def CalcularPendientePrecios(arr):
    if len(arr)<12:
        return 400;
    primeros_dias=arr[-10:-5]
    ultimos_dias=arr[-5::]
    suma1=0
    suma2=0
    for i in primeros_dias:
        suma1+=i
    for i in ultimos_dias:
        suma2+=i
    suma1/=len(primeros_dias)
    suma2/=len(ultimos_dias)
    if suma2<suma1:
        return 0
    else:
        return 550
# Now we get into the meat of the algorithm. 
def record_vars(context, data):
    # Create a variable for the price of the Boeing stock
    context.price = data.current(context.stock, 'price')
    #variables para calcualr cuando invertir
    
    context.registro_precios.append(context.price)
  
    cantidad_a_invertir=CalcularPendientePrecios(context.registro_precios)
    # Create variables to track the short and long moving averages. 
    # The short moving average tracks over 20 days and the long moving average
    # tracks over 80 days. 
    price_history = data.history(context.stock, 'price', 80, '1d')
    short_mavg = price_history[-20:].mean()
    long_mavg = price_history.mean()

    # If the short moving average is higher than the long moving average, then 
    # we want our portfolio to hold 500 stocks of Boeing
    if (short_mavg > long_mavg ):
        order_target(context.stock, +cantidad_a_invertir)
    else :
        order_target(context.stock, 0)

    # Record our variables to see the algo behavior. You can record up to 
    # 5 custom variables. Series can be toggled on and off in the plot by
    # clicking on labeles in the legend. 
    record(short_mavg = short_mavg,
        long_mavg = long_mavg,
        goog_price = context.price)
