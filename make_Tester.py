# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import xml.dom.minidom as Dom
import ConfigParser
import os
import re


class Myconf(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr  

class Conf:
    def __init__(self,ini_file):
        self.ini_f = ini_file
        self.config=Myconf()
        self.config.readfp(open(ini_file))
        
    def get_str_para(self,section,parameter):
        str_para = self.config.get(section,parameter)
        return str_para
    
    def get_int_para(self,section,parameter):
        int_para = self.config.getint(section,parameter)
        return int_para
        
    def get_float_para(self,section,parameter):
        float_para = self.config.getint(section,parameter)
        return float_para
    
    def get_option(self,option):
        print self.config.options(option) 
        return self.config.options(option)

def read_params(params_filer):
    params_dict = {}
    
    with open(params_filer) as params_object:
        for line in params_object:
            line = line.strip('\n')
            key2,value = line.split('=')
            if re.search(',',key2)is None:
                key1 = key2
            if params_dict.has_key(key1):
                params_dict[key1][key2] = value
                    
            else:
                params_dict[key1] = {}
            
    print params_dict
    return params_dict

class XML_file:
    def __init__(self):
        self.user = {}
        self.script = {}
        self.code = {}
        self.scriptparam = {}
        
    def get_scriptparam(self):
        self.scriptparam = read_params()
        
    def get_user(self,ini_f):
        self.user["UserType"] = "0"  # 默认值
        
        (filepath,tempfilename) = os.path.split(ini_f)   # filepath为文件的目录
        (filename,extension) = os.path.splitext(tempfilename)  # filename文件名，extension扩展名
        self.user["ParentUser"] = filename
        
        user_conf = Conf(ini_f)
        config_list = user_conf.get_option("config")
        for con in config_list:
            if user_conf.get_int_para("config", con) <> 0:
                self.user["AccountLastDeposit"] = str(user_conf.get_int_para("config", con))
                self.user["UserName"] = con
        print self.user
    
    def get_script(self):
        pass
    
    def get_code(self):
        pass


def creat_XML():
    doc = Dom.Document()  
    root_node = doc.createElement("Root")  
    root_node.setAttribute("EndTime", "43144")  
    root_node.setAttribute("StartTime", "42779")  
    root_node.setAttribute("TesterType", "0")  
    root_node.setAttribute("IsOptimization", "False")
    root_node.setAttribute("IsOpenSpeed", "False")  
    root_node.setAttribute("Speed", "220")  
    root_node.setAttribute("TimePartType", "0")  
    root_node.setAttribute("IsContinue", "False")
    
    
    doc.appendChild(root_node)  
    users_node = doc.createElement("users")  
    root_node.appendChild(users_node)
    
    users_name_node = doc.createElement("user")  
    users_name_node.setAttribute("UserName", "UNICORE5_RU_15M")  
    users_name_node.setAttribute("AccountLastDeposit", "234000")  
    users_name_node.setAttribute("ParentUser", "15208260")  
    users_name_node.setAttribute("UserType", "0")  
    users_node.appendChild(users_name_node)
    
    scripts_node = doc.createElement("Scripts")  
    users_name_node.appendChild(scripts_node)
    
    scripts_name_node = doc.createElement("Script")  
    scripts_name_node.setAttribute("name", "UNICORE5")  
    scripts_name_node.setAttribute("crc", "0") 
    scripts_node.appendChild(scripts_name_node)
    
    codes_node = doc.createElement("codes")  
    scripts_name_node.appendChild(codes_node)
    
    codes_name_node = doc.createElement("code")  
    codes_name_node.setAttribute("mar", "1")  
    codes_name_node.setAttribute("product", "99999") 
    codes_name_node.setAttribute("period", "770") 
    codes_node.appendChild(codes_name_node)
    
    scriptparams_node = doc.createElement("scriptparams")  
    scripts_name_node.appendChild(scriptparams_node)
    
    scriptparams_name_node = doc.createElement("scriptparam")  
    scriptparams_name_node.setAttribute("Selected", "False")  
    scriptparams_name_node.setAttribute("iType", "2") 
    scriptparams_name_node.setAttribute("SingleSize", "4") 
    scriptparams_name_node.setAttribute("Max", "10")  
    scriptparams_name_node.setAttribute("Min", "10") 
    scriptparams_name_node.setAttribute("Step", "0") 
    scriptparams_name_node.setAttribute("Name", "MULITY")  
    scriptparams_name_node.setAttribute("DefaultValue", "15") 
    scriptparams_name_node.setAttribute("DefaultStrValue", "") 
    scriptparams_node.appendChild(scriptparams_name_node)
     
 
    f = open("book_store.xml", "w")  
    f.write(doc.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8"))  
    f.close() 
    print "ok"   
        

    



if __name__ == "__main__":
    ini_file = "D:\\workspace\\work\\wk\\config.ini"
    ini_file = "D:\\workspace\\work\\wk\\15208260.ini"
    params_file = "D:\\workspace\\work\\wk\\UNICORE1-AG-3M.PARAMS"
    xml_test = XML_file()
    xml_test.get_user(ini_file)
#     creat_XML()
#     read_params(params_file)
#     con = Conf(ini_file)
#     con.get_option("period")
    pass
