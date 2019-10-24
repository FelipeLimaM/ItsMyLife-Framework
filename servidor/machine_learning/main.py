# recebe o nome da pasta e qual funcao deseja
# entra na pasta e unzipa o arquivo
# passa os dados pelo pre-processamento (ou nao)
# passa os dados para o cluster
# escreve o resultado
# zipa os arquivos
import sys
import os
import pandas as pd
import zipfile as zf
import pre_processing as pre
from clustering import Clustering
import getopt
import subprocess
import pdf_generator as pdf



info = '''
Parameters:
    -h
        Show options.
    -i
        Input file, in which the format varies according to the selected function.

Functions:
    --zip
        Required parameters:
            -i <file.csv>

        Optional parameters:

        Make magic kkk.

    --clusterize
        Required parameters:
            -i <file.csv>
        Optional parameters:


            -g  Create graphic with lines.

            -G  Create graphic with points.
            -M  Show modality information in graphic.

            -m <model_name>     Model used in the PreProcessing classifier:
                                -> "all" (default) -> all beacons will be used
                                -> "simple" -> just hardcoded fixed beacons will be used

            -k <number_of_clusters>     Number of clusters used to do the clustering
                                        If not set, a comparation to find the best k will be used

            -f <features>   Which features will be used
                            -> "b" (default) -> just beacons will be used
                            -> "b,w" -> beacons and wifi will be used
            -a <type>   Clusterization Algorithm: kmeans | kmodes.

        Make magic kkk.

'''




def main(argv):
    inputfile = ''

    functions = ["help","feature_vector", "clusterize","csv_modality", "csv_beacons"] # only example
    # Check param in program call
    try:

        opts, args = getopt.getopt(argv,"i:gGMm:k:f:a:h",functions) #A letter plus ":" -> param with input  | A letter without ":" -> It's kind flag
    except getopt.GetoptError:
        print ("ops1")
        sys.exit(2)

    if not opts:
        print ("ops2")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            inputfile = arg
        elif opt in ("-h", "--help"):
            print (info)
            sys.exit(2)
    if sum(1 for x in argv if "--" in x) != 1:
        print ("Insert only a function as parameter \n\n Use --help or -h to get help")
        sys.exit(2)

    execute_func(opts,inputfile)


def execute_func(opts,inputfile):
    func = [item for item in opts if "--" in item[0]][0]
    if "--feature_vector" in func:
        pass


    if "--clusterize" in func:
        build_graphic = False
        kind_graphic = 0
        modality = False
        k="compare_k"
        algorithm = "kmeans"
        model="all"
        features="b" # just beacons


        for opt, arg in opts:
            if opt == '-g':
                build_graphic = True
                kind_graphic = 1

            if opt == '-G':
                build_graphic = True
                kind_graphic = 2


            if opt == '-M' and build_graphic:
                kind_graphic *= 10
                modality = True


            if opt == '-A':
                algorithm = arg


            if opt == '-m':
                model = arg

            if opt == '-k':
                try:
                    k = int(arg)
                except:
                    print ("k is not a valid int value")
                    sys.exit(2)

            if opt == '-f':
                features = arg



        current_dir = os.getcwd()
        # caminho para a pasta que contem o zip e os graficos
        path = os.path.join(current_dir, 'results/'+inputfile+'/')


        zipname = os.path.join(path, inputfile+'.zip')

        with zf.ZipFile(zipname,'a') as myzip:
            pre_processing = None
            df = None
            # tenta abrir a matriz full -> sem modality
            try:
                with myzip.open('full_matrix.csv') as myfile:
                    df = pd.read_csv(myfile, sep=',', header=0, index_col=0)
                    pre_processing = pre.PreProcessing(df,model=model,features=features)
                    df = pre_processing.build()
                    outputfile = model+".csv"
            # so consegue abrir a matriz reduced -> com modality
            except:

                try:
                    # matriz normalizada ja esta salva
                    with myzip.open(model+'_normalized.csv') as myfile:
                        # nao vai fazer a normalizacao de novo, vai usar normalized pronta
                        # NAO PRECISA DE PRE PROCESSAMENTO
                        df = pd.read_csv(myfile, sep=',', header=0, index_col=0)
                        print ("number of features = {}".format(df.shape[1]))
                        outputfile = model+"_normalized.csv"

                # matriz normalizada ainda nao esta salva
                # vai ocorrer a normalizacao e depois a matriz resultante sera salva
                except:
                    with myzip.open('reduced_matrix.csv') as myfile:

                        df = pd.read_csv(myfile, sep=',', header=0, index_col=0)
                        pre_processing = pre.PreProcessing(df,norm=True,model=model,features=features)
                        df = pre_processing.build()
                        print ("number of features = {}".format(df.shape[1]))
                        outputfile = model+"_normalized.csv"
                        # salva matriz normalizada resultante no zip
                        df.to_csv(model+"_normalized.csv", sep=',', encoding='utf-8', header=True)
                        myzip.write(model+"_normalized.csv")
                        os.remove(model+"_normalized.csv")

            # clusterizacao
            n_clusters = 0
            labels = None
            if k == "compare_k":
                labels, n_clusters = Clustering(df).clusterize()
                outputfile = "labels_"+str(n_clusters)+"_clusters_compared_"+outputfile
            else:
                labels, n_clusters = Clustering(df, mode="fixed_k", n_clusters=k).clusterize()
                outputfile = "labels_"+str(n_clusters)+"_clusters_fixed_"+outputfile

            timestamp = list(df.index)
            with open(outputfile, 'w') as f:
            	f.write("seconds,clusters\n")
            	for i in range(len(labels)):
                    f.write("{},{}\n".format(timestamp[i],labels[i]))


            myzip.write(outputfile)
            os.remove(outputfile)

            if modality:
                m = os.path.join(path, "modality.csv")
                pre_processing.get_modalities().to_csv(m, sep=',', encoding='utf-8')
                myzip.write(m, os.path.basename(m))
                os.remove(m)

        if build_graphic:
            pdf.Pdf_generator(kind=kind_graphic, file_=outputfile, path=path, zip_file=zipname).build()


    # salva um csv so com a timestamp e os modalities (valor de 0 a 3)
    if "--csv_modality" in func:
        current_dir = os.getcwd()
        # caminho para a pasta que contem o zip e os graficos
        path = os.path.join(current_dir, 'results/'+inputfile+'/')

        zipname = os.path.join(path, inputfile+'.zip')
        with zf.ZipFile(zipname,'a') as myzip:
            with myzip.open('reduced_matrix.csv') as myfile:
                # le somente as colunas dos modality
                df = pd.read_csv(myfile, sep=',', header=0, index_col=0, usecols=["timestamp","walking", "stopped", "vehicle", "running"])
                # transforma as 4 colunas em uma coluna numerica
                df["modality"] = df.idxmax(axis=1).astype('category').cat.codes
                df = df.set_index('seconds')
                # escreve csv
                df["modality"].to_csv("modality.csv", sep=',', encoding='utf-8', header=True)
                myzip.write("modality.csv")

    # salva um csv so com a timestamp e os beacons, sem linhas zeradas, bateria, wifi, modality
    if "--csv_beacons" in func:
        current_dir = os.getcwd()
        # caminho para a pasta que contem o zip e os graficos
        path = os.path.join(current_dir, 'results/'+inputfile+'/')


        zipname = os.path.join(path, inputfile+'.zip')
        with zf.ZipFile(zipname,'a') as myzip:
            with myzip.open('reduced_matrix.csv') as myfile:
                df = pd.read_csv(myfile, sep=',', header=0, index_col=0)
                # le somente as colunas dos beacons
                beacons=df.loc[:,: pre.macRegex(df)]
                beacons = pre.removeZeroLines(beacons)
                df.to_csv("beacons.csv", sep=',', encoding='utf-8', header=True)
                myzip.write("beacons.csv")
                os.remove("beacons.csv")











if __name__ == "__main__":
    main(sys.argv[1:])
