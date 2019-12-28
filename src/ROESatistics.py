#-*-coding=utf-8-*-
__author__ = 'ni'

import pandas as pd
# import os
import numpy as np
import tushare as ts
import time
import globalSetting as gs


THIS_MODULE = 'ROESatistics'

dirfix= gs.g_data_dir + THIS_MODULE + gs.g_dir_separator

def get_years_report(start_year, end_year):
    if(start_year > end_year):
        tmp = start_year
        start_year = end_year
        end_year = tmp
    
    for i in range(start_year, end_year + 1):
        print(i + '\n')
        df = ts.get_report_data(i, 4)
        exclefile = str(i) + '-' + 'ROE' + '.xlsx'
        df.to_excel(exclefile)
        time.sleep(6)
        # 1,2,3,4: 1是一季度 2是中报 3是三季度 4是年报
        # for j in range(1, 4 + 1):
        #     print(j)
        #     df = ts.get_report_data(i, j)
        #     exclefile = str(i) + '-' + str(j) + '.xlsx'
        #     df.to_excel(exclefile)
        #     time.sleep(60)


def merge_report(start_year, end_year):
    if(start_year > end_year):
        tmp = start_year
        start_year = end_year
        end_year = tmp

    frames = []
    for i in range(start_year, end_year + 1):    
        exclefile = str(i) + '-' + 'ROE' + '.xlsx'
        print(exclefile + '\n')
        df = pd.read_excel(exclefile)
        # data=open("test.txt",'w+') 
        # print(df.duplicated())
        df.drop_duplicates(subset=['code'],keep='first',inplace=True)
        df.set_index("code", drop=True, inplace=True)
        #print(df)
        frames.append(df)
    
    mergedFrame = pd.concat(frames, axis=1)
    print(mergedFrame)
    exclefile = str(start_year) + '-' + str(end_year) + '-' + 'ROE' + '.xlsx'
    mergedFrame.to_excel(exclefile)
    pass


def deal_merged_report(start_year, end_year):
    if(start_year > end_year):
        tmp = start_year
        start_year = end_year
        end_year = tmp

    exclefile = str(start_year) + '-' + str(end_year) + '-' + 'ROE' + '.xlsx'
    df = pd.read_excel(exclefile)
    columns = df.columns.values.tolist()
    col_roe = []  # 存储包含‘roe’字段的列名
    col_roe.append('code')
    for i in columns:
        if 'roe' in i:
            col_roe.append(i)
    
    df = df[col_roe]
    result = df.loc[(df[col_roe] >= 10)]
    print(result)
    exclefile = str(start_year) + '-' + str(end_year) + '-filter-only-' + 'ROE' + '.xlsx'
    df.to_excel(exclefile)


def get_target_data(start_year, end_year, roe):
    if(start_year > end_year):
        tmp = start_year
        start_year = end_year
        end_year = tmp

    exclefile = dirfix + str(start_year) + '-' + str(end_year) + '-filter-only-' + 'ROE' + '.xlsx'
    df = pd.read_excel(exclefile)
    columns = df.columns.values.tolist()
    if len(columns) < 2+1:
        return

    calibrate_data = ((df[columns[2]] >= roe) & (df[columns[2]] == df[columns[2]]))
    #calibrate_data = df[columns[2]] #erorr:need set true or false to compare
    for i in range(len(columns)):
        if i == 2:
            pass
        elif i > 2:
            calibrate_data = ((df[columns[i]] >= roe) | (df[columns[i]] != df[columns[i]])) & calibrate_data
        else:
            pass

    #print(df[calibrate_data])
    exclefile = str(start_year) + '-' + str(end_year) + '-target-' + str(roe) + '-ROE' + '.xlsx'
    df[calibrate_data].to_excel(exclefile)
    pass


def main():
    start = 2006
    end = 2018
    # 获得数据
    #get_years_report(start, end)
    # 开始合并数据
    #merge_report(start, end)
    # 获取有用数据
    #deal_merged_report(start, end)
    # 筛选数据
    get_target_data(start, end, 15)
    pass


main()
    

    
