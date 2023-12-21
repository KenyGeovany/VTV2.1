#!/bin/bash
#SBATCH --partition=C0
#SBATCH --job-name=den_g
#SBATCH --output=log/result1.log

#SBATCH --ntasks-per-node=32
#SBATCH --ntasks=64
#SBATCH --mem=0
#SBATCH --time=0

#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=keny.chin@cimat.mx

cd /home/est_posgrado_keny.chin/models
source /opt/anaconda3_titan/bin/activate
conda activate envkeny
hostname
date
#!/usr/bin/env python
Tasks=/home/est_posgrado_keny.chin/models/built_bash/pdhg_rgb_den_gradient.sh
mpirun.openmpi -np ${SLURM_NTASKS} /opt/ClusterTools/MPI_Scheduler $Tasks  1
date
