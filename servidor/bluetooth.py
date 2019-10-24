import sqlite3, csv, sys, getopt, os
from operator import itemgetter
import utils


class ExportBluetooth():

    def __init__(self, the_list=[], is_blacklist=False):
        self.the_list = the_list
        self.is_blacklist = is_blacklist


    def run(self,inputfile, outputfile):
        if self.the_list:
            self.run_special(inputfile, outputfile)
        else:
            self.run_default(inputfile, outputfile)

    def run_special(self, inputfile, outputfile):
        conn = sqlite3.connect(inputfile)
        c1 = conn.cursor()
        c2 = conn.cursor()
        c3 = conn.cursor()

        # if the list is diferent from void
        my_list= [i[0] for i in c1.execute('select * from ble_device') if i[1] in self.the_list ]

        with open(outputfile, 'w') as csvfile:
            fieldnames = ['timestamp','count']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for row in c2.execute('select * from timeline'):
                count = 0
                for line in c3.execute('select * from ble where time_id ='+ str(row[0])):
                    if (line[5] in my_list and not self.is_blacklist) or ( not(line[5] in my_list) and self.is_blacklist):
                        count+=1
                CSV_line = [row[1],count]
                writer.writerow(CSV_line)

    def run_default(self,inputfile, outputfile):
        conn = sqlite3.connect(inputfile)
        c2 = conn.cursor()
        c3 = conn.cursor()

        with open(outputfile, 'w') as csvfile:
            fieldnames = ['timestamp','count']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for row in c2.execute('select * from timeline'):
                count = 0
                for line in c3.execute('select * from ble where time_id ='+ str(row[0])):
                    count+=1
                CSV_line = [row[1],count]
                writer.writerow(CSV_line)


class BluetoothGraphic():

    def run(self,inputfile, outputfile):
        print "Rscript machine_learning/pdf/pdf_lines_ble.R \""+inputfile+"\" \""+outputfile+"\""
        os.system("Rscript machine_learning/pdf/pdf_lines_ble.R \""+inputfile+"\" \""+outputfile+"\"")
