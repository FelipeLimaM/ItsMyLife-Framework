import getopt
import subprocess
import sys
import os

class Pdf_generator(object):

    def __init__(self, kind=0, file_="", zip_file="",path=""):
        super(Pdf_generator, self).__init__()
        self.kind = kind
        self.file_ = file_
        self.path = path
        self.zip_file = zip_file

    def file_title_parse(self):
        list_option = self.file_.split("_")
        return {
            "number" : list_option[1],
            "PreProcessing": list_option[2],
            "TypeClusterization": list_option[3],
            "???": list_option[4].split(".")[0]
        }


    def build(self):
        info = self.file_title_parse()
        output = self.zip_file[:-4]+"_"+info["number"]+"_lines.pdf"
        try:
            print ("Create graphic...")
            if self.kind == 1: # Grafico de linhas sem o modality
                os.system("Rscript pdf/pdf_lines.R "+ self.zip_file+" "+self.file_+" "+output)
            if self.kind == 2: # Grafico de pontos sem o modality
                os.system("Rscript pdf/pdf_points.R "+ self.zip_file+" "+self.file_+" "+output)

            if self.kind == 10: # Grafico de linhas com o modality
                os.system("Rscript pdf/pdf_lines_modality.R "+ self.zip_file+" "+self.file_+" "+output)


            print ("Ok")
        except Exception :
            print ("Problem :(")
            return
