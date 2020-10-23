#!/bin/bash

#SBATCH --job-name Psat_1r2
#SBATCH -q primary
#SBATCH -N 1
#SBATCH -n 16
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

cd /wsu/home/hf/hf68/hf6839/Simulations/Graphene_water/Graphene_water_MoSDeF/mosdef_slitpore/simulations/Psat_SPCE_298K/set1/1r2

/wsu/home/hf/hf68/hf6839/GOMC-2_6-master/bin/GOMC_CPU_GEMC +p16 water_GEMC_NVT_298K.conf > water_GEMC_NVT_298K.dat
