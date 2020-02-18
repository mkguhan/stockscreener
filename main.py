# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 20:45:45 2020

@author: @guhankumar
"""
 
import pandas as pd
import backtrader as bt
import datetime

#scripts = ["ADANIPORTS", "BHARTIARTL","UPL", "AXISBANK", "HDFC", "ASIANPAINT","HINDUNILVR", "TITAN","TCS", "ZEEL", "TATASTEEL","HINDALCO","HDFCBANK", "ICICIBANK","INFRATEL","INDUSINDBK","HCLTECH","TECHM","INFY","DRREDDY"]
scripts = ["HEROMOTOCO","TCS","INFY","SBIN","HDFCBANK","BPCL","KOTAKBANK","UPL","TATASTEEL","HCLTECH","TECHM","SUNPHARMA","ASIANPAINT","LT","AXISBANK","RELIANCE","INDUSINDBK","ADANIPORTS","HDFC","GRASIM","BHARTIARTL","TITAN","HINDUNILVR","ICICIBANK","CIPLA"]

def get_historical_data(script):
    alpha_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=NSE:{}&interval=15min&apikey=FIKNV2QYP8FRIOPF&outputsize=full&datatype=csv".format(script)
    hist_df = pd.read_csv(alpha_url, parse_dates=True)
    hist_df['date'] = pd.to_datetime(hist_df['timestamp'])
    hist_df['datetime'] = hist_df['date'].dt.tz_localize('US/Eastern').dt.tz_convert('Asia/Kolkata')
    hist_df['datetime'] = hist_df['datetime'].dt.tz_localize(tz=None)
    hist_df.drop(['timestamp','date'], axis=1, inplace=True)
    hist_df['date'] = hist_df['datetime'].dt.date
    hist_df.set_index('datetime', inplace=True)
    return hist_df

def is_shooting_star(data):
    open = data[0]
    close = data[3]
    high = data[1]
    low = data[2] 
    #RSI = data[4]
    #print("Open: {} High {} Low {} Close{} Time {}".format(open,high,low,close, time))
    #Lower Wick Calculation
    lower_wick = open - low
    #Upper Wick Calculation
    upper_wick = high - close
    if open < 500 :
      low_wick_per = 1
    elif open > 500:
      low_wick_per = 1.5
    #Body Calculation
    Body = close - open
    #print("Low Wick: {} ;Body {} ; Upper Wick {}".format(lower_wick,Body,upper_wick))
    if open >= low and open < close:
      if lower_wick == 0 or lower_wick < low_wick_per:
          if upper_wick > (1.25 * Body):
              if lower_wick < Body:
                 print("Lower Wick: {} ;Body {} ; Upper Wick {}".format(lower_wick,Body,upper_wick))  
                 return True
              else:
                  return False
          else:
              return False
      else:
          return False
    else: 
          return False
     
def get_rsi_14(script):
    alpha_url = "https://www.alphavantage.co/query?function=RSI&symbol=NSE:{}&interval=15min&time_period=14&series_type=close&apikey=FIKNV2QYP8FRIOPF&datatype=csv".format(script) 
    rsi_df = pd.read_csv(alpha_url, parse_dates=True)
    rsi_df['date'] = pd.to_datetime(rsi_df['time'])
    rsi_df['datetime'] = rsi_df['date'].dt.tz_localize('US/Eastern').dt.tz_convert('Asia/Kolkata')
    rsi_df['datetime'] = rsi_df['datetime'].dt.tz_localize(tz=None)
    rsi_df.drop(['time','date'], axis=1, inplace=True)
    rsi_df.set_index('datetime', inplace=True)
    return rsi_df

def combine_ohlc_function(ohlc, rsi):
    combine_ohlc = pd.concat([ohlc, rsi], axis=1, sort=False)
    return combine_ohlc
    

if __name__ == "__main__" :
        enddate = datetime.datetime.now().date()
        startdate = datetime.datetime(2020, 1, 8 ).date()
        
        while startdate <= enddate :
            print("Processing the Data for date {}......".format(startdate))
            for script in scripts:
                #print("Stock : {}".format(script))
                ohlc_data = get_historical_data(script)
                #rsi_data = get_rsi_14(script)
                #data = combine_ohlc_function(ohlc_data,rsi_data)
                data = ohlc_data
                isdata_avlbe = data[(data['date'] == startdate)]
                if startdate.weekday() < 5 and len(isdata_avlbe) > 0:
                  df = data[(data['date'] == startdate)]
                  #print(df)
                  data_915=[df.iloc[-1]['open'],df.iloc[-1]['high'],df.iloc[-1]['low'],df.iloc[-1]['close']]
                  if is_shooting_star(data_915):
                      print("Date : {} :  {}".format(startdate,script))
            startdate = startdate + datetime.timedelta(days = 1)
            