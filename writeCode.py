# -*- coding:UTF-8 -*-
'''
@author: maidou
'''
import xml.dom.minidom
import datetime
import ConfigParser


    # oldlist为过期合约。newlist为新上线合约。T1609、TF1609 T1706、TF1706
    # 上期所为小写如:fu1609,中金所为大写如：IF1609，大商所为小写如：i1609，郑商所为大写并且去掉1如：ZC609
#     oldlist = ('IC1611','IH1611','IF1611')
#     newlist = ('IC1701','IH1701','IF1701')

config=ConfigParser.ConfigParser()
config.readfp(open('writeCodeConfig.ini'))
oldstr=config.get('Code','oldlist')
newstr=config.get('Code','newlist')
oldlist=oldstr.split(',')
newlist=newstr.split(',')

oldfile=config.get('FileDir','oldFile')
newfile=config.get('FileDir','newFile')



# 获取日期为版本号 
def setver():
    today = datetime.datetime.now()
    todaystr = today.strftime("%Y%m%d")
    ver = todaystr + "00"
    print ver
    return ver

# 删除过期合约
def removeNodes(itemlist,oldlist):
    for name in oldlist:
        for item in itemlist:
            if item.getAttribute('tradeName') == name:
                fanode = item.parentNode
                fanode.removeChild(item)
#            print item.getAttribute('tradeName')
    return doms

# 将字母与数字分开，“X”划入数字内
def separateSN(name):
    proName = ''
    proNum = ''
    for s in name:
        if s.isalpha() and s.upper() <> 'X':  #将变量s内容转化为大写与‘X’比较
            proName =  proName + s
        else:
            proNum = proNum + s
    return proName,proNum

# 添加新品种
def addNodes(itemlist,newlist):
    for name in newlist:
        proName,proNum = separateSN(name)
        prolin = 0
        for item in itemlist:
            itemName,ietmNum = separateSN(item.getAttribute('tradeName'))
            if proName == itemName:
                if len(ietmNum) <> 1: # and proNum < int(ietmNum):
                    pass
                else:
                    if proName == itemName:
                        print proName,proNum
                        atts = {}
                        atts['productId'] = item.getAttribute('productId')[0:-4]
                        atts['showName1'] = item.getAttribute('showName')[0:-2]
#                        print item.getAttribute('showName')[0:-2]
                        atts['showName2'] = item.getAttribute('showName')[-4:]
                        atts['tradeName'] = item.getAttribute('tradeName')
                        atts['dot'] = item.getAttribute('dot')
                        atts['istradeInWeekEnd'] = item.getAttribute('istradeInWeekEnd')
                        atts['timezone'] = item.getAttribute('timezone')
                        atts['closetime'] = item.getAttribute('closetime')
                        atts['volumeMultiple'] = item.getAttribute('volumeMultiple')
                        
                        fanode = item.parentNode
                        newnode = doms.createElement('product')
                        if len(str(proNum)) == 3:
                            newnode.setAttribute('productId',atts['productId']+'1'+str(proNum))
                            newnode.setAttribute('showName',atts['showName1']+'1'+str(proNum))
                        else:
                            newnode.setAttribute('productId',atts['productId']+str(proNum))
                            newnode.setAttribute('showName',atts['showName1']+str(proNum))
                        newnode.setAttribute('tradeName',name)
                        newnode.setAttribute('dot',atts['dot'])
                        newnode.setAttribute('istradeInWeekEnd',atts['istradeInWeekEnd'])
                        newnode.setAttribute('timezone',atts['timezone'])
                        newnode.setAttribute('closetime',atts['closetime'])
                        newnode.setAttribute('volumeMultiple',atts['volumeMultiple'])
                        if item.hasChildNodes:
                            newchi = doms.createElement('tradetime')
                            for child in item.childNodes:
                                if child.nodeType <> item.TEXT_NODE:
                                    for childs in child.childNodes:
                                        attlist = []
                                        if childs.nodeType <> item.TEXT_NODE:
                                            attrib = childs.attributes
                                            attlist = attrib.items()
                                            newchi2 = doms.createElement('time')
                                            newchi2.setAttribute(attlist[0][0],attlist[0][1])
                                            newchi2.setAttribute(attlist[1][0],attlist[1][1])
                                            newchi.appendChild(newchi2)

                                newnode.appendChild(newchi)
                            
                        fanode.appendChild(newnode)    
                        fanode.insertBefore(newnode,item)   # 插入连续前
            prolin += 1  #记录行数 
    return doms

if __name__ == "__main__":
    doms = xml.dom.minidom.parse(oldfile)
    root = doms.documentElement
    root.setAttribute('version',setver())
    itemlist = root.getElementsByTagName('product')
    f = open(newfile,'w')
    
    root2 = removeNodes(itemlist,oldlist)
    itemlist2 = root2.getElementsByTagName('product')
    
    xmlDomObject = addNodes(itemlist2,newlist)
    # 先去掉所有格式，再重新添加格式写入
    if xmlDomObject:
        xmlStr = xmlDomObject.toprettyxml(indent = '', newl = '', encoding = 'UTF-8')
        xmlStr = xmlStr.replace('\t', '').replace('\n', '')
        xmlDomObject = xml.dom.minidom.parseString(xmlStr)
        f.write(xmlDomObject.toprettyxml(indent = '\t', newl = '\n', encoding = 'UTF-8'))
    f.close