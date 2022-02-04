#!/usr/bin/env python
# coding: utf-8

# In[27]:


import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import sklearn
import math


# In[70]:


#PATH_PREDICTIONS = 'predictions_file.json'


# In[47]:


def read_data(path = PATH_PREDICTIONS):
    data = []
    for line in open(path, 'r'):
        result = json.loads(line)
        data.append(result)
        
    return data


# In[68]:


#Filtering sligtly improves results. It filters data at the beginning
#(First 10 estimates where LR does not have sufficient data) and where 
#R2 is low (where data points are too variable).

#1. for the first 10 bids predictions read pred = last order
#2. after 10th order: look at R2. If R2< 0.5, pred15s = last order
#3. Later try pred15s = (pred15s*R2 + Last_order*(1-R2)) ? 

def filter_results(dataset):
    
    for i in range(len(dataset)):
        if i < 10:
            dataset[i]['Pred15s'] = dataset[i]['Last order']
        elif data1[i]['R2'] < 0.5:
            dataset[i]['Pred15s'] = dataset[i]['Last order']
    return dataset

#RMSE Calculation:
def get_rmse_pred(json_text):
    
    actual15s = [i["Last order"] for i in json_text][1:]
    predicted15s = [i["Pred15s"] for i in json_text][:-1]
        
    mse_pred15s = sklearn.metrics.mean_squared_error(actual15s, predicted15s)
    n= len(json_text)
    rmse_pred15s = math.sqrt(mse_pred15s/n)
    
    return rmse_pred15s#, rmse_same15s 

#RMSE Calculation if predictions were made by taking the last actual order 
# without any LR calculations (assume order will be the same as the last one)
def get_rmse_same(json_text):
    
    actual15s = [i["Last order"] for i in json_text][1:]
    same15s = [i["Last order"] for i in json_text][:-1]
        
    mse_same15s = sklearn.metrics.mean_squared_error(actual15s, same15s)
    n= len(json_text)
    rmse_same15s = math.sqrt(mse_same15s/n)
    
    return rmse_same15s#, rmse_same15s 


def plot_asks(data):
    asks = [i["Last order"] for i in data if i["Order type"]=="asks"] 
    pred15s_asks = [i["Pred15s"] for i in data if i["Order type"]=="asks"]
    
    plt.plot(asks, label="Asks")
    plt.plot(pred15s_asks, label = "Asks Pred15s")
    first_time = data[0]['Last Order time']
    end_time = data[-1]['Last Order time']
    title = "Time of plot: " + first_time + "-" + end_time
    plt.title(title)
    plt.legend()
    plt.show()  

def plot_bids(data):
    bids = [i["Last order"] for i in data if i["Order type"]=="bids"] 
    pred15s_bids = [i["Pred15s"] for i in data if i["Order type"]=="bids"]
    plt.plot(bids, label = "Bids")
    plt.plot(pred15s_bids, label = "Bids Pred15s")
    first_time = data[0]['Last Order time']
    end_time = data[-1]['Last Order time']
    title = "Time of plot: " + first_time + "-" + end_time
    plt.title(title)
    plt.legend()
    plt.show()  
    


# In[ ]:





# In[69]:


data = read_data()
print(len(data))
print(get_rmse_pred(data))
print(get_rmse_same(data))

plot_asks(data)
plot_bids(data)

