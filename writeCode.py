# -*- coding:UTF-8 -*-
'''
@author: maidou
'''
import xml.dom.minidom
import datetime
import ConfigParser
import os


    # oldlist为过期合约。newlist为新上线合约。T1609、TF1609 T1706、TF1706
    # 上期所为小写如:fu1609,中金所为大写如：IF1609，大商所为小写如：i1609，郑商所为大写并且去掉1如：ZC609



class Conf:
    def __init__(self,ini_file):
        self.ini_f = ini_file
        self.config=ConfigParser.ConfigParser()
        self.config.readfp(open(ini_file))
        
    def get_Old_list(self):
        old_str = self.config.get('Code','oldlist')
        old_list = old_str.split(',')
        return old_list
    
    def get_New_list(self):
        new_str = self.config.get('Code','newlist')
        new_list = new_str.split(',')
        return new_list
        
    def get_old_dir(self):
        return self.config.get('FileDir','oldDir')
    
    def get_new_dir(self):
        return self.config.get('FileDir','newDir')


class Xml_file:
    def __init__(self):
        self.doms = ''
        self.xmlDomObject = ''
        self.itemlist = ''
        

    def get_root(self,oldfile,oldlist,newlist):
        self.doms = xml.dom.minidom.parse(oldfile)
        root = self.doms.documentElement
        root.setAttribute('version',setver())
        self.itemlist = root.getElementsByTagName('product')
        
        
        root2 = self.removeNodes(oldlist)
        self.itemlist = root2.getElementsByTagName('product')
        
        self.xmlDomObject = self.addNodes(newlist)
        
    
    def writer_file(self,newfile):
        f = open(newfile,'w')
    
        # 先去掉所有格式，再重新添加格式写入
        if self.xmlDomObject:
            xmlStr = self.xmlDomObject.toprettyxml(indent = '', newl = '', encoding = 'UTF-8')
            xmlStr = xmlStr.replace('\t', '').replace('\n', '')
            xmlDomObject = xml.dom.minidom.parseString(xmlStr)
            f.write(xmlDomObject.toprettyxml(indent = '\t', newl = '\n', encoding = 'UTF-8'))
        f.close
        print '%s is ok!'% newfile
    
    def removeNodes(self,oldlist):
        # 删除过期合约
        for name in oldlist:
            for item in self.itemlist:
                if item.getAttribute('tradeName') == name:
                    fanode = item.parentNode
                    fanode.removeChild(item)
        return self.doms
    
    def addNodes(self,newlist):
        # 添加新品种
        for name in newlist:
            proName,proNum = separateSN(name)
            
            for item in self.itemlist:
                itemName,ietmNum = separateSN(item.getAttribute('tradeName'))
                
                if proName == itemName:
                    if proNum < ietmNum:
                        print proName,proNum
                        atts = {}
                        atts['productId'] = item.getAttribute('productId')[0:-4]
                        if ietmNum == int(LIANXU):
                            atts['showName1'] = item.getAttribute('showName')[0:-2]
                        else:
                            atts['showName1'] = item.getAttribute('showName')[0:-4]
                        
                        atts['tradeName'] = item.getAttribute('tradeName')
                        atts['dot'] = item.getAttribute('dot')
                        atts['istradeInWeekEnd'] = item.getAttribute('istradeInWeekEnd')
                        atts['timezone'] = item.getAttribute('timezone')
                        atts['closetime'] = item.getAttribute('closetime')
                        atts['volumeMultiple'] = item.getAttribute('volumeMultiple')
                            
                        fanode = item.parentNode
                        newnode = self.doms.createElement('product')
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
                            newchi = self.doms.createElement('tradetime')
                            for child in item.childNodes:
                                if child.nodeType <> item.TEXT_NODE:
                                    for childs in child.childNodes:
                                        attlist = []
                                        if childs.nodeType <> item.TEXT_NODE:
                                            attrib = childs.attributes
                                            attlist = attrib.items()
                                            newchi2 = self.doms.createElement('time')
                                            newchi2.setAttribute(attlist[0][0],attlist[0][1])
                                            newchi2.setAttribute(attlist[1][0],attlist[1][1])
                                            newchi.appendChild(newchi2)
    
                                newnode.appendChild(newchi)
                                
                        fanode.appendChild(newnode)    
                        fanode.insertBefore(newnode,item)   # 插入连续前
                        break  
        return self.doms    
    
    
    
def set_doms(xml_dir):
    # 传入代码表所在目录，返回 文件名列表 及 文件名所在目录
    file_list = []
    if os.path.isdir(xml_dir):
        for root,dir,files in os.walk(xml_dir):
            for filepath in files:
                    
                file_list.append(filepath)
                
    return file_list,root

def make_newfile(dir,filer):
    # 传入目标文件夹路径和文件名，新建目标文件夹，链接文件夹与文件，返回目标文件绝对路径
    yOrn = os.path.isdir(dir)
    if yOrn is False:
        print "Make dir %s" % dir
        os.mkdir(dir)
    file_str = os.path.join(dir,filer)
    return file_str
        


# 获取日期为版本号 
def setver():
    today = datetime.datetime.now()
    todaystr = today.strftime("%Y%m%d")
    ver = todaystr + "00"
    print ver
    return ver





def separateSN(name):
    # 将字母与数字分开，“X”划入数字内为1000，返回品种名和合约名（cu 和  1801）
    proName = ''
    proNum = '0'
#     print name
    for s in name:
        if s.isalpha() and s.upper() <> 'X':  #将变量s内容转化为大写与‘X’比较
            proName =  proName + s
        else:
            if s.upper() == 'X':
                proNum = LIANXU
            else:
                proNum = proNum + s
    proNum = int(proNum)
#     print proName,proNum
    return proName,proNum




def main(ini_file):
    conf = Conf(ini_file)
    
    xml_list,root = set_doms(conf.get_old_dir())
    old_list = conf.get_Old_list()
    new_list = conf.get_New_list()
    
    for fi in xml_list:
        xmlFile = os.path.join(root,fi)
        if os.path.isfile(xmlFile):
            xml_file = Xml_file()
            
            xml_file.get_root(xmlFile,old_list,new_list)
            
            
            newfile = make_newfile(conf.get_new_dir(),fi)
            xml_file.writer_file(newfile)


if __name__ == "__main__":
    LIANXU = '10000'
    conf_ini = 'writeCodeConfig.ini'
    main(conf_ini)
    
    
    