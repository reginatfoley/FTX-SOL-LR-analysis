# FTX-SOL-LR-analysis
This python script performs a simple Simple Linear Regression analysis on FTX market solana (SOL/USD) price. 
Motivation was to see if LR would perform better than publicly available simple extrapolation tools. Orders on FTX market consist on bids and asks. 
My code separates them and does a price prediction 15s, 30s and 1 min in a future. QC analysis comparing results to 'no regression' or simple assumption 
that the price will stay the same as the last order was preformed. Not too surprisingly, considering how variable cryptocurrency prices are, LR did not 
perform much better than publicly available tools. 
