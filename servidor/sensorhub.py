import sqlite3, csv, sys, getopt, os
from operator import itemgetter


class ExportSensorHub():
    '''Class to get only SensorHub information from backup database.'''
    def run(self,inputfile, outputfile):
        conn = sqlite3.connect(inputfile)
        c2 = conn.cursor()
        c3 = conn.cursor()

        with open(outputfile, 'w') as csvfile:
            fieldnames = ['timestamp','status']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for row in c2.execute('select * from modality'):
                # CSV_line = [0] * len(fieldnames)
                for time in c3.execute('select * from timeline where _id ='+ str(row[1])):
                    CSV_line = [time[1],row[2]]
                writer.writerow(CSV_line)

class SensorHubGraphic():
    '''Build Graphic from file created by ExportSensorHub() '''
    def run(self,inputfile, outputfile):
        print "Rscript machine_learning/pdf/pdf_lines_sensor_hub.R \""+inputfile+"\" \""+outputfile+"\""
        os.system("Rscript machine_learning/pdf/pdf_lines_sensor_hub.R \""+inputfile+"\" \""+outputfile+"\"")
