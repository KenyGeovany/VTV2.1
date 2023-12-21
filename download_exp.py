import subprocess
import sys
from update_persistences import *

# Example
# experiment = "pdhg_rgb_den_gradient 20 5 7 0.01 0.01 0.001 10000"
# model_name = "pdhg_rgb_den_gradient"
# built_data_script = "built_data_g.py"
# name_job = "den_g"
# name_log = "result.log"
# python3 download_exp.py built_data_g.py den_g result.log 123 pdhg_rgb_den_gradient 20 5 7 0.01 0.01 0.001 10000

# Parameters
experiment = " ".join(sys.argv[5:])
model_name = experiment.split(" ")[0]
built_data_script = sys.argv[1]
name_job = sys.argv[2]
name_log = sys.argv[3]
config = set(sys.argv[4])

remote_user="usr"
remote_host="199.800.80.800"
remote_port="8888"

def run_code(instruction):
    process = subprocess.run(instruction, shell=True, check=True, capture_output=True, encoding='utf-8')
    if process.returncode == 0:
        if len(process.stdout)>0:
            update_download_history(process.stdout.split("\n")[-2])
    else:
        update_download_history("Error runing: "+instruction)
    return process.returncode
exist_exp = 0

# Analize if the experiment has been uploaded in the cluster. If it is not return error.
full_experiment = name_job + " " + name_log + " " + experiment
there_exists = 0
with open("persistences/history.txt", mode="r") as history:
    history_lines = history.readlines()
    for i in range(len(history_lines)):
        if full_experiment != history_lines[i][:-1]:
            there_exists += 1
    if there_exists == len(history_lines):
        exist_exp = 1

if exist_exp == 0:
    # Steps
    if str(1) in config:
        instruction = 'rsync -e "ssh -p '+remote_port+'" '+remote_user+'@'+remote_host+':~/models/log/'+name_log+' models/log/'+name_log
        update_download_history("* Descargando log...")
        if run_code(instruction)==0:
            update_download_history("Log descargado.\n")

    if str(2) in config:
        update_download_history("* Descargando archivos...")
        instruction = 'rsync -r -e "ssh -p "' + remote_port + ' ' + remote_user + '@' + remote_host + ':~/models/output/' + model_name + '/ models/output/' + model_name + '/R_' + model_name
        if run_code(instruction)==0:
            update_download_history("Archivos descargados.\n")

    if str(3) in config:
        update_download_history("* Construyendo las tablas...\n")
        instruction = 'cd models/built_data; python3 '+built_data_script+' '+experiment
        if run_code(instruction) == 0:
            update_download_history("\nTablas construidas.\n")
        else:
            # Nota. Si el buit_data_script es incorrecto, entonces la app no lo podrá reconocer
            # solo se podrá saber que existe el erro por que se terminó el runo y no se confirmó
            # la construcción de las tablas, o checando la terminal donde se ejecutó el main.py
            update_download_history("\nError construyendo las tablas. Checar los datos y el built_data_script.\n")
else:
    update_download_history("Experimento no existe: checar los datos y el built_data.\n")
