{% extends base_script %}
{% block project_header %}
#PBS -l walltime=95:59:00,mem=100gb
module purge
module load intel/cluster/2018
module load mkl
module load fftw
module load conda
source activate /home/siepmann/singh891/anaconda3/envs/slitpore37
date >> execution.log
{{ super() }}
{% endblock %}

