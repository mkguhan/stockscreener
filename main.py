# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 20:45:45 2020

@author: Admin
"""

import pandas as pd
import backtrader as bt
scripts = ["ADANIPORTS", "BHARTIARTL","UPL", "AXISBANK", "HDFC", "ASIANPAINTS","HINDUNILVR", "TITAN"]
def get_historical_data(script):
    alpha_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=NSE:{}&interval=15min&apikey=FIKNV2QYP8FRIOPF&datatype=csv".format(script)
    hist_df = pd.read_csv(alpha_url, parse_dates=True)
    hist_df['date'] = pd.to_datetime(hist_df['timestamp'])
    hist_df['datetime'] = hist_df['date'].dt.tz_localize('US/Eastern').dt.tz_convert('Asia/Kolkata')
    hist_df['datetime'] = hist_df['datetime'].dt.tz_localize(tz=None)
    hist_df.drop(['timestamp','date'], axis=1, inplace=True)
    hist_df.set_index('datetime', inplace=True)
    return hist_df

def is_shooting_star(data):
    open = data[0]
    close = data[3]
    high = data[1]
    low = data[2] 
    
    if open > low and open < close:
      #Lower Wick Calculation
      lower_wick = open - low
      #Upper Wick Calculation
      upper_wick = high - close
      #Body Calculation
      Body = close - open
      
      if lower_wick == 0 or lower_wick < (.25 * open):
        if upper_wick > (1.25 * Body):
          return True
        else:
          return False
      else:
        return False
    else:
      return False
     
    #Condition 1 :
        # Open - Low should be 0 or 0.25% of price
        # Wick(High - Close) should be 1.25 % of Body(Close - Open)
        



if __name__ == "__main__" :
        scripts = ["ADANIPORTS", "BHARTIARTL","UPL", "AXISBANK", "HDFC", "ASIANPAINT","HINDUNILVR", "TITAN"]
        print("Processing the Data")
        for script in scripts:
            print("Stock : {}".format(script))
            data = get_historical_data(script)
            datas = [data.iloc[0]['open'],data.iloc[0]['high'],data.iloc[0]['low'],data.iloc[0]['close']]
            print(is_shooting_star(datas))
            df = (data  ['datetime'] == '17-02-2020')