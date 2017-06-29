# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import sqlite3
import csv
import time

class SqliteDate:
    def __init__(self,sqflie):
        self.cx = sqlite3.connect(sqflie)
        self.dates = None
        
    def getcu(self):
        return self.cx.cursor()
    
    def selectdb(self):
        cu = self.getcu()
        sql = 'select * from KlineData'
        litedate = cu.execute(sql)
        self.dates = cu.fetchall()
        
    def exceptcsv(self,outfile):
        self.selectdb()
        csvfile = file(outfile,'wb')
        writer = csv.writer(csvfile)
        if self.dates is not None:
            for lin in self.dates:
                day_str,time_str = self.formattime(lin[0])
                ope,hig,low,clo,vol,hod,men = lin[1],lin[2],lin[3],lin[4],lin[5],lin[6],lin[7]
                writer.writerow([day_str,time_str,ope,hig,low,clo,vol,hod,men])
#             writer.writerows(self.dates)
        csvfile.close()

    def formattime(self,time_int):
        ti = time.localtime(time_int)
        hours_int = int(time.strftime("%H", ti))
        day_str = time.strftime("%Y.%m.%d", ti)
        time_str = time.strftime("%H:%M", ti)
        if 0 <= hours_int <= 5 or  12 <= hours_int <= 14 or 16 <= hours_int <= 18 :
            pass
        else:
            print day_str,time_str
        
        return day_str,time_str

if __name__ == '__main__':
    sqlfile = 'D:\\BAK\\ATS_date\\sh\\bu_ipt\\min1.db'
    outfile = 'D:\\BAK\\ATS_date\\sh\\bu_ipt\\bu_ipt_min1.csv'
    s = SqliteDate(sqlfile)
    s.exceptcsv(outfile)
    