#!/bin/bash

#SBATCH --job-name 10A_NVT
#SBATCH -q primary 
#SBATCH -N 1
#SBATCH -n 8
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

cd /wsu/home/hf/hf68/hf6839/Simulations/Graphene_water/Graphene_water_MoSDeF/mosdef_slitpore/simulations/NVT/3x3x1.0nm_3-layer/gomc

/wsu/home/hf/hf68/hf6839/GOMC-2_6-master/bin/GOMC_CPU_NVT +p8 slit_water_NVT.conf > slit_water_NVT.dat
