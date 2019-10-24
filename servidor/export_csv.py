import sqlite3, csv, sys, getopt
from operator import itemgetter


def run(inputfile, outputfile, bluetooth=False,wifi=False,battery=False,sensorhub=False,optimize=False,
            whitelist_ble=[],whitelist_wifi=[],blacklist_ble=[],blacklist_wifi=[],init_time=None,finish_time=None):
    conn = sqlite3.connect(inputfile)
    count1 = conn.cursor()
    count2 = conn.cursor()
    ble_cursor= conn.cursor()
    wifi_cursor = conn.cursor()
    get_time = conn.cursor()

    n1 = conn.cursor()
    n2 = conn.cursor()
    n3 = conn.cursor()
    n4 = conn.cursor()
    n5 = conn.cursor()

    c2 = conn.cursor()
    c3 = conn.cursor()
    c4 = conn.cursor()
    c5 = conn.cursor()
    c6 = conn.cursor()

    n_ble = 0
    n_wif = 0

    if init_time:
        print "entro pq tem algo"
        for i in get_time.execute('SELECT MIN(_id), MAX(_id) FROM timeline WHERE time >= '+str(init_time)+' AND time <= '+str(finish_time)):
            init_time = i[0]
            finish_time = i[1]
    else:
        print "Nao entro    \o/"
        for i in get_time.execute('SELECT MIN(_id), MAX(_id) FROM timeline'):
            init_time = i[0]
            finish_time = i[1]

    print "INIT TIME :", init_time
    print "FINISH TIME :", finish_time

    if whitelist_ble:
        whitelist_ble= [i[0] for i in ble_cursor.execute('select * from ble_device') if i[1] in whitelist_ble ]
        print "whitelist_ble", whitelist_ble
    if blacklist_ble:
        blacklist_ble= [i[0] for i in ble_cursor.execute('select * from ble_device') if i[1] in blacklist_ble ]
        print "blacklist_ble", blacklist_ble
    if whitelist_wifi:
        whitelist_wifi = [i[0] for i in wifi_cursor.execute('select * from wifi_device') if i[2] in whitelist_wifi ]
        print "whitelist_wifi", whitelist_wifi
    if blacklist_wifi:
        blacklist_wifi= [i[0] for i in wifi_cursor.execute('select * from wifi_device') if i[2] in blacklist_wifi ]
        print "blacklist_wifi", blacklist_wifi

    with open(outputfile, 'w') as csvfile:
        fieldnames = ['timestamp',]
        if bluetooth:
            n_ble = len(count1.execute('select * from ble_device').fetchall())
            for i in n1.execute('select * from ble_device'):
                fieldnames.append(i[1])
        if wifi:
            n_wifi = len(count2.execute('select * from wifi_device').fetchall())
            for i in n2.execute('select * from wifi_device'):
                fieldnames.append(i[1].encode('utf-8'))
        if sensorhub:
            fieldnames.append("sensorhub")
        if battery:
            fieldnames.append("battery")

        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        p_level_battery = 100
        p_status_sensorhub = 0
        p_timestamp = 0
        for row in c2.execute('SELECT * from timeline WHERE _id >= '+str(init_time)+' AND _id <= '+str(finish_time)+ ' ORDER BY time ASC'):
            list_include = [row[1],]
            if bluetooth:
                mylineBLE = [0] * n_ble
                if whitelist_ble or blacklist_ble:
                    for line in c3.execute('select * from ble where time_id ='+ str(row[0])):
                        if (line[5] in whitelist_ble) or not(line[5] in blacklist_ble):
                            mylineBLE[line[5]-1] = 1
                else:
                    # print c3.execute('SELECT _id from ble_device where ble_device._id = ble.mac_id and ble.time_id = '+ str(row[0])).fetchall():
                    #
                    #
                    # raise
                    for line in c3.execute('select * from ble where time_id ='+ str(row[0])):
                        mylineBLE[line[5]-1] = 1
                list_include += mylineBLE
            if wifi:
                mylineWIFI = [0] * n_wifi
                if whitelist_wifi or blacklist_wifi:
                    for line in c4.execute('select * from wifi where time_id ='+ str(row[0])):
                        if (line[5] in whitelist_wifi) or not(line[5] in blacklist_wifi):
                            mylineWIFI[line[5]-1] = 1
                else:
                    for line in c4.execute('select * from wifi where time_id ='+ str(row[0])):
                        mylineWIFI[line[5]-1] = 1
                list_include += mylineWIFI
            if sensorhub:
                mylineSensorHub = 0
                for line in c5.execute('select * from modality where time_id <='+ str(row[0]) +' ORDER BY time_id DESC LIMIT 1'):
                    mylineSensorHub = line[2]
                list_include += [mylineSensorHub]
            if battery:
                for line in c6.execute('select * from battery where time_id <='+ str(row[0]) +' ORDER BY time_id DESC LIMIT 1'):
                    mybatterylevel = line[3]
                list_include += [mybatterylevel]

            if optimize:
                level_battery = list_include[len(list_include)-1]
                status_sensorhub = list_include[len(list_include)-2]
                timestamp = list_include[0]

                if status_sensorhub in [1,32]:
                    if status_sensorhub == p_status_sensorhub:
                        if level_battery != p_level_battery  and level_battery < p_level_battery:
                            # only battery
                            list_include = [timestamp,]
                            if (bluetooth):
                                list_include+= [-1] * n_ble
                            if (wifi):
                                list_include += [-1] * n_wifi
                            if (sensorhub):
                                list_include.append(status_sensorhub)
                            if (battery):
                                list_include.append(level_battery)
                            writer.writerow(list_include)
                    else:
                        writer.writerow(list_include)
                else:
                    writer.writerow(list_include)

                p_level_battery = level_battery
                p_status_sensorhub = status_sensorhub
                p_timestamp = timestamp
            else:
                writer.writerow(list_include)
