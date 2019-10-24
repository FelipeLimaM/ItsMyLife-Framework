# -*- coding: utf-8 -*-
import os, sqlite3, datetime
import shutil
import time
import traceback
import re, random
from sendMail import Gmail
from cryptography.fernet import Fernet
import requests
import json
from pytz import timezone
import pytz

PASS = ''
EMAIL_ROOT = ''

def show_info(params):
    msg = " ---------- CONFIG ---------- \n\n"
    for i in params:
        if not i in ["KEY_IML", "filename", "init_time", "finish_time"]:
            msg += str(i)+ " = "+str(params[i])+"\n"
    msg += "\n ---------- CONFIG ---------- \n"
    return msg

def get_datetime():
    return datetime.datetime.now()

def end_func(label,init):
    end_time = get_datetime()
    msg = "\n"+ label + " start at "+ init.strftime("%Y-%m-%d %H:%M:%S")
    msg += "\n"+ label + " end at "+ end_time.strftime("%Y-%m-%d %H:%M:%S")
    msg += "\nTime execution ("+label+"): "+ str(end_time - init)+"\n\n\n"

    return msg

def get_list(filename):
    conn = sqlite3.connect(download_database(filename))
    c2 = conn.cursor()
    c1 = conn.cursor()
    list_id_ble = {}
    for i in c2.execute('select * from ble_device'):
        list_id_ble[str(i[1])]= None
    list_id_wifi = {}
    for i in c1.execute('select * from wifi_device'):
        if i[1]:
            list_id_wifi[i[1].encode("utf8").replace('"',"").replace("'","")+"("+str(i[2])+")"]= None
    return list_id_ble, list_id_wifi

def parsePeriod(string):
    init_time = string[:string.rfind("-")-1]
    finish_time = string[string.rfind("-")+2:]

    init_time = datetime.datetime.strptime(str(init_time),"%Y/%m/%d %H:%M")
    finish_time = datetime.datetime.strptime(str(finish_time),"%Y/%m/%d %H:%M")
    print init_time, "\t\t\t" ,finish_time, "\n\n"

    init_time = timezone('America/Sao_Paulo').localize(init_time, is_dst=True)
    finish_time = timezone('America/Sao_Paulo').localize(finish_time, is_dst=True)
    print init_time, "\t\t\t" ,finish_time, "\n\n"


    init_time = init_time.astimezone(pytz.utc)
    finish_time = finish_time.astimezone(pytz.utc)
    print init_time, "\t\t\t" ,finish_time, "\n\n"


    return int(time.mktime(init_time.timetuple())), int(time.mktime(finish_time.timetuple()))


def get_period(filename):
    conn = sqlite3.connect(download_database(filename))
    c1 = conn.cursor()
    init_time = 0
    finish_time = 0
    for i in c1.execute('SELECT MIN(time) AS First, MAX(time) AS Last FROM timeline'):
        print datetime.datetime.fromtimestamp(i[0]).strftime("%Y/%m/%d %H:%M"),"\t\t",i[0],"\n",datetime.datetime.fromtimestamp(i[1]).strftime("%Y/%m/%d %H:%M"),"\t\t",i[1]
        init_time = datetime.datetime.fromtimestamp(i[0],timezone('America/Sao_Paulo')).strftime("%Y/%m/%d %H:%M")
        finish_time = datetime.datetime.fromtimestamp(i[1],timezone('America/Sao_Paulo')).strftime("%Y/%m/%d %H:%M")
        # brazil = timezone('America/Sao_Paulo')
        # floridaDatetime = datetime.datetime.fromtimestamp(ts, florida)

    # date_str = "2009-05-05 22:28:15"
    # datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('UTC'))
    return init_time, finish_time

def get_error(e,params):
    msg = "\n\n -------------------------------------------------\n\n"
    msg += str(e) + "\n\n"
    msg += str(traceback.format_exc())
    msg += "\n\n -------------------------------------------------\n\n"
    params['email_response'] += msg
    params['email_response'] += end_func("Error",params["a_func"])
    params['email_response'] += end_func("Until the error",params["all_time"])
    # print params['email_response']
    response_email(params['email'],params['subject'], params['email_response'])
    return 1

def download_database(path, full_path=True):
    path_real = path[8:path.rfind("/")+1]
    filename_real = path[path.rfind("/")+1:]

    filename_real_time = (filename_real[:filename_real.rfind(".")]+(str(random.random()))[2:]+filename_real[filename_real.rfind("."):]).replace("(","").replace(")","")

    name_cache = path_real + filename_real
    name_cache = name_cache[:name_cache.rfind("/")]+"_"+ name_cache[name_cache.rfind("/")+1:]

    if not os.path.exists(os.getcwd()+"/output/database/"):
        os.makedirs(os.getcwd()+"/output/database/")

    if os.path.exists(os.getcwd()+"/output/database/"+name_cache):
        shutil.copyfile(os.getcwd()+"/output/database/"+name_cache, os.getcwd()+"/output/"+path[8:path.rfind("/")+1] + filename_real_time)
    else:
        command_download = "sh download_file.sh \""+path_real+"\"  \""+filename_real+"\"  \""+filename_real_time+"\""
        print ("Download file (Firebase) ...")
        os.system(command_download)
        print "\n\n", os.getcwd()+"/output/"+path_real + filename_real_time, " copy for "
        print os.getcwd()+"/output/database/"+name_cache, "\n\n"
        shutil.copyfile(os.getcwd()+"/output/"+path_real + filename_real_time, os.getcwd()+"/output/database/"+name_cache)

    if full_path:
        return os.getcwd()+"/output/"+path[8:path.rfind("/")+1] + filename_real_time
    else:
        return os.getcwd()+"/output/"+path[8:path.rfind("/")+1], filename_real_time



def download_database_full(params, full_path=True):
    path = params['filename']
    path_real = path[8:path.rfind("/")+1]
    filename_real = path[path.rfind("/")+1:]

    filename_real_time = (filename_real[:filename_real.rfind(".")]+(str(random.random()))[2:]+filename_real[filename_real.rfind("."):]).replace("(","").replace(")","")

    name_cache = path_real + filename_real
    name_cache = name_cache[:name_cache.rfind("/")]+"_"+ name_cache[name_cache.rfind("/")+1:]

    if not os.path.exists(os.getcwd()+"/output/database/"):
        os.makedirs(os.getcwd()+"/output/database/")

    if os.path.exists(os.getcwd()+"/output/database/"+name_cache):
        shutil.copyfile(os.getcwd()+"/output/database/"+name_cache, os.getcwd()+"/output/"+path[8:path.rfind("/")+1] + filename_real_time)
    else:
        command_download = "sh download_file.sh \""+path_real+"\"  \""+filename_real+"\"  \""+filename_real_time+"\""
        print ("Download file (Firebase) ...")
        os.system(command_download)
        print "\n\n", os.getcwd()+"/output/"+path_real + filename_real_time, " copy for "
        print os.getcwd()+"/output/database/"+name_cache, "\n\n"
        shutil.copyfile(os.getcwd()+"/output/"+path_real + filename_real_time, os.getcwd()+"/output/database/"+name_cache)

    if full_path:
        return os.getcwd()+"/output/"+path[8:path.rfind("/")+1] + filename_real_time
    else:
        # return os.getcwd()+"/output/"+path[8:path.rfind("/")+1], filename_real_time
        params['path_real'] = os.getcwd()+"/output/"+path[8:path.rfind("/")+1]
        params['database_name'] = filename_real_time





def parse_wifi_list(list_wifi):
    response_mac = []
    response_name = []
    for i in list_wifi:
        response_mac.append( i[i.find("(")+1:-1] )
        response_name.append( i[:i.find("(")] )
    return response_mac, response_name


def create_link(key,path,file_name,level=False,params={}):
    cipher_suite = Fernet(key)
    if level:
        url = "http://localhost:8081/permalink?filename="+str(cipher_suite.encrypt(bytes(path)))+"&config="+str(cipher_suite.encrypt(bytes(file_name)))+"&key="+str(cipher_suite.encrypt(bytes(level)))+"&extra="+str(cipher_suite.encrypt(bytes(json.dumps(params))))
        # url = "http://gw.lmcad.ic.unicamp.br:2204/permalink?filename="+str(cipher_suite.encrypt(bytes(path)))+"&config="+str(cipher_suite.encrypt(bytes(file_name)))+"&key="+str(cipher_suite.encrypt(bytes(level)))+"&extra="+str(cipher_suite.encrypt(bytes(json.dumps(params))))
    else:
        url = "http://localhost:8081/permalink?filename="+str(cipher_suite.encrypt(bytes(path)))+"&config="+str(cipher_suite.encrypt(bytes(file_name)))
        # url = "http://gw.lmcad.ic.unicamp.br:2204/permalink?filename="+str(cipher_suite.encrypt(bytes(path)))+"&config="+str(cipher_suite.encrypt(bytes(file_name)))
    try:
        query_params = {'access_token': '2986e04530f2fd1992024e59b4ef729f85714b49','longUrl': url}
        endpoint = 'https://api-ssl.bitly.com/v3/shorten'
        response = requests.get(endpoint, params=query_params, verify=False)
        data = json.loads(response.content)
        if data['status_code'] == 200:
            return data['data']['url']
        else:
            return url
    except Exception as e:
        return url


def response_resquest_download(params, msg):
    response_email(params['email'],title,msg)

def response_email(email,title,body):
    gm = Gmail(EMAIL_ROOT, PASS)
    try:
        gm.send_message(email,title,body);
        print "sent for " + email
    except Exception as e:
        print " Error on email " + email
        gm.send_message("itsmylifeframework@gmail.com","[not sent]"+title,body);


def response_download_file(self,path_real,graphic_name):
    self.response.headers['Content-Type'] ='application/octet-stream'
    self.response.headers['Content-Disposition'] = 'attachment; filename="'+graphic_name+'"'
    data = open(path_real+graphic_name).read()
    self.response.out.write(data)
