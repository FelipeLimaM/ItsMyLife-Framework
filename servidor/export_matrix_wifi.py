import sqlite3, csv, sys, getopt
from operator import itemgetter





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
        # n_ble = len(c0_.execute('select * from ble_device').fetchall())
        # for i in c0.execute('select * from ble_device'):
        #     fieldnames.append(i[1])
        n_wifi = len(c1.execute('select * from wifi_device').fetchall())
        for i in c1.execute('select * from wifi_device'):
            fieldnames.append(i[1].encode('utf-8'))
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        previous_line_wifi = [0] * n_wifi
        for row in c2.execute('select * from timeline'):

            # mylineBLE = [0] * n_ble
            mylineWIFI = [0] * n_wifi
            # for line in c3.execute('select * from ble where time_id ='+ str(row[0])):
            #     mylineBLE[line[5]-1]= 1
            for line in c4.execute('select * from wifi where time_id ='+ str(row[0])):
                mylineWIFI[line[5]-1]= 1
            if (sum(mylineWIFI)>0):
                list_include = [row[1],] + mylineWIFI #+ mylineBLE
                previous_line_wifi = mylineWIFI
            else:
                list_include = [row[1],] + previous_line_wifi #+ mylineBLE
            writer.writerow(list_include)
