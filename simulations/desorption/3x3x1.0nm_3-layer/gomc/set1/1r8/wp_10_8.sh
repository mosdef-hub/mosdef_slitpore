#!/bin/bash

#SBATCH --job-name 1r8
#SBATCH -q primary 
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --mem=16G
#SBATCH --constraint=intel
#SBATCH --mail-type=ALL
#SBATCH -o output_%j.out
#SBATCH -e errors_%j.err
#SBATCH -t 336:0:0

echo  "Running on host" hostname
echo  "Time is" date

module swap gnu7/7.3.0 intel/2019


cd /home/brad/Programs/GIT_repositories/mosdef_slitpore_built_for_testing/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc/set1/1r8

GOMC_CPU_GCMC +p4 in.conf > out8a.dat
