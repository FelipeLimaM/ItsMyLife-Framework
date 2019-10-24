import argparse
import os
import time
import spur
import subprocess


# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/compute/api/create_instance.py

def build_outname(params):
    # fixed(compared)_all(hardcoded,pca)_kmeans(kmode).pdf(csv)
    outputname = params["clusters"]+"_"+params["features"]+"_"+params["algorithm"]+"."+params["output"]
    return outputname


def build_command_line(params):
    # example: python main.py --clusterize -g -k 7 -f all -a kmeans -o csv -i "/Backup/benicio@motorola.com/database__20_09_2017_30_day(s).sqlite"
    command_line = "python main.py --clusterize -a "+params["algorithm"]+" -f "+params["features"]

    # numero fixo de clusters
    if params["clusters"] == "fixed":
        command_line += " -k "+params["number"]

    # arquivo de entrada
    command_line += ' -i '+params["filename"]+ ''

    command_line += ' -o '+params["output"]

    command_line += ' -x '+build_outname(params)

    return command_line


def run(params):
    os.popen("cd ../mestrado/machine_learning/; "+ build_command_line(params))
    # subprocess.pop("cd ../mestrado/machine_learning/; "+build_command_line(params), shell=True)
    output_file = subprocess.Popen(["cd ../mestrado/machine_learning/; ", "./lastfile.sh"], stdout=subprocess.PIPE, shell=True)
    return output_file.stdout.read()
#
# def run(params):
#         shell = spur.SshShell(
#             hostname=instance['networkInterfaces'][0]['accessConfigs'][0]['natIP'],
#             username="ubuntu",
#             private_key_file=os.path.expanduser('~/.ssh/id_rsa'),
#             missing_host_key=spur.ssh.MissingHostKey.accept
#         )
#         output_file = ""
#         result = "";
#         cwd = "/home/ubuntu/itsmylife-miletus/cloud/machine_learning/"
#         with shell:
#             print "shell ok"
#             print build_command_line(params)
#             shell.run(["./run.sh"]+build_command_line(params).split(),cwd=cwd,store_pid=True)
#             output_file =  shell.run(["./lastfile.sh"],cwd=cwd,store_pid=False).output
#             print str(os.getcwd()), ">>>>>>"
#
#         final_output_doc = os.getcwd()+"/output_server."+params["output"]
#         scp_command = "scp ubuntu@"+TODOIP+":"
#         scp_command += cwd
#         scp_command += output_file
#         scp_command += " "+ final_output_doc
#
#         scp_command = scp_command.replace("\n"," ")
#         print scp_command
#
#         condition = True
#         while condition:
#             try:
#                 os.system(scp_command)
#                 condition = False
#             except Exception as e:
#                 print e
#
#         print final_output_doc
#         return final_output_doc
