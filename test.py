# _*_ coding:utf-8 _*_
#xiaohei.python.seo.call.me:)
#win+python2.7.x
import csv
'''
csvfile = file('C:\\Users\\liuyang\\Desktop\\ji\\csvtest.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['id', 'url', 'keywords'])
data = [
  ('1', 'http://www.xiaoheiseo.com/', 'С��'),
  ('2', 'http://www.baidu.com/', '�ٶ�'),
  ('3', 'http://www.jd.com/', '����')
]
writer.writerows(data)
csvfile.close()
'''
def getdict(status):
    dictstr = ''

    for i in status.keys():
        sta = i + '=' + status[i]
        dictstr = dictstr + '&' + sta

    return dictstr

if __name__ == '__main__':
    dicts = {'a':'1','b':'2'}
    d2 = {}
    strd = getdict(dicts)
    print type(strd),strd
    pass