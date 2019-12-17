#-*-coding=utf-8-*-
__author__ = 'ni'


import pandas as pd
import os
import numpy as np
import tushare as ts

global global_rate
global_rate = 10000
#pd.set_option('display.max_rows',None)
class StatisticsMarketValue():
    def __init__(self):
        print("StatisticsMarketValue")

    def start_statistics(self, min, max):
        if min > max:
            tmp = min
            min = max
            max = tmp
        csvfile = "today_all.csv"
        if not os.path.exists(csvfile):
            print("get data from tushare")
            df = ts.get_today_all()#属性：代码，名称，涨跌幅，现价，开盘价，最高价，最低价，最日收盘价，成交量，换手率，成交额，市盈率，市净率，总市值，流通市值
            df.to_csv(csvfile)
        else:
            df = pd.read_csv(csvfile)
        result = df.loc[(df["mktcap"] >= min) & (df["mktcap"] <= max)].sort_values(["mktcap"], ascending=False)
        filterFrame = result.name.str.contains('ST') | result.name.str.contains('退')
        exclefile = str(min/global_rate) + '-' + str(max/global_rate) + '.xlsx'
        print('filename:' + exclefile)
        result[~filterFrame].to_excel(exclefile)
        exclefile = str(min/global_rate) + '-' + str(max/global_rate) + '-ST.xlsx'
        print('filename:' + exclefile)
        result[filterFrame].to_excel(exclefile)
        print(result)


def main():
    obj = StatisticsMarketValue()
    obj.start_statistics(0*global_rate, 10*global_rate)
    obj.start_statistics(10*global_rate, 30*global_rate)
    obj.start_statistics(30*global_rate, 50*global_rate)
    obj.start_statistics(50*global_rate, 100*global_rate)
    obj.start_statistics(300*global_rate, 100*global_rate)
    obj.start_statistics(300*global_rate, 500*global_rate)
    obj.start_statistics(1000*global_rate, 500*global_rate)
    obj.start_statistics(1000*global_rate, 5000*global_rate)
    obj.start_statistics(100000*global_rate, 5000*global_rate)


main()