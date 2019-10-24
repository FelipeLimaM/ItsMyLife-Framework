import sqlite3, csv, sys, getopt
from operator import itemgetter



def status_machine(modality,lastmodality):
    if modality == lastmodality and (modality == 1  or modality == 32):
        return False
    else:
        return True

def create_list_modality(modality):
    if modality == 1:
        return [1,0,0,0]
    elif modality == 32:
        return [0,1,0,0]
    elif modality == 16:
        return [0,0,1,0]
    elif modality == 8:
        return [0,0,0,1]
    else:
        return [0,0,0,0]


def run (inputfile, outputfile):
    conn = sqlite3.connect(inputfile)
    c0_ = conn.cursor()
    c0 = conn.cursor()
    c1_ = conn.cursor()
    c1 = conn.cursor()
    c2 = conn.cursor()
    c3 = conn.cursor()
    c4 = conn.cursor()
    n_ble = 0
    n_wif = 0
    with open(outputfile, 'w') as csvfile:
        fieldnames = ['timestamp',]
        n_ble = len(c0_.execute('select * from ble_device').fetchall())
        for i in c0.execute('select * from ble_device'):
            fieldnames.append(i[1])
        fieldnames += ['stopped', 'vehicle', 'running', 'walking']
        # n_wifi = len(c1.execute('select * from wifi_device').fetchall())
        # for i in c1.execute('select * from wifi_device'):
        #     fieldnames.append(i[1].encode('utf-8'))
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        lastmodality = 0
        for row in c2.execute('select * from timeline'):
            mylineBLE = [0] * n_ble
            modality = 0
            # mylineWIFI = [0] * n_wifi
            for line in c3.execute('select * from ble where time_id ='+ str(row[0])):
                mylineBLE[line[5]-1]= 1
            # for line in c4.execute('select * from wifi where time_id ='+ str(row[0])):
            #     mylineWIFI[line[5]-1]= 1
            for line in c4.execute('select * from modality where time_id <='+ str(row[0])+' ORDER BY time_id DESC'):
                modality = line[2]
                break
            if status_machine(modality, lastmodality):
                list_include = [row[1],] + mylineBLE + create_list_modality(modality)
                lastmodality = modality
                writer.writerow(list_include)
