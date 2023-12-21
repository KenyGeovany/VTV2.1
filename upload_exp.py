import subprocess
import sys
from update_persistences import *

# Example
# experiment = "pdhg_rgb_den_gradient 20 5 7 0.01 0.01 0.001 10000"
# model_name = "pdhg_rgb_den_gradient"
# built_bash_script = "built_bash_g.py"
# name_job = "den_g"
# name_log = "result.log"
# python3 download_exp.py built_bash_g.py den_g result.log 123 pdhg_rgb_den_gradient 20 5 7 0.01 0.01 0.001 10000

# Modificar el bash
experiment = " ".join(sys.argv[5:])
model_name = experiment.split(" ")[0]
built_bash_script = sys.argv[1]
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
            update_upload_history(process.stdout.split("\n")[-2])
    else:
        update_upload_history("Error runing: "+instruction)
    return process.returncode

# Updating bash
if str(1) in config:
    instruction = 'cd models/built_bash; python3 '+ built_bash_script + ' ' + experiment
    print(instruction)
    update_upload_history("* Actualizando bash...")
    if run_code(instruction)==0:
        update_upload_history(model_name + ".sh Actualizado\n")

if str(2) in config:
    instruction = 'ssh -p '+remote_port+' '+remote_user+'@'+remote_host+' "cd models; cd output; if [ ! -d '+model_name+' ]; then mkdir '+model_name+'; fi"' #[ ! -d '+model_name+' ] && mkdir '+model_name+'"'
    update_upload_history("* Creating directory in models/output/...")
    if run_code(instruction)==0:
        update_upload_history("Directory created.\n")

# Updating slurm
if str(3) in config:
    update_upload_history("* Actualizando slurm_general.sh...")
    f_slurm = open("models/slurm_general.sh", "w")
    f_slurm.write("#!/bin/bash\n")
    f_slurm.write("#SBATCH --partition=P0\n")
    f_slurm.write("#SBATCH --job-name="+name_job+"\n")
    f_slurm.write("#SBATCH --output=log/" + name_log + "\n\n")
    f_slurm.write("#SBATCH --ntasks-per-node=32\n")
    f_slurm.write("#SBATCH --ntasks=64\n")
    f_slurm.write("#SBATCH --mem=0\n")
    f_slurm.write("#SBATCH --time=0\n\n")
    f_slurm.write("#SBATCH --mail-type=END,FAIL\n")
    f_slurm.write("#SBATCH --mail-user=usr@gmail.com\n\n")
    f_slurm.write("cd ~/models\n")
    f_slurm.write("source /opt/anaconda3_titan/bin/activate\n")
    f_slurm.write("conda activate env_usr\n")
    f_slurm.write("hostname\n")
    f_slurm.write("date\n")
    f_slurm.write("#!/usr/bin/env python\n")
    f_slurm.write("Tasks=~/models/built_bash/"+model_name+".sh\n")
    f_slurm.write("mpirun.openmpi -np ${SLURM_NTASKS} /opt/ClusterTools/MPI_Scheduler $Tasks  1\n")
    f_slurm.write("date\n")
    f_slurm.close()
    update_upload_history("slurm_general.sh Actualizado.\n")

if str(4) in config:
    instruction = 'cd models; scp -P '+remote_port+' "built_bash/output/'+model_name+'.sh" '+remote_user+'@'+remote_host+':~/models/built_bash/'
    update_upload_history("* Subiendo bash...")
    if run_code(instruction)==0:
        update_upload_history("Bash subido.\n")

if str(5) in config:
    instruction = 'cd models; scp -P '+remote_port+' slurm_general.sh '+remote_user+'@'+remote_host+':~/models/'
    update_upload_history("* Subiendo slurm...")
    if run_code(instruction)==0:
        update_upload_history("Slurm subido.\n")

if str(6) in config:
    instruction = 'ssh -p '+remote_port+' '+remote_user+'@'+remote_host+' "cd models; sbatch slurm_general.sh"'
    if run_code(instruction)==0:
        update_upload_history("\n* Ejecutando slurm...")
        # Actualizar persistences/history.txt con el nuevo experimento que se ha subido exitosamente.
        full_experiment = name_job + " " + name_log + " " + experiment + "\n"
        with open("persistences/history.txt", mode="a") as history:
            history.write(full_experiment)
