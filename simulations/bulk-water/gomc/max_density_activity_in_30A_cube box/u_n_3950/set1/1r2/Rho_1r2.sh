#!/bin/bash

#SBATCH --job-name Rho_1r2
#SBATCH -q primary
#SBATCH -N 1
#SBATCH -n 2
#SBATCH --mem=16G
#SBATCH --constraint=intel
#SBATCH --mail-type=ALL
#SBATCH --mail-user=bc118@wayne.edu
#SBATCH -o output_%j.out
#SBATCH -e errors_%j.err
#SBATCH -t 336:0:0

echo  "Running on host" hostname
echo  "Time is" date
module swap gnu7/7.3.0 intel/2019

echo  "Time is" date

cd /wsu/home/hf/hf68/hf6839/Simulations/Graphene_water/Graphene_water_MoSDeF/mosdef_slitpore/simulations/bulk-water/gomc/max_cap_conc_and_P_in_SPCE/u_n_3950/set1/1r2

/wsu/home/hf/hf68/hf6839/GOMC-2_6-master/bin/GOMC_CPU_GCMC +p2 water_GCMC.conf > water_GCMC.dat
