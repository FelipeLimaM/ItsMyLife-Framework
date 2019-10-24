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
        fieldnames = ['timestamp','modality']
        MYfile = []
        running = 0
        stopped = 0
        walking = 0
        vehicle = 0
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        previous = 0
        myday = 0
        time = 0

        for i in c0.execute('select * from modality'):
            for time in c1.execute('select * from timeline where _id ='+ str(i[1])):
                print  myday ==0 or (time[1] - myday) > 86400
                if (myday == 0) or (time[1] - myday) > 86400:
                    for (x,y) in  MYfile:
                        if y == 1:
                            stopped +=x
                        if y == 8:
                            walking +=x
                        if y == 16:
                            running +=x
                        if y == 32:
                            vehicle +=x

                    writer.writerow(["stopped", stopped])
                    writer.writerow(["walking", walking])
                    writer.writerow(["running", running])
                    writer.writerow(["vehicle", vehicle])

                    myday = time
                    stopped = 0
                    walking = 0
                    running = 0
                    vehicle = 0


                if previous == 0:
                    previous = time[1]
                MYfile.append([time[1]-previous,i[2]])
                # writer.writerow([time[1]-previous,i[2]])
                previous = time[1]
