# -*- coding:utf-8 -*-
'''
@author: liuyang
'''
import xml.dom.minidom as Dom
import ConfigParser
import os
import re
import sys

class Myconf(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr  

class Conf:
    def __init__(self,ini_file):
        self.ini_f = ini_file
        self.config=Myconf()
        try:
            self.config.readfp(open(ini_file))
        except:
            sys.exit(1)
        
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
        print "option",self.config.options(option) 
        return self.config.options(option)



class User:
    def __init__(self,pa_name):
        self.pa_name = pa_name
        self.user_attr = {}
        self.script_attr = {}
        self.code_attr = {}
        self.scriptparam = {}
    
    def read_params(self,p_file):
        if os.path.isfile(p_file):
            with open(p_file,"r") as f:
                
                for i in f :
                    line1=i.strip("\n")
                    (p_name,p_value) = line1.split("=")
                    if re.search(",",p_name) is None:
                        iType = g_config.get_int_para("iType", p_name)
                        self.scriptparam.update({p_name:{"Name":p_name,"DefaultValue":p_value}})
                        self.scriptparam[p_name].update({"iType":str(iType)})
                        self.scriptparam[p_name].update({"SingleSize":str(iType * 2)})
                        self.scriptparam[p_name].update({"DefaultStrValue":g_config.get_str_para("scriptparam", "DefaultStrValue")})
                    else:
                        name_held = p_name.split(",")[0]
                        if p_name.endswith("F"):
                            if p_value == "1":
                                self.scriptparam[name_held].update({"Selected":"True"})
                            else:
                                self.scriptparam[name_held].update({"Selected":"False"})
                                
                        elif p_name.endswith("1"):
                            self.scriptparam[name_held].update({"Min":p_value})
                            
                        elif p_name.endswith("2"):
                            self.scriptparam[name_held].update({"Max":p_value})
                        
                        elif p_name.endswith("3"):
                            self.scriptparam[name_held].update({"Step":p_value})
                        
                        else:
                            print "Error, no prames."
        
    def set_scriptparam_attr(self,f_name,p_list):
        print f_name,p_list
        for i in p_list:
            se =  re.search(f_name,i)
            if se is not None:
                self.read_params(i)
                print self.scriptparam
                break
        
        pass
        
    def set_user_attr(self,conf,con,filename,p_list):
        self.user_attr["UserType"] = "0"
        
        con2 = con.replace("-","_")
        self.user_attr["UserName"] = con2
        self.set_scriptparam_attr(con,p_list)
        
        self.user_attr["ParentUser"] = filename
        self.user_attr["AccountLastDeposit"] = conf.get_str_para("config", con)
        
        print "user_attr is %s"% self.user_attr
        
    
    def set_script_attr(self,opt):
        self.script_attr["name"] = opt
        self.script_attr["crc"] = "0"
        
        print "script is %s"% self.script_attr
        
    
    def set_code_attr(self,pro,lin):
        self.code_attr["mar"] = "1"
        
        ini_conf = Conf(ini_file)
        self.code_attr["product"] = ini_conf.get_str_para("product", pro)
        self.code_attr["period"] = ini_conf.get_str_para("period", lin)
        
        print "code is %s"% self.code_attr
        
    def get_user_attr(self):
        return self.user_attr
    
    def get_script_attr(self):
        return self.script_attr
    
    def get_code_attr(self):
        return self.code_attr
        
    def get_scriptparam_attr(self):
        return self.scriptparam
        
        

        
        
def make_xml(u_list,p_list,xml_f):
    doc = Dom.Document()  
    root_node = doc.createElement("Root")  
    for r_name in g_config.get_option("root"):
        r_value = g_config.get_str_para("root", r_name)
        root_node.setAttribute(r_name, r_value)
    
    
    doc.appendChild(root_node)  
    users_node = doc.createElement("users")  
    root_node.appendChild(users_node)
    
    for user_p in u_list:
        users_name_node = doc.createElement("user")  
        for s_name_ini in g_config.get_option("user"):
            s_value_ini = g_config.get_str_para("user", s_name_ini)
            users_name_node.setAttribute(s_name_ini, s_value_ini)

        user_para = user_p.get_user_attr()
        if user_para is not None:
            for u_key in user_para.keys():
                users_name_node.setAttribute(u_key, user_para[u_key])
    
        users_node.appendChild(users_name_node)
        
        scripts_node = doc.createElement("Scripts")  
        users_name_node.appendChild(scripts_node)
        
        scripts_name_node = doc.createElement("Script")  
        for s_name_ini in g_config.get_option("Script"):
            s_value_ini = g_config.get_str_para("Script", s_name_ini)
            scripts_name_node.setAttribute(s_name_ini, s_value_ini)

        script_para = user_p.get_script_attr()
        if script_para is not None:
            for u_key in script_para.keys():
                scripts_name_node.setAttribute(u_key, script_para[u_key])
        
        scripts_node.appendChild(scripts_name_node)
        
        
        codes_node = doc.createElement("codes")  
        scripts_name_node.appendChild(codes_node)
        
        codes_name_node = doc.createElement("code")  
        for s_name_ini in g_config.get_option("code"):
            s_value_ini = g_config.get_str_para("code", s_name_ini)
            codes_name_node.setAttribute(s_name_ini, s_value_ini)

        code_para = user_p.get_code_attr()
        if code_para is not None:
            for u_key in code_para.keys():
                codes_name_node.setAttribute(u_key, code_para[u_key])
        
        codes_node.appendChild(codes_name_node)
        
        scriptparams_node = doc.createElement("scriptparams")  
        scripts_name_node.appendChild(scriptparams_node)
        
        para_para = user_p.get_scriptparam_attr()
        #  待修改
        for p_key in para_para:
            scriptparams_name_node = doc.createElement("scriptparam")
            p_dict = para_para[p_key]
            if p_dict is not None:
                for u_key in p_dict.keys():
                    scriptparams_name_node.setAttribute(u_key, p_dict[u_key])
            scriptparams_node.appendChild(scriptparams_name_node)
        

    f = open(xml_f, "w")  
    f.write(doc.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8"))  
    f.close() 
    print "ok"   
    pass        
        
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

def read_txt(txt_file):
    user_list = []
    params_list = []
    
    if os.path.isdir(params_dir):
        for (root, dirs, files) in os.walk(params_dir):
            for f in files:
                if f.endswith("Params"):
                    codefile = os.path.join(root,f)
                    params_list.append(codefile)
                    
    (filepath,tempfilename) = os.path.split(txt_file)  # filepath为文件的目录,即D:\\workspace\\work\\wk
    (filename,extension) = os.path.splitext(tempfilename) # filename为文件名15208260, extension为文件扩展名,即.txt
    
    txt_conf = Conf(txt_file)
    for con in txt_conf.get_option("config"):
        if con <> "FZ_1":
            (strategy,product,time_line) = con.split("-")
            user = User(con)
            user.set_user_attr(txt_conf,con,filename,params_list)
            user.set_script_attr(strategy)
            user.set_code_attr(product,time_line)
            user_list.append(user)
    
    print user_list,params_list
    return user_list,params_list

def main(test_file):
    
    (user_gene_list,params_list) = read_txt(txt_file)
    make_xml(user_gene_list,params_list,test_file)
    pass


if __name__ == "__main__":
    ini_file = "D:\\workspace\\work\\wk\\config.ini"
    txt_file = "D:\\workspace\\work\\wk\\15208260.txt"
    params_dir = "D:\\workspace\\work\\wk\\"
    tester = "D:\\workspace\\work\\wk\\test.Tester"
    g_config = Conf(ini_file)
    main(tester)
#     read_params(params_file)
#     con = Conf(ini_file)
#     con.get_option("period")
    
