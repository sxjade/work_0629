# -*- coding:utf-8 -*-
import os
import csv
import pandas
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime


class MinFiver:
    def __init__(self,src,dct):
        self.min1filedir = src
        self.min5filedir = dct
        self.df = None
        self.min5df = None
        

    def openfile(self,filename,min5):
        hearderlist = ['date','time','open','high','low','close','downvol','holdvol','zero']
        
        self.df = pandas.read_csv(filename,header=None,names=hearderlist,keep_date_col=True,parse_dates={'timestamp':['date','time']},index_col='timestamp' )
        ohlc_dict = {'open':'first','high':'max','low':'min','close':'last','downvol':'sum','holdvol':'sum','zero':'sum'}
        
        # 合成5分钟数据，how为条件，
        self.min5df = self.df.resample('5T',how=ohlc_dict,closed='right',label='right').dropna()
        
        # 重新排序列
        open = self.min5df.pop('open')
        hold = self.min5df.pop('holdvol')
        downvol = self.min5df.pop('downvol')
        zero = self.min5df.pop('zero')
        self.min5df.insert(0,'open',open)
        self.min5df.insert(4,'downvol',downvol)
        self.min5df.insert(5,'hold',hold)
        self.min5df.insert(6,'zero',zero)
        self.min5df[['open','high','low','close','downvol','hold','zero']] = self.min5df[['open','high','low','close','downvol','hold','zero']].astype(int)
    #     pydate_array = df2.index.to_pydatetime()
    #     date_only_array = np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(pydate_array )
    #     date_only_series = pd.Series(date_only_array)
    #     
    #     time_only_array = np.vectorize(lambda s: s.strftime('%H:%M'))(pydate_array )
    #     time_only_series = pd.Series(time_only_array)
    # #     print type(time_only_series),time_only_series
    #     df2.insert(0,'date',date_only_series)
    #     df2.insert(1,'times',time_only_series)
    # #     print df2
#         self.min5df.to_csv(min5,header=False)
        self.writer(min5)
#         print '%s writer ok.' % min5
        
    def writer(self,dscfile):
        minfile = file(dscfile,'wb')
        writer = csv.writer(minfile)
        if self.min5df is not None:
            for i in self.min5df.index:
                lin = self.min5df.loc[i]
                daystr,timestr = self.chengedate(lin.name)
                linlist = [daystr,timestr,lin['open'],lin['high'],lin['low'],lin['close'],lin['downvol'],lin['hold'],lin['zero']]
                writer.writerow(linlist)
#                 print linlist
        minfile.close()
        print 'min5 writer ok.'
        
    def chengedate(self,timestp):
        daystr = datetime.strftime(timestp,'%Y.%m.%d')
        timestr = datetime.strftime(timestp,'%H:%M')
        return daystr,timestr
        
    
    def outfile(self,dirs,filename):
        
        min5name = '5' + filename[1:]
        min5path = os.path.join(dirs,min5name)
        
        return min5path
        
    def main(self):
        if os.path.isdir(self.min1filedir):
            for root,dir,files in os.walk(self.min1filedir):
                for filer in files:
                    filepath = os.path.join(root,filer)
                    min5 = self.outfile(self.min5filedir,filer)
                    print filepath
                    self.openfile(filepath,min5)
                    

if __name__ == '__main__':
    min1filedir = 'D:\BaiduNetdiskDownload\out\kline\zz'
    min5filedir = 'D:\BaiduNetdiskDownload\out\kline'
#     openfile('D:\\BaiduNetdiskDownload\\out\\1min-1-09999.csv')
    fa = MinFiver(min1filedir,min5filedir)
    fa.main()
    