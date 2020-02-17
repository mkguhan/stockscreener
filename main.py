# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 20:45:45 2020

@author: @guhankumar
"""
 
import pandas as pd
import backtrader as bt

scripts = ["ADANIPORTS", "BHARTIARTL","UPL", "AXISBANK", "HDFC", "ASIANPAINTS","HINDUNILVR", "TITAN"]

def get_historical_data(script):
    alpha_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=NSE:{}&interval=15min&apikey=FIKNV2QYP8FRIOPF&outputsize=full&datatype=csv".format(script)
    hist_df = pd.read_csv(alpha_url, parse_dates=True)
    hist_df['date'] = pd.to_datetime(hist_df['timestamp'])
    hist_df['datetime'] = hist_df['date'].dt.tz_localize('US/Eastern').dt.tz_convert('Asia/Kolkata')
    hist_df['datetime'] = hist_df['datetime'].dt.tz_localize(tz=None)
    hist_df.drop(['timestamp','date'], axis=1, inplace=True)
    hist_df['date'] = hist_df['datetime']
    hist_df.set_index('date', inplace=True)
    return hist_df

def is_shooting_star(data):
    open = data[0]
    close = data[3]
    high = data[1]
    low = data[2] 
    time = data[4]
    #print("Open: {} High {} Low {} Close{} Time {}".format(open,high,low,close, time))
    #Lower Wick Calculation
    lower_wick = low - open
    #Upper Wick Calculation
    upper_wick = high - close
    #Body Calculation
    Body = close - open
    if open <= low and open < close and (lower_wick == 0 or lower_wick < (int(.25/100) * open)) and upper_wick > (1.25 * Body):
        return True
    else:
        return False
     
    


if __name__ == "__main__" :
        scripts = ["ADANIPORTS", "BHARTIARTL","UPL", "AXISBANK", "HDFC", "ASIANPAINT","HINDUNILVR", "TITAN"]
        print("Processing the Data......")
        for script in scripts:
            print("Stock : {}".format(script))
            data = get_historical_data(script)
            df = data[(data['datetime'] > '2020-02-07')]
            data_915=[df.iloc[-1]['open'],df.iloc[-1]['high'],df.iloc[-1]['low'],df.iloc[-1]['close'],df.iloc[-1]['datetime']]
            print(is_shooting_star(data_915))
            df_daily=daily_data(script)