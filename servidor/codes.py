import os, sys
import traceback
import export_csv
import pandas as pd
import machine_learning.pre_processing as pre
from machine_learning.clustering import Clustering
from battery import ExportBattery, BatteryGraphic
from sensorhub import ExportSensorHub, SensorHubGraphic
from bluetooth import ExportBluetooth, BluetoothGraphic
from wifi import ExportWifi, WifiGraphic
import utils

def download_database(params):
    params['subject'] =  "Database - "
    path_real, database_name = utils.download_database(params['filename'], full_path = False)
    utils.response_email(params['email'] , params['subject'], utils.create_link(params['KEY_IML'],path_real,database_name))

def filter_simple_bluetooth(params):
    params['subject'] =  "Filter Bluetooth Graphic"
    email_response = utils.show_info(params) + "\n"
    path_real, database_name = utils.download_database(params['filename'], full_path = False)
    only_name = database_name[:database_name.rfind(".")]
    params["all_time"] = utils.get_datetime() #TIME
    params["a_func"] = utils.get_datetime() #TIME
    try:
        email_response += "Exporting data (Bluetooth) ..."
        export_csv ="filter_ble%s" % (only_name+".csv")
        ExportBluetooth(params['ble_list'],params['is_blacklist']).run(path_real+database_name,path_real+export_csv)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("CSV conversion",params["a_func"])
    email_response += "OK\n"
    email_response += "\n CSV file = "+utils.create_link(params['KEY_IML'],str(path_real),str(export_csv))+"\n\n\n"
    email_response += time_txt

    try:
        email_response += "Building Graphic (Bluetooth) ..."
        path_graphic ="filter_ble_%s" % (only_name+".pdf")
        BluetoothGraphic().run(path_real+export_csv,path_real+path_graphic)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("Graphic creation",params["a_func"])
    email_response += "OK\n"
    email_response += "\n Graphic = "+utils.create_link(params['KEY_IML'],str(path_real),str(path_graphic))+"\n\n\n"
    email_response += time_txt

    email_response += utils.end_func("All process",params["all_time"])
    return utils.response_email(params['email'],params['subject'], email_response)

def filter_simple_wifi(params):
    params['subject'] =  "Filter WIFI Graphic "
    email_response = utils.show_info(params) + "\n"
    path_real, database_name = utils.download_database(params['filename'], full_path = False)
    only_name = database_name[:database_name.rfind(".")]
    params["all_time"] = utils.get_datetime() #TIME
    params["a_func"] = utils.get_datetime() #TIME
    try:
        email_response += "Exporting data (WIFI) ..."
        export_csv ="filter_wifi%s" % (only_name+".csv")
        wifi_list_mac, wifi_list_name = utils.parse_wifi_list(params['wifi_list'])
        ExportWifi(wifi_list_mac,wifi_list_name,params['is_blacklist']).run(path_real+database_name,path_real+export_csv)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("CSV conversion",params["a_func"])
    email_response += "OK\n"
    email_response += "\n CSV file = "+utils.create_link(params['KEY_IML'],str(path_real),str(export_csv))+"\n\n\n"
    email_response += time_txt

    try:
        email_response += "Building Graphic (Bluetooth) ..."
        path_graphic ="filter_wifi_%s" % (only_name+".pdf")
        WifiGraphic().run(path_real+export_csv,path_real+path_graphic)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("Graphic creation",params["a_func"])
    email_response += "OK\n"
    email_response += "\n Graphic = "+utils.create_link(params['KEY_IML'],str(path_real),str(path_graphic))+"\n\n\n"
    email_response += time_txt

    email_response += utils.end_func("All process",params["all_time"])
    return utils.response_email(params['email'],params['subject'], email_response)

def simple_sensorHub(params):
    params['subject'] =  "SensorHub Graphic "
    email_response = ""
    path_real, database_name = utils.download_database(params['filename'], full_path = False)
    only_name = database_name[:database_name.rfind(".")]
    params["all_time"] = utils.get_datetime() #TIME
    params["a_func"] = utils.get_datetime() #TIME
    try:
        email_response += "Exporting data (Sensor Hub) ..."
        export_csv ="SensorHub_%s" % (only_name+".csv")
        ExportSensorHub().run(path_real+database_name, path_real+export_csv)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("CSV conversion",params["a_func"])
    email_response += "OK\n"
    email_response += "\n CSV file = "+utils.create_link(params['KEY_IML'],str(path_real),str(export_csv))+"\n\n\n"
    email_response += time_txt

    try:
        email_response += "Building Graphic (Sensor Hub) ..."
        path_graphic ="sensor_hub_%s" % (only_name+".pdf")
        SensorHubGraphic().run(path_real+export_csv,path_real+path_graphic)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("Graphic creation",params["a_func"])
    email_response += "OK\n"
    email_response += "\n Graphic = "+utils.create_link(params['KEY_IML'],str(path_real),str(path_graphic))+"\n\n\n"
    email_response += time_txt

    email_response += utils.end_func("All process",params["all_time"])
    return utils.response_email(params['email'],params['subject'], email_response)

def simple_bluetooth(params):
    params['subject'] =  "Bluetooth Graphic "
    email_response = ""
    path_real, database_name = utils.download_database(params['filename'], full_path = False)
    only_name = database_name[:database_name.rfind(".")]
    params["all_time"] = utils.get_datetime() #TIME
    params["a_func"] = utils.get_datetime() #TIME
    try:
        email_response += "Exporting data (Bluetooth) ..."
        export_csv ="ble_%s" % (only_name+".csv")
        ExportBluetooth().run(path_real+database_name, path_real+export_csv)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("CSV conversion",params["a_func"])
    email_response += "OK\n"
    email_response += "\n CSV file = "+utils.create_link(params['KEY_IML'],str(path_real),str(export_csv))+"\n\n\n"
    email_response += time_txt

    try:
        email_response +="Building Graphic (Bluetooth) ..."
        path_graphic ="ble_%s" % (only_name+".pdf")
        BluetoothGraphic().run(path_real+export_csv,path_real+path_graphic)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("Graphic creation",params["a_func"])
    email_response += "OK\n"
    email_response += "\n Graphic = "+utils.create_link(params['KEY_IML'],str(path_real),str(path_graphic))+"\n\n\n"
    email_response += time_txt

    email_response += utils.end_func("All process",params["all_time"])
    return utils.response_email(params['email'],params['subject'], email_response)

def simple_wifi(params):
    params['subject'] =  "WIFI Graphic "
    email_response = ""
    path_real, database_name = utils.download_database(params['filename'], full_path = False)
    only_name = database_name[:database_name.rfind(".")]
    params["all_time"] = utils.get_datetime() #TIME
    params["a_func"] = utils.get_datetime() #TIME
    try:
        email_response += "Exporting data (WIFI) ..."
        export_csv ="wifi_%s" % (only_name+".csv")
        ExportWifi().run(path_real+database_name, path_real+export_csv)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("CSV conversion",params["a_func"])
    email_response += "OK\n"
    email_response += "\n CSV file = "+utils.create_link(params['KEY_IML'],str(path_real),str(export_csv))+"\n\n\n"
    email_response += time_txt

    try:
        email_response +="Building Graphic (WIFI) ..."
        path_graphic ="wifi_%s" % (only_name+".pdf")
        WifiGraphic().run(path_real+export_csv,path_real+path_graphic)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("Graphic creation",params["a_func"])
    email_response += "OK\n"
    email_response += "\n Graphic = "+utils.create_link(params['KEY_IML'],str(path_real),str(path_graphic))+"\n\n\n"
    email_response += time_txt

    email_response += utils.end_func("All process",params["all_time"])
    return utils.response_email(params['email'],params['subject'], email_response)

def simple_battery(params):
    params['subject'] =  "Battery Graphic "
    email_response = ""
    path_real, database_name = utils.download_database(params['filename'], full_path = False)
    only_name = database_name[:database_name.rfind(".")]
    params["all_time"] = utils.get_datetime() #TIME
    params["a_func"] = utils.get_datetime() #TIME
    try:
        email_response += "Exporting data (Battery) ..."
        export_csv ="battery_%s" % (only_name+".csv")
        ExportBattery().run(path_real+database_name, path_real+export_csv)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("CSV conversion",params["a_func"])
    email_response += "OK\n"
    email_response += "\n CSV file = "+utils.create_link(params['KEY_IML'],str(path_real),str(export_csv))+"\n\n\n"
    email_response += time_txt

    try:
        email_response += "Building Graphic (Battery) ..."
        path_graphic ="battery_%s" % (only_name+".pdf")
        BatteryGraphic().run(path_real+export_csv,path_real+path_graphic)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("Graphic creation",params["a_func"])
    email_response += "OK\n"
    email_response += "\n Graphic = "+utils.create_link(params['KEY_IML'],str(path_real),str(path_graphic))+"\n\n\n"
    email_response += time_txt

    email_response += utils.end_func("All process",params["all_time"])
    return utils.response_email(params['email'],params['subject'], email_response)

def exec_ML_1(params):
    params['subject'] = "Machine Learning - Results"
    email_response = utils.show_info(params) + "\n"
    try:
        email_response += "download database ..."
        path_real, database_name = utils.download_database(params['filename'], full_path = False)
    except Exception as e:
        return utils.get_error(e, params)

    email_response += "OK\n"
    email_response += "\n Database = "+utils.create_link(params['KEY_IML'],str(path_real),str(database_name))+"\n\n\n"
    params['path_real'] = path_real
    params['database_name'] = database_name

    params["only_database_name"] = database_name[:database_name.rfind(".")]
    params["all_time"] = utils.get_datetime() #TIME
    params["a_func"] = utils.get_datetime() #TIME
    try:
        email_response += "Converting csv ..."
        params["csvfile"] = params["only_database_name"]+".csv"
        export_csv.run(
            inputfile=path_real+database_name,
            outputfile=path_real+params["csvfile"],
            bluetooth=params['bluetooth'],
            wifi=params['wifi'],
            sensorhub=params['optimzation_sensor_hub'],
            battery=True if params['optimzation_sensor_hub'] else False ,
            optimize=params['optimzation_sensor_hub'],
            )
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("CSV conversion",params["a_func"])
    email_response += "OK\n"
    email_response += "\n CSV file = "+utils.create_link(params['KEY_IML'],str(path_real),str(params["csvfile"]))+"\n\n"
    email_response += time_txt

    params["a_func"] = utils.get_datetime() #TIME
    try:
        email_response += "PreProcessing ..."
        df = pd.read_csv(open(path_real+params["csvfile"],"r"), sep=',', header=0, index_col=0)
        pre_processing = pre.PreProcessing(df,norm=params['optimzation_sensor_hub'])
        df = pre_processing.build()
        df.to_csv(path_real+"pre_processing"+params["csvfile"], sep=',', encoding='utf-8', header=True)
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("PreProcessing",params["a_func"])
    email_response += "OK\n"
    email_response += "\n CSV PreProcessing = "+utils.create_link(params['KEY_IML'],str(path_real),path_real+"pre_processing"+params["csvfile"])+"\n\n"
    email_response += time_txt
    params['csvpreprocessing'] = path_real+"pre_processing"+params["csvfile"]

    params["a_func"] = utils.get_datetime() #TIME
    try:
        email_response += "Clustering ..."
        labels, n_clusters = Clustering(df, mode="fixed_k", n_clusters=int(params['number'])).clusterize()
        timestamp = list(df.index)
        params['csvcluster'] = str(params['number'])+"clusters"+params["only_database_name"]+".csv"
        with open(path_real+params['csvcluster'], 'w') as f:
            f.write("timestamp,clusters\n")
            for i in range(len(labels)):
                f.write("{},{}\n".format(timestamp[i],labels[i]))
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("Clustering",params["a_func"])
    email_response += "OK\n"
    email_response += "\n CSV MachineLearning = "+utils.create_link(params['KEY_IML'],str(path_real),str(params['csvcluster']))+"\n\n"
    email_response += time_txt


    params["a_func"] = utils.get_datetime() #TIME
    try:
        email_response += "Creating graphic..."
        params['pdfgraphic'] = (params["only_database_name"]+".pdf").replace("(","").replace(")","")
        print "Rscript machine_learning/pdf/pdf_lines.R \""+path_real+params['csvcluster']+"\" \""+path_real+params['pdfgraphic']+"\""
        os.system("Rscript machine_learning/pdf/pdf_lines.R \""+path_real+params['csvcluster']+"\" \""+path_real+params['pdfgraphic']+"\"")
    except Exception as e:
        return utils.get_error(e, params)

    time_txt = utils.end_func("Graphic creation",params["a_func"])
    email_response += "OK\n"
    email_response += "\n Graphic = "+utils.create_link(params['KEY_IML'],str(path_real),str(params['pdfgraphic']))+"\n\n"
    email_response += time_txt


    print email_response
    email_response += utils.end_func("All process",params["all_time"])
    return utils.response_email(params['email'],"Machine Learning - Results", email_response)

def exec_ML(params):
    params["email_response"] = utils.show_info(params) + "\n"
    params["subject"] = "Machine Learning - Results (With Filter)"

    E_get_database(params)

    E_export_csv(params)

    df = E_pre_processing(params)

    E_clustering(df,params)

    E_graphic(params)

    params["email_response"] += utils.end_func("All process",params["all_time"])
    # print params["email_response"]
    return utils.response_email(params['email'],params["subject"], params["email_response"])


def continue_ML(params):
    params["email_response"] = utils.show_info(params) + "\n"
    params["only_database_name"] = params['filename'][:params['filename'].rfind(".")]
    params["subject"] = "Machine Learning - Results (Continue)"

    params["all_time"] = utils.get_datetime() #TIME
    if params['level_html'] == 1:

        params['csvfile'] = params['filename']
        df = E_pre_processing(params)
        E_clustering(df,params)
        E_graphic(params)


    elif params['level_html'] == 2:

        params['csvpreprocessing'] = params['filename']
        df = pd.read_csv(open(params['path_real']+params["csvpreprocessing"],"r"), sep=',', header=0, index_col=0)
        E_clustering(df,params)
        E_graphic(params)


    elif params['level_html'] == 3:

        params['csvcluster'] = params['filename']
        E_graphic(params)




    params["email_response"] += utils.end_func("All process",params["all_time"])
    print params["email_response"]
    return utils.response_email(params['email'],params["subject"], params["email_response"])

def E_get_database(params):
    try:
        params["email_response"] += "download database ..."
        utils.download_database_full(params, full_path = False)
    except Exception as e:
        utils.get_error(e, params)
        raise

    params["email_response"] += "OK\n"
    params["email_response"] += "\n Database = "+utils.create_link(params['KEY_IML'],str(params['path_real']),str(params['database_name']))+"\n\n\n"

    params["only_database_name"] = params['database_name'][:params['database_name'].rfind(".")]
    params["all_time"] = utils.get_datetime() #TIME

def E_export_csv(params):
    init_time = None
    finish_time = None

    params["whitelist_ble"]=[]
    params["whitelist_wifi"]=[]
    params["blacklist_ble"]=[]
    params["blacklist_wifi"]=[]

    if params['bluetooth']:
        if 'is_only_hardcode' in params:
            if params['is_only_hardcode']:
                # Hardcode
                print "entro errado"
            else:
                print "entro certo"
                if 'ble_list' in params:
                    if params['ble_list']:
                        if 'is_blacklist_ble' in params:
                            if params['is_blacklist_ble']:
                                params["blacklist_ble"] = params['ble_list']
                            else:
                                params["whitelist_ble"] = params['ble_list']

    if params['wifi']:
        if 'wifi_list' in params:
            if params['wifi_list']:
                if 'is_blacklist_wifi' in params:
                    if params['is_blacklist_wifi']:
                        params["blacklist_wifi"] = utils.parse_wifi_list(params['wifi_list'])[0]
                    else:
                        params["whitelist_wifi"] = utils.parse_wifi_list(params['wifi_list'])[0]


    if 'set_period' in params:
        if params['set_period']:
            init_time = params['init_time']
            finish_time = params['finish_time']


    params["a_func"] = utils.get_datetime() #TIME
    try:
        params["email_response"] += "Converting csv ..."
        params["csvfile"] = params["only_database_name"]+".csv"
        export_csv.run(
            inputfile=params['path_real']+params['database_name'],
            outputfile=params['path_real']+params["csvfile"],
            bluetooth=params['bluetooth'],
            wifi=params['wifi'],
            sensorhub=params['optimzation_sensor_hub'],
            battery= True if params['optimzation_sensor_hub'] else False,
            optimize=params['optimzation_sensor_hub'],
            whitelist_ble=params["whitelist_ble"],
            whitelist_wifi=params["whitelist_wifi"],
            blacklist_ble=params["blacklist_ble"],
            blacklist_wifi=params["blacklist_wifi"],
            init_time = init_time,
            finish_time = finish_time,
            )
    except Exception as e:
        utils.get_error(e, params)
        raise

    time_txt = utils.end_func("CSV conversion",params["a_func"])
    params["email_response"] += "OK\n"
    params["email_response"] += "\n CSV file = "+utils.create_link(params['KEY_IML'],str(params['path_real']),str(params["csvfile"]),str("1"),{'optimzation_sensor_hub':params["optimzation_sensor_hub"]})+"\n\n"
    params["email_response"] += time_txt

def E_pre_processing(params):
    params["a_func"] = utils.get_datetime() #TIME
    try:
        params["email_response"] += "PreProcessing ..."
        params['csvpreprocessing'] = "pre_processing"+params["csvfile"]
        df = pd.read_csv(open(params['path_real']+params["csvfile"],"r"), sep=',', header=0, index_col=0)
        pre_processing = pre.PreProcessing(df,norm=params['optimzation_sensor_hub'])
        df = pre_processing.build()
        df.to_csv(params['path_real']+params['csvpreprocessing'], sep=',', encoding='utf-8', header=True)
    except Exception as e:
        utils.get_error(e, params)
        raise


    time_txt = utils.end_func("PreProcessing",params["a_func"])
    params["email_response"] += "OK\n"
    params["email_response"] += "\n CSV PreProcessing = "+utils.create_link(params['KEY_IML'],str(params['path_real']),str(params['csvpreprocessing']),str("2"),{'optimzation_sensor_hub':params["optimzation_sensor_hub"]})+"\n\n"
    params["email_response"] += time_txt

    return df

def E_clustering(df,params):
    params["a_func"] = utils.get_datetime() #TIME
    try:
        params["email_response"] += "Clustering ..."
        labels, n_clusters = Clustering(df, mode="fixed_k", n_clusters=int(params['number'])).clusterize()
        timestamp = list(df.index)
        params['csvcluster'] = str(params['number'])+"clusters"+params["only_database_name"]+".csv"
        with open(params['path_real']+params['csvcluster'], 'w') as f:
            f.write("timestamp,clusters\n")
            for i in range(len(labels)):
                f.write("{},{}\n".format(timestamp[i],labels[i]))
    except Exception as e:
        utils.get_error(e, params)
        raise

    time_txt = utils.end_func("Clustering",params["a_func"])
    params["email_response"] += "OK\n"
    params["email_response"] += "\n CSV MachineLearning = "+utils.create_link(params['KEY_IML'],str(params['path_real']),str(params['csvcluster']),str("3"),{})+"\n\n"
    params["email_response"] += time_txt

def E_graphic(params):
    params["a_func"] = utils.get_datetime() #TIME
    try:
        params["email_response"] += "Creating graphic..."
        params['pdfgraphic'] = (params["only_database_name"]+".pdf").replace("(","").replace(")","")
        print "Rscript machine_learning/pdf/pdf_lines.R \""+params['path_real']+params['csvcluster']+"\" \""+params['path_real']+params['pdfgraphic']+"\""
        os.system("Rscript machine_learning/pdf/pdf_lines.R \""+params['path_real']+params['csvcluster']+"\" \""+params['path_real']+params['pdfgraphic']+"\"")
    except Exception as e:
        utils.get_error(e, params)
        raise

    time_txt = utils.end_func("Graphic creation",params["a_func"])
    params["email_response"] += "OK\n"
    params["email_response"] += "\n Graphic = "+utils.create_link(params['KEY_IML'],str(params['path_real']),str(params['pdfgraphic']))+"\n\n"
    params["email_response"] += time_txt
