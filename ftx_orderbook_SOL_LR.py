#!/usr/bin/env python
# coding: utf-8

# This python script performs a simple Simple Linear Regression analysis on FTX market solana (SOL/USD) price. Orders on FTX market consist on bids and asks. My code separates them and does a price prediction 15s, 30s and 1 min in a future. 
# QC analysis comparing results to 'no regression' or simple assumption that the price will stay the same as the last order was preformed. Unsurprisingly, considering how variable cryptocurrency prices are, LR did not perform much better.

# In[14]:


import requests
import json
from time import sleep
import datetime
from datetime import date
import matplotlib.pyplot as plt
import numpy as np


# In[15]:


LIMIT = 10       # How many data points to use for LR estimate and predictions
market_name = 'SOL/USD'
depth = 20
interval = 15    # Time interval between API requests
URL = f'https://ftx.com/api/markets/{market_name}/orderbook?depth={depth}'


# In[18]:


def request(url = URL):
    order= []

    book = requests.get(url).json()
    #filter out any empty data (if any):
    if book:
        orderbook_results = book['result']
        orderbook_results['time'] = str(datetime.datetime.utcnow())
        order.append(orderbook_results)
        sleep(interval)    
    return order


def update_dataset(dataset):
    datasize = len(dataset)
    #Case 1: filling up dataset at the beginning (starting program)
    if datasize == 1: 
        full_chunk = []
        full_chunk.append(dataset)
        while datasize< LIMIT:
            new_order = request()
            full_chunk.append(new_order)
            datasize+=1
        return full_chunk
    # After it was initialized: updating dataset
    else:
        new_order = request()
        dataset.append(new_order)
        new_chunk = dataset[1:]
        return new_chunk

    
def separate_orders(dataset):
    bids = []
    asks = []
    times = []
    for order in dataset:
        bids.append(order[0]['bids'])
        asks.append(order[0]['asks'])
        times.append(order[0]['time'])
        # returning one record only
        
    wasks = weighted_price(asks)
    wbids = weighted_price(bids)

    return wasks, wbids, times


def weighted_price(orders):
    weighted_orders = []

    for order in orders:
        s = np.sum(np.prod(order, axis = 1))   #multiply price by order size then sum to get total
        w = np.sum(order, axis = 0)[1]         #weights, order size
        weighted_orders.append(round(s/w, 4))
    return weighted_orders


def LR_estimation(order, order_type, times):

    X = np.array(list(range(0, len(order)))).reshape(-1, 1)
    Y = np.array(order).reshape(-1, 1)                       # take all order that is a small chunk 20x15s = 3min ?
    end = len(order)
    reg = linear_model.LinearRegression()
    reg_fit = reg.fit(X, Y)
    R2 = reg_fit.score(X, Y) 
    coef = reg_fit.coef_
    intercept = reg_fit.intercept_
    #Predict 15s, 30s and 1 minute in the future
    pred15s = reg_fit.predict(np.array(end+1).reshape(-1, 1))[0][0] ## predicting 1*15s = 15s in the future
    pred30s = reg_fit.predict(np.array(end+2).reshape(-1, 1))[0][0] ## predicting 2*15s = 30s in the future
    pred60s = reg_fit.predict(np.array(end+4).reshape(-1, 1))[0][0] ## predicting 4*15s = 1 minute in the future        
    #pred = [prediction15s, prediction30s, prediction60s]
    last_time = times[-1]
    print("LR Estimate for {} at {} :\n R2={}, coef={}, intercept={},\n".format(order_type,             last_time, round(R2, 2), round(coef[0][0], 2), round(intercept[0], 2))) 
    print("Predictions for 15s= {}, 30s= {} and 1 min= {}".format(round(pred15s, 5), round(pred30s, 5), round(pred60s, 5)))
    
    
    timenow = str(datetime.datetime.utcnow())
    print("Time: ", timenow)
    #estimates = [order_type, order, R2, coef[0][0], intercept[0], pred, timenow]
    get_accuracy(order_type, order[-1], R2, coef[0][0], intercept[0], pred15s, pred30s, pred60s, last_time, timenow)
    
    plot_orderbook(order, order_type, timenow)
    
    return  [R2, coef[0][0], intercept[0]], pred15s, pred30s, pred60s 

    
#Execute this function to run continuously:
def run_orderbook():
    first_request = request()
    dataset = update_dataset(first_request)  ## Filling up orderbook for LR Regression
    while True:
        orders = separate_orders(dataset)
        #Do Linear Regression - ASKS
        asks = orders[0]
        times = orders[2]
        order_type = 'asks'
        lr_estimate_asks = LR_estimation(asks, order_type, times)
        
        #Do Linear Regression - BIDS
        bids = orders[1]
        order_type = 'bids'
        lr_estimate_bids = LR_estimation(bids, order_type, times)

        #plot_orderbook(dataset)  #Optionally can plot a new graph with asks and bids every 15s
    
        ## Update dataset with a new request:    
        dataset = update_dataset(dataset)    

#-------------------------------------------------------------------------------
#Global path to write results:
PATH_PREDICTIONS = 'predictions_file.json'

#This function is called in LR_estimation function to write results into a file:
def get_accuracy(order_type, lastorder, R2, coef, intercept, pred15s, pred30s, pred60s, last_time, timenow):
    
    line = {"Order type": order_type, "Last order": lastorder, "R2": R2, "Coefficient": coef, "Intercep": intercept, "Pred15s": pred15s, "Pred30s": pred30s, "Pred60s": pred60s, "Last Order time": last_time, "Timenow": timenow}
    
    with open(PATH_PREDICTIONS, 'a', newline='') as file:
        file.write(json.dumps(line) + '\n')


def plot_orderbook(dataset, data_type, timenow):
    
    plt.plot(dataset, label=data_type)    
    plottitle = "Time of plot: " + timenow
    plt.title(plottitle)
    plt.legend()
    plt.show()  
        


# In[17]:


run_orderbook()

