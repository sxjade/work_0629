

def getdict(status):
    dictstr = ''
        
    for i in status.keys():
        sta = i + '=' + status[i]
        dictstr = dictstr + '&' + sta
            
    return dictstr

if __name__ == '__main__':
    dicts = {'a':'1','b':'2'}
    d2 = {}
    strd = getdict(d2)
    print type(strd),strd
    pass