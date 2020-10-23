import numpy as np
import matplotlib.pyplot as plt
import csv as csv
import pandas as pd
import matplotlib.ticker as ticker
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
from scipy.stats import linregress
import seaborn as sns
from matplotlib.colors import ListedColormap


sns.color_palette("deep",2)

E_vs_P_Psat_saving_name = "E_vs_P_div_Psat.pdf"

axis_Label_font_size = 22
legend_font_size = 16
axis_number_font_size = 18

PointSizes = 8
ConnectionLineSizes = 2
Reg_Density_Linestyle = '--'  #'-' =  solid, '--' = dashed, ':'= dotted
Critical_Density_Linestyle = None


Psat_data_file = '../Psat_SPCE_298K/gomc/analysis/SPCE_Pvap_at_298K_df.csv'
Psat_data = pd.read_csv(Psat_data_file, sep=',', header=0, na_values='NaN',
						usecols=[0,1], index_col=False)

Psat_data = pd.DataFrame(Psat_data)
print(Psat_data)

Psat_SPEC_data_bar = Psat_data.loc[:,'Avg_Pvap_bar']
Psat_SPEC_data_bar = list(Psat_SPEC_data_bar)[0]
print('Psat_SPEC_data_bar = '+str(Psat_SPEC_data_bar))
Psat_at_298K = Psat_SPEC_data_bar

#**************
# P vs T plot ranges (start)
#*************
Psat_div_Po_min = 0.001
Psat_div_Po_max = 30

E_per_nm_sq_10A_min = -1.9
E_per_nm_sq_10A_max = 17
E_per_nm_sq_10A_step = 5

E_per_nm_sq_16A_min = -4.8
E_per_nm_sq_16A_max = 34
E_per_nm_sq_16A_step = 10

#**************
# P vs T plot ranges (end)
#*************

Chemical_name = 'grapene_water'

flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
my_cmap = ListedColormap(sns.color_palette(flatui).as_hex())
WSU_color = '#ff7f0e'
NDU_color = '#1f77b4'


#********************************
#  Cassandra variables (start)
#********************************
No_independant_run_sets_per_10A_ads_Cass = 3   # interger only
No_independant_run_sets_per_16A_ads_Cass = 3   # interger only
No_independant_run_sets_per_10A_des_Cass = 3   # interger only
No_independant_run_sets_per_16A_des_Cass = 3   # interger only

#********************************
#  Cassandra variables (end)
#********************************


#********************************
#  File importing (start)
#********************************
#import Gubbins rescaled data
calc_data_reading_name_10A_ads_Gubbins = 'Gubbins_extracted_data/10_ads_rescaled.csv'
calc_data_reading_name_16A_ads_Gubbins = 'Gubbins_extracted_data/16_ads_rescaled.csv'

calc_data_reading_name_10A_des_Gubbins = 'Gubbins_extracted_data/10_des_rescaled.csv'
calc_data_reading_name_16A_des_Gubbins = 'Gubbins_extracted_data/16_des_rescaled.csv'

calc_data_10A_ads_Gubbins = pd.read_csv(calc_data_reading_name_10A_ads_Gubbins,  sep=',')
calc_data_10A_ads_Gubbins_df = pd.DataFrame(calc_data_10A_ads_Gubbins)
print(calc_data_10A_ads_Gubbins_df )
calc_data_16A_ads_Gubbins = pd.read_csv(calc_data_reading_name_16A_ads_Gubbins,  sep=',')
calc_data_16A_ads_Gubbins_df = pd.DataFrame(calc_data_16A_ads_Gubbins)

calc_data_10A_des_Gubbins = pd.read_csv(calc_data_reading_name_10A_des_Gubbins,  sep=',')
calc_data_10A_des_Gubbins_df = pd.DataFrame(calc_data_10A_des_Gubbins)

calc_data_16A_des_Gubbins = pd.read_csv(calc_data_reading_name_16A_des_Gubbins,  sep=',')
calc_data_16A_des_Gubbins_df = pd.DataFrame(calc_data_16A_des_Gubbins)

Psat_ratio_10A_ads_Gubbins = calc_data_10A_ads_Gubbins_df.loc[:, 'P_div_Po' ].tolist()
Psat_ratio_16A_ads_Gubbins = calc_data_16A_ads_Gubbins_df.loc[:, 'P_div_Po' ].tolist()
Psat_ratio_10A_des_Gubbins = calc_data_10A_des_Gubbins_df.loc[:, 'P_div_Po' ].tolist()
Psat_ratio_16A_des_Gubbins = calc_data_16A_des_Gubbins_df.loc[:, 'P_div_Po' ].tolist()


Avg_E_No_water_per_nm_sq_10A_ads_Gubbins = calc_data_10A_ads_Gubbins_df.loc[:, 'nmols_per_nm^2' ].tolist()
Avg_E_No_water_per_nm_sq_16A_ads_Gubbins = calc_data_16A_ads_Gubbins_df.loc[:, 'nmols_per_nm^2' ].tolist()
Avg_E_No_water_per_nm_sq_10A_des_Gubbins = calc_data_10A_des_Gubbins_df.loc[:, 'nmols_per_nm^2' ].tolist()
Avg_E_No_water_per_nm_sq_16A_des_Gubbins = calc_data_16A_des_Gubbins_df.loc[:, 'nmols_per_nm^2' ].tolist()


#import GOMC data

calc_data_reading_name_10A_ads = '../adsorption/3x3x1.0nm_3-layer/gomc/analysis/adsorption_10A_slit_df.txt'
calc_data_reading_name_16A_ads = '../adsorption/3x3x1.6nm_3-layer/gomc/analysis/adsorption_16A_slit_df.txt'

calc_data_reading_name_10A_des = '../desorption/3x3x1.0nm_3-layer/gomc/analysis/desorption_10A_slit_df.txt'
calc_data_reading_name_16A_des = '../desorption/3x3x1.6nm_3-layer/gomc/analysis/desorption_16A_slit_df.txt'

calc_data_10A_ads = pd.read_csv(calc_data_reading_name_10A_ads,  sep='\s+', index_col=0)
calc_data_10A_ads_df = pd.DataFrame(calc_data_10A_ads)

calc_data_16A_ads = pd.read_csv(calc_data_reading_name_16A_ads,  sep='\s+', index_col=0)
calc_data_16A_ads_df = pd.DataFrame(calc_data_16A_ads)

calc_data_10A_des = pd.read_csv(calc_data_reading_name_10A_des,  sep='\s+', index_col=0)
calc_data_10A_des_df = pd.DataFrame(calc_data_10A_des)

calc_data_16A_des = pd.read_csv(calc_data_reading_name_16A_des,  sep='\s+', index_col=0)
calc_data_16A_des_df = pd.DataFrame(calc_data_16A_des)

Psat_ratio_10A_ads = calc_data_10A_ads_df.loc[:, 'Psat_ratio' ].tolist()
Psat_ratio_16A_ads = calc_data_16A_ads_df.loc[:, 'Psat_ratio' ].tolist()
Psat_ratio_10A_des = calc_data_10A_des_df.loc[:, 'Psat_ratio' ].tolist()
Psat_ratio_16A_des = calc_data_16A_des_df.loc[:, 'Psat_ratio' ].tolist()


Avg_E_No_water_per_nm_sq_10A_ads = calc_data_10A_ads_df.loc[:, 'Avg_E_No_water_per_nm_sq' ].tolist()
Avg_E_No_water_per_nm_sq_16A_ads = calc_data_16A_ads_df.loc[:, 'Avg_E_No_water_per_nm_sq' ].tolist()
Avg_E_No_water_per_nm_sq_10A_des = calc_data_10A_des_df.loc[:, 'Avg_E_No_water_per_nm_sq' ].tolist()
Avg_E_No_water_per_nm_sq_16A_des = calc_data_16A_des_df.loc[:, 'Avg_E_No_water_per_nm_sq' ].tolist()

StdDev_E_No_water_per_nm_sq_10A_ads = calc_data_10A_ads_df.loc[:, 'StdDev_E_No_water_per_nm_sq' ].tolist()
StdDev_E_No_water_per_nm_sq_16A_ads = calc_data_16A_ads_df.loc[:, 'StdDev_E_No_water_per_nm_sq' ].tolist()
StdDev_E_No_water_per_nm_sq_10A_des = calc_data_10A_des_df.loc[:, 'StdDev_E_No_water_per_nm_sq' ].tolist()
StdDev_E_No_water_per_nm_sq_16A_des = calc_data_16A_des_df.loc[:, 'StdDev_E_No_water_per_nm_sq' ].tolist()


#import Cassandra data
calc_data_reading_name_10A_ads_Cass = '../adsorption/3x3x1.0nm_3-layer/cassandra/analysis/results.csv'
calc_data_reading_name_16A_ads_Cass = '../adsorption/3x3x1.6nm_3-layer/cassandra/analysis/results.csv'

calc_data_reading_name_10A_des_Cass = '../desorption/3x3x1.0nm_3-layer/cassandra/analysis/results.csv'
calc_data_reading_name_16A_des_Cass = '../desorption/3x3x1.6nm_3-layer/cassandra/analysis/results.csv'

calc_reading_name_pressure_Cass = '../bulk-water/cassandra/analysis/results_nd.csv'

calc_data_10A_ads_Cass = pd.read_csv(calc_data_reading_name_10A_ads_Cass,  sep=',', index_col=0)
calc_data_10A_ads_Cass_df = pd.DataFrame(calc_data_10A_ads_Cass)

calc_data_16A_ads_Cass = pd.read_csv(calc_data_reading_name_16A_ads_Cass,  sep=',', index_col=0)
calc_data_16A_ads_Cass_df = pd.DataFrame(calc_data_16A_ads_Cass)

calc_data_10A_des_Cass = pd.read_csv(calc_data_reading_name_10A_des_Cass,  sep=',', index_col=0)
calc_data_10A_des_Cass_df = pd.DataFrame(calc_data_10A_des_Cass)

calc_data_16A_des_Cass = pd.read_csv(calc_data_reading_name_16A_des_Cass,  sep=',', index_col=0)
calc_data_16A_des_Cass_df = pd.DataFrame(calc_data_16A_des_Cass)

calc_data_pressure_Cass = pd.read_csv(calc_reading_name_pressure_Cass,  sep=',', index_col=0)
calc_data_pressure_Cass_df = pd.DataFrame(calc_data_pressure_Cass)


mu_kJ_per_mol_10A_ads_Cass = calc_data_10A_ads_Cass_df.loc[:, 'mu-cassandra_kJmol' ].tolist()
mu_kJ_per_mol_16A_ads_Cass = calc_data_16A_ads_Cass_df.loc[:, 'mu-cassandra_kJmol' ].tolist()
mu_kJ_per_mol_10A_des_Cass = calc_data_10A_des_Cass_df.loc[:, 'mu-cassandra_kJmol' ].tolist()
mu_kJ_per_mol_16A_des_Cass = calc_data_16A_des_Cass_df.loc[:, 'mu-cassandra_kJmol' ].tolist()

Avg_E_No_water_per_nm_sq_10A_ads_Cass = calc_data_10A_ads_Cass_df.loc[:, 'nmols_per_nm^2' ].tolist()
Avg_E_No_water_per_nm_sq_16A_ads_Cass = calc_data_16A_ads_Cass_df.loc[:, 'nmols_per_nm^2' ].tolist()
Avg_E_No_water_per_nm_sq_10A_des_Cass = calc_data_10A_des_Cass_df.loc[:, 'nmols_per_nm^2' ].tolist()
Avg_E_No_water_per_nm_sq_16A_des_Cass = calc_data_16A_des_Cass_df.loc[:, 'nmols_per_nm^2' ].tolist()


mu_kJ_per_mol_Cass = calc_data_pressure_Cass_df.loc[:, 'mu-cassandra_kJmol' ].tolist()
Avg_pressure_bar_Cass = calc_data_pressure_Cass_df.loc[:, 'press_bar' ].tolist()

mu_kJ_per_mol_and_P_dict = {}

for i in range(0, len(mu_kJ_per_mol_Cass)):
    P_iteration = Avg_pressure_bar_Cass[i]
    mu_kJ_per_mol_Cass_iteration = mu_kJ_per_mol_Cass[i]
    mu_kJ_per_mol_and_P_dict.update({mu_kJ_per_mol_Cass_iteration : P_iteration})


slope_Cass, intercept_Cass, r_value_Cass, p_value_Cass, stderr_Cass = linregress(list(mu_kJ_per_mol_and_P_dict.keys()),
                                                         y = np.log(list(mu_kJ_per_mol_and_P_dict.values())))

No_runs_per_set_10A_ads_Cass = int( len(mu_kJ_per_mol_10A_ads_Cass) / No_independant_run_sets_per_10A_ads_Cass )
No_runs_per_set_16A_ads_Cass = int( len(mu_kJ_per_mol_16A_ads_Cass) / No_independant_run_sets_per_16A_ads_Cass )
No_runs_per_set_10A_des_Cass = int( len(mu_kJ_per_mol_10A_des_Cass) / No_independant_run_sets_per_10A_des_Cass )
No_runs_per_set_16A_des_Cass = int( len(mu_kJ_per_mol_16A_des_Cass) / No_independant_run_sets_per_16A_des_Cass )


# new Cassandra organization
Avg_of_E_per_area_10A_ads_Cass_list = []
mu_kJ_per_mol_10A_ads_Cass_list = []
P_div_Po_10A_ads_Cass_list = []
Avg_mu_kJ_per_mol_10A_ads_Cass_list = []
Std_Dev_E_per_area_10A_ads_Cass_list = []

mu_kJ_per_mol_10A_ads_Cass_unique_list = []
for k in range(0, len(mu_kJ_per_mol_10A_ads_Cass)):
    if mu_kJ_per_mol_10A_ads_Cass[k] not in mu_kJ_per_mol_10A_ads_Cass_unique_list:
        mu_kJ_per_mol_10A_ads_Cass_unique_list.append(mu_kJ_per_mol_10A_ads_Cass[k])


for i in range(0, No_runs_per_set_10A_ads_Cass):
    Average_of_mu_list_iteration = []
    Average_of_E_per_area_list_iteration = []
    for j in range(0, No_independant_run_sets_per_10A_ads_Cass):
        iteration_line = i*No_independant_run_sets_per_10A_ads_Cass +j
        Average_of_mu_list_iteration.append(mu_kJ_per_mol_10A_ads_Cass[iteration_line])
        Average_of_E_per_area_list_iteration.append(Avg_E_No_water_per_nm_sq_10A_ads_Cass[iteration_line])

    Avg_of_E_per_area_10A_ads_Cass_list.append(np.mean(Average_of_E_per_area_list_iteration))
    Avg_mu_kJ_per_mol_10A_ads_Cass_list.append(np.mean(Average_of_mu_list_iteration))
    Calc_P_div_Po = np.mean(np.exp(Avg_mu_kJ_per_mol_10A_ads_Cass_list[i] * slope_Cass + intercept_Cass)) / Psat_at_298K
    P_div_Po_10A_ads_Cass_list.append(Calc_P_div_Po)
    Std_Dev_E_per_area_10A_ads_Cass_list.append(np.std(Average_of_E_per_area_list_iteration, ddof=1))



zipped_lists = zip(P_div_Po_10A_ads_Cass_list, Avg_of_E_per_area_10A_ads_Cass_list, Std_Dev_E_per_area_10A_ads_Cass_list)
sorted_pairs = sorted(zipped_lists)
tuples = zip(*sorted_pairs)
P_div_Po_10A_ads_Cass_list, Avg_of_E_per_area_10A_ads_Cass_list, Std_Dev_E_per_area_10A_ads_Cass_list  = [ list(tuple) for tuple in tuples]




Avg_of_E_per_area_10A_des_Cass_list = []
mu_kJ_per_mol_10A_des_Cass_list = []
P_div_Po_10A_des_Cass_list = []
Avg_mu_kJ_per_mol_10A_des_Cass_list = []
Std_Dev_E_per_area_10A_des_Cass_list = []

mu_kJ_per_mol_10A_des_Cass_unique_list = []
for k in range(0, len(mu_kJ_per_mol_10A_des_Cass)):
    if mu_kJ_per_mol_10A_des_Cass[k] not in mu_kJ_per_mol_10A_des_Cass_unique_list:
        mu_kJ_per_mol_10A_des_Cass_unique_list.append(mu_kJ_per_mol_10A_des_Cass[k])


for i in range(0, No_runs_per_set_10A_des_Cass):
    Average_of_mu_list_iteration = []
    Average_of_E_per_area_list_iteration = []
    for j in range(0, No_independant_run_sets_per_10A_des_Cass):
        iteration_line = i*No_independant_run_sets_per_10A_des_Cass +j
        Average_of_mu_list_iteration.append(mu_kJ_per_mol_10A_des_Cass[iteration_line])
        Average_of_E_per_area_list_iteration.append(Avg_E_No_water_per_nm_sq_10A_des_Cass[iteration_line])

    Avg_of_E_per_area_10A_des_Cass_list.append(np.mean(Average_of_E_per_area_list_iteration))
    Avg_mu_kJ_per_mol_10A_des_Cass_list.append(np.mean(Average_of_mu_list_iteration))
    Calc_P_div_Po = np.mean(np.exp(Avg_mu_kJ_per_mol_10A_des_Cass_list[i] * slope_Cass + intercept_Cass)) / Psat_at_298K
    P_div_Po_10A_des_Cass_list.append(Calc_P_div_Po)
    Std_Dev_E_per_area_10A_des_Cass_list.append(np.std(Average_of_E_per_area_list_iteration, ddof=1))


zipped_lists = zip(P_div_Po_10A_des_Cass_list, Avg_of_E_per_area_10A_des_Cass_list, Std_Dev_E_per_area_10A_des_Cass_list)
sorted_pairs = sorted(zipped_lists)
tuples = zip(*sorted_pairs)
P_div_Po_10A_des_Cass_list, Avg_of_E_per_area_10A_des_Cass_list, Std_Dev_E_per_area_10A_des_Cass_list  = [ list(tuple) for tuple in tuples]



Avg_of_E_per_area_16A_ads_Cass_list = []
mu_kJ_per_mol_16A_ads_Cass_list = []
P_div_Po_16A_ads_Cass_list = []
Avg_mu_kJ_per_mol_16A_ads_Cass_list = []
Std_Dev_E_per_area_16A_ads_Cass_list = []

mu_kJ_per_mol_16A_ads_Cass_unique_list = []
for k in range(0, len(mu_kJ_per_mol_16A_ads_Cass)):
    if mu_kJ_per_mol_16A_ads_Cass[k] not in mu_kJ_per_mol_16A_ads_Cass_unique_list:
        mu_kJ_per_mol_16A_ads_Cass_unique_list.append(mu_kJ_per_mol_16A_ads_Cass[k])


for i in range(0, No_runs_per_set_16A_ads_Cass):
    Average_of_mu_list_iteration = []
    Average_of_E_per_area_list_iteration = []
    for j in range(0, No_independant_run_sets_per_16A_ads_Cass):
        iteration_line = i*No_independant_run_sets_per_16A_ads_Cass +j
        Average_of_mu_list_iteration.append(mu_kJ_per_mol_16A_ads_Cass[iteration_line])
        Average_of_E_per_area_list_iteration.append(Avg_E_No_water_per_nm_sq_16A_ads_Cass[iteration_line])

    Avg_of_E_per_area_16A_ads_Cass_list.append(np.mean(Average_of_E_per_area_list_iteration))
    Avg_mu_kJ_per_mol_16A_ads_Cass_list.append(np.mean(Average_of_mu_list_iteration))
    Calc_P_div_Po = np.mean(np.exp(Avg_mu_kJ_per_mol_16A_ads_Cass_list[i] * slope_Cass + intercept_Cass)) / Psat_at_298K
    P_div_Po_16A_ads_Cass_list.append(Calc_P_div_Po)
    Std_Dev_E_per_area_16A_ads_Cass_list.append(np.std(Average_of_E_per_area_list_iteration, ddof=1))


zipped_lists = zip(P_div_Po_16A_ads_Cass_list, Avg_of_E_per_area_16A_ads_Cass_list, Std_Dev_E_per_area_16A_ads_Cass_list)
sorted_pairs = sorted(zipped_lists)
tuples = zip(*sorted_pairs)
P_div_Po_16A_ads_Cass_list, Avg_of_E_per_area_16A_ads_Cass_list, Std_Dev_E_per_area_16A_ads_Cass_list  = [ list(tuple) for tuple in tuples]




Avg_of_E_per_area_16A_des_Cass_list = []
mu_kJ_per_mol_16A_des_Cass_list = []
P_div_Po_16A_des_Cass_list = []
Avg_mu_kJ_per_mol_16A_des_Cass_list = []
Std_Dev_E_per_area_16A_des_Cass_list = []

mu_kJ_per_mol_16A_des_Cass_unique_list = []
for k in range(0, len(mu_kJ_per_mol_16A_des_Cass)):
    if mu_kJ_per_mol_16A_des_Cass[k] not in mu_kJ_per_mol_16A_des_Cass_unique_list:
        mu_kJ_per_mol_16A_des_Cass_unique_list.append(mu_kJ_per_mol_16A_des_Cass[k])


for i in range(0, No_runs_per_set_16A_des_Cass):
    Average_of_mu_list_iteration = []
    Average_of_E_per_area_list_iteration = []
    for j in range(0, No_independant_run_sets_per_16A_des_Cass):
        iteration_line = i*No_independant_run_sets_per_16A_des_Cass +j
        Average_of_mu_list_iteration.append(mu_kJ_per_mol_16A_des_Cass[iteration_line])
        Average_of_E_per_area_list_iteration.append(Avg_E_No_water_per_nm_sq_16A_des_Cass[iteration_line])

    Avg_of_E_per_area_16A_des_Cass_list.append(np.mean(Average_of_E_per_area_list_iteration))
    Avg_mu_kJ_per_mol_16A_des_Cass_list.append(np.mean(Average_of_mu_list_iteration))
    Calc_P_div_Po = np.mean(np.exp(Avg_mu_kJ_per_mol_16A_des_Cass_list[i] * slope_Cass + intercept_Cass)) / Psat_at_298K
    P_div_Po_16A_des_Cass_list.append(Calc_P_div_Po)
    Std_Dev_E_per_area_16A_des_Cass_list.append(np.std(Average_of_E_per_area_list_iteration, ddof=1))



zipped_lists = zip(P_div_Po_16A_des_Cass_list, Avg_of_E_per_area_16A_des_Cass_list, Std_Dev_E_per_area_16A_des_Cass_list)
sorted_pairs = sorted(zipped_lists)
tuples = zip(*sorted_pairs)
P_div_Po_16A_des_Cass_list, Avg_of_E_per_area_16A_des_Cass_list, Std_Dev_E_per_area_16A_des_Cass_list  = [ list(tuple) for tuple in tuples]


# original Cassandra organization
"""

Avg_of_E_per_area_10A_ads_Cass_list = []
mu_kJ_per_mol_10A_ads_Cass_list = []
P_div_Po_10A_ads_Cass_list = []
Avg_mu_kJ_per_mol_10A_ads_Cass_list = []
Std_Dev_E_per_area_10A_ads_Cass_list = []
for i in range(0, No_runs_per_set_10A_ads_Cass):
    Average_of_mu_list = []
    Average_of_E_per_area_list_iteration = []
    for j in range(0, No_independant_run_sets_per_10A_ads_Cass):
        evaluate_iteration = i + j * int(No_runs_per_set_10A_ads_Cass)
        Average_of_mu_list.append(mu_kJ_per_mol_10A_ads_Cass[evaluate_iteration])
        Average_of_E_per_area_list_iteration.append(Avg_E_No_water_per_nm_sq_10A_ads_Cass[evaluate_iteration])

    Avg_of_E_per_area_10A_ads_Cass_list.append(np.mean(Average_of_E_per_area_list_iteration))
    Avg_mu_kJ_per_mol_10A_ads_Cass_list.append(np.mean(Average_of_mu_list))
    Calc_P_div_Po = np.mean(np.exp(mu_kJ_per_mol_10A_ads_Cass[i] * slope_Cass + intercept_Cass)) / Psat_at_298K
    P_div_Po_10A_ads_Cass_list.append(Calc_P_div_Po)
    Std_Dev_E_per_area_10A_ads_Cass_list.append(np.std(Average_of_E_per_area_list_iteration, ddof=1))


zipped_lists = zip(P_div_Po_10A_ads_Cass_list, Avg_of_E_per_area_10A_ads_Cass_list, Std_Dev_E_per_area_10A_ads_Cass_list)
sorted_pairs = sorted(zipped_lists)
tuples = zip(*sorted_pairs)
P_div_Po_10A_ads_Cass_list, Avg_of_E_per_area_10A_ads_Cass_list, Std_Dev_E_per_area_10A_ads_Cass_list  = [ list(tuple) for tuple in tuples]


Avg_of_E_per_area_16A_ads_Cass_list = []
mu_kJ_per_mol_16A_ads_Cass_list = []
P_div_Po_16A_ads_Cass_list = []
Avg_mu_kJ_per_mol_16A_ads_Cass_list = []
Std_Dev_E_per_area_16A_ads_Cass_list = []
for i in range(0, No_runs_per_set_16A_ads_Cass):
    Average_of_mu_list = []
    Average_of_E_per_area_list_iteration = []
    for j in range(0, No_independant_run_sets_per_16A_ads_Cass):
        evaluate_iteration = i + j * int(No_runs_per_set_16A_ads_Cass)
        Average_of_mu_list.append(mu_kJ_per_mol_16A_ads_Cass[evaluate_iteration])
        Average_of_E_per_area_list_iteration.append(Avg_E_No_water_per_nm_sq_16A_ads_Cass[evaluate_iteration])

    Avg_of_E_per_area_16A_ads_Cass_list.append(np.mean(Average_of_E_per_area_list_iteration))
    Avg_mu_kJ_per_mol_16A_ads_Cass_list.append(np.mean(Average_of_mu_list))
    Calc_P_div_Po = np.mean(np.exp(mu_kJ_per_mol_16A_ads_Cass[i] * slope_Cass + intercept_Cass)) / Psat_at_298K
    P_div_Po_16A_ads_Cass_list.append(Calc_P_div_Po)
    Std_Dev_E_per_area_16A_ads_Cass_list.append(np.std(Average_of_E_per_area_list_iteration, ddof=1))


zipped_lists = zip(P_div_Po_16A_ads_Cass_list, Avg_of_E_per_area_16A_ads_Cass_list, Std_Dev_E_per_area_16A_ads_Cass_list)
sorted_pairs = sorted(zipped_lists)
tuples = zip(*sorted_pairs)
P_div_Po_16A_ads_Cass_list, Avg_of_E_per_area_16A_ads_Cass_list, Std_Dev_E_per_area_16A_ads_Cass_list  = [ list(tuple) for tuple in tuples]


Avg_of_E_per_area_10A_des_Cass_list = []
mu_kJ_per_mol_10A_des_Cass_list = []
P_div_Po_10A_des_Cass_list = []
Avg_mu_kJ_per_mol_10A_des_Cass_list = []
Std_Dev_E_per_area_10A_des_Cass_list = []
for i in range(0, No_runs_per_set_10A_des_Cass):
    Average_of_mu_list = []
    Average_of_E_per_area_list_iteration = []
    for j in range(0, No_independant_run_sets_per_10A_des_Cass):
        evaluate_iteration = i + j * int(No_runs_per_set_10A_des_Cass)
        Average_of_mu_list.append(mu_kJ_per_mol_10A_des_Cass[evaluate_iteration])
        Average_of_E_per_area_list_iteration.append(Avg_E_No_water_per_nm_sq_10A_des_Cass[evaluate_iteration])

    Avg_of_E_per_area_10A_des_Cass_list.append(np.mean(Average_of_E_per_area_list_iteration))
    Avg_mu_kJ_per_mol_10A_des_Cass_list.append(np.mean(Average_of_mu_list))
    Calc_P_div_Po = np.mean(np.exp(mu_kJ_per_mol_10A_des_Cass[i] * slope_Cass + intercept_Cass)) / Psat_at_298K
    P_div_Po_10A_des_Cass_list.append(Calc_P_div_Po)
    Std_Dev_E_per_area_10A_des_Cass_list.append(np.std(Average_of_E_per_area_list_iteration, ddof=1))


zipped_lists = zip(P_div_Po_10A_des_Cass_list, Avg_of_E_per_area_10A_des_Cass_list, Std_Dev_E_per_area_10A_des_Cass_list)
sorted_pairs = sorted(zipped_lists)
tuples = zip(*sorted_pairs)
P_div_Po_10A_des_Cass_list, Avg_of_E_per_area_10A_des_Cass_list, Std_Dev_E_per_area_10A_des_Cass_list  = [ list(tuple) for tuple in tuples]


Avg_of_E_per_area_16A_des_Cass_list = []
mu_kJ_per_mol_16A_des_Cass_list = []
P_div_Po_16A_des_Cass_list = []
Avg_mu_kJ_per_mol_16A_des_Cass_list = []
Std_Dev_E_per_area_16A_des_Cass_list = []
for i in range(0, No_runs_per_set_16A_des_Cass):
    Average_of_mu_list = []
    Average_of_E_per_area_list_iteration = []
    for j in range(0, No_independant_run_sets_per_16A_des_Cass):
        evaluate_iteration = i + j * int(No_runs_per_set_16A_des_Cass)
        Average_of_mu_list.append(mu_kJ_per_mol_16A_des_Cass[evaluate_iteration])
        Average_of_E_per_area_list_iteration.append(Avg_E_No_water_per_nm_sq_16A_des_Cass[evaluate_iteration])

    Avg_of_E_per_area_16A_des_Cass_list.append(np.mean(Average_of_E_per_area_list_iteration))
    Avg_mu_kJ_per_mol_16A_des_Cass_list.append(np.mean(Average_of_mu_list))
    Calc_P_div_Po = np.mean(np.exp(mu_kJ_per_mol_16A_des_Cass[i] * slope_Cass + intercept_Cass)) / Psat_at_298K
    P_div_Po_16A_des_Cass_list.append(Calc_P_div_Po)
    Std_Dev_E_per_area_16A_des_Cass_list.append(np.std(Average_of_E_per_area_list_iteration, ddof=1))


zipped_lists = zip(P_div_Po_16A_des_Cass_list, Avg_of_E_per_area_16A_des_Cass_list, Std_Dev_E_per_area_16A_des_Cass_list)
sorted_pairs = sorted(zipped_lists)
tuples = zip(*sorted_pairs)
P_div_Po_16A_des_Cass_list, Avg_of_E_per_area_16A_des_Cass_list, Std_Dev_E_per_area_16A_des_Cass_list  = [ list(tuple) for tuple in tuples]
"""

#****************************************
#Plot Number 1  (start)
#****************************************

fig1, ax1 = plt.subplots(2, 1, sharex=True)

plt.xlabel('$P/P_{sat}$', fontname="Arial", fontsize=axis_Label_font_size)
plt.ylabel('        $\u03BE$ (No. waters / nm$^2$)', fontname="Arial", fontsize=axis_Label_font_size)

ax1[0].set_xticks(np.arange(0, 100, 10))
ax1[1].set_xticks(np.arange(0, 100, 10))
ax1[0].set_yticks(np.arange(-200, 200, E_per_nm_sq_10A_step))
ax1[1].set_yticks(np.arange(-200, 200, E_per_nm_sq_16A_step))
ax1[0].xaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=5))
ax1[1].xaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=5))

WSU_color = '#ff7f0e'
NDU_color = '#1f77b4'

ax1[0].errorbar(P_div_Po_10A_ads_Cass_list, Avg_of_E_per_area_10A_ads_Cass_list, Std_Dev_E_per_area_10A_ads_Cass_list ,
                color=NDU_color , marker='D', linestyle='-' , markersize=PointSizes+2, linewidth=ConnectionLineSizes,
                fillstyle='full', label= "Cassandra - adsorb", ecolor='k', capsize=4, capthick=2
                , alpha=0.9) #label=File_label_No1
ax1[0].errorbar(P_div_Po_10A_des_Cass_list, Avg_of_E_per_area_10A_des_Cass_list, Std_Dev_E_per_area_10A_des_Cass_list,
                color=NDU_color,  marker='D', linestyle='--' , markersize=PointSizes+2, linewidth=ConnectionLineSizes,
                fillstyle='none', label= "Cassandra - desorb", ecolor='dimgrey', capsize=4, capthick=2
                , alpha=0.7)

mu_kJ_per_mol_16A_des_Cass = calc_data_16A_des_Cass_df.loc[:, 'mu-cassandra_kJmol' ].tolist()

Avg_E_No_water_per_nm_sq_10A_ads_Cass = calc_data_10A_ads_Cass_df.loc[:, 'nmols_per_nm^2' ].tolist()

ax1[0].errorbar(Psat_ratio_10A_ads, Avg_E_No_water_per_nm_sq_10A_ads, StdDev_E_No_water_per_nm_sq_10A_ads,
                color=WSU_color , marker='o', linestyle='-' , markersize=PointSizes, linewidth=ConnectionLineSizes,
                fillstyle='full', label= "GOMC - adsorb", ecolor='k', capsize=0.5, capthick=1
                , alpha=0.9)
ax1[0].errorbar(Psat_ratio_10A_des, Avg_E_No_water_per_nm_sq_10A_des, StdDev_E_No_water_per_nm_sq_10A_des,
                color=WSU_color , marker='o', linestyle='--' , markersize=PointSizes, linewidth=ConnectionLineSizes,
                fillstyle='none', label= "GOMC - desorb",  ecolor='dimgrey', capsize=0.5, capthick=1
                , alpha=0.7)

ax1[1].errorbar(P_div_Po_16A_ads_Cass_list, Avg_of_E_per_area_16A_ads_Cass_list, Std_Dev_E_per_area_16A_ads_Cass_list,
                color=NDU_color , marker='D', linestyle='-' , markersize=PointSizes+2, linewidth=ConnectionLineSizes,
                fillstyle='full',  ecolor='k', capsize=4, capthick=2
                , alpha=0.9)
ax1[1].errorbar(P_div_Po_16A_des_Cass_list, Avg_of_E_per_area_16A_des_Cass_list, Std_Dev_E_per_area_16A_des_Cass_list,
                color=NDU_color,  marker='D', linestyle='--' , markersize=PointSizes+2, linewidth=ConnectionLineSizes,
                fillstyle='none',  ecolor='dimgrey', capsize=4, capthick=2
                , alpha=0.7)

ax1[1].errorbar(Psat_ratio_16A_ads, Avg_E_No_water_per_nm_sq_16A_ads, StdDev_E_No_water_per_nm_sq_16A_ads,
                color=WSU_color , marker='o', linestyle='-' , markersize=PointSizes, linewidth=ConnectionLineSizes,
                fillstyle='full', ecolor='k', capsize=0.5, capthick=1
                , alpha=0.9)
ax1[1].errorbar(Psat_ratio_16A_des, Avg_E_No_water_per_nm_sq_16A_des, StdDev_E_No_water_per_nm_sq_16A_des,
                color=WSU_color ,  marker='o', linestyle='--' , markersize=PointSizes, linewidth=ConnectionLineSizes,
                fillstyle='none',  ecolor='dimgrey', capsize=0.5, capthick=1
                , alpha=0.7)


ax1[0].plot(Psat_ratio_10A_ads_Gubbins, Avg_E_No_water_per_nm_sq_10A_ads_Gubbins,
                color='darkred',  marker='s', linestyle='-' , markersize=PointSizes+2, linewidth=ConnectionLineSizes,
                fillstyle='full', label= "Striolo - adsorb", alpha=0.5)
ax1[0].plot(Psat_ratio_10A_des_Gubbins, Avg_E_No_water_per_nm_sq_10A_des_Gubbins,
                color='darkred',  marker='s', linestyle='--' , markersize=PointSizes+2, linewidth=ConnectionLineSizes,
                fillstyle='none', label= "Striolo - desorb", alpha=0.5)

ax1[1].plot(Psat_ratio_16A_ads_Gubbins, Avg_E_No_water_per_nm_sq_16A_ads_Gubbins,
                color='darkred',  marker='s', linestyle='-' , markersize=PointSizes+2, linewidth=ConnectionLineSizes,
                fillstyle='full', label= "Striolo - adsorb", alpha=0.5)
ax1[1].plot(Psat_ratio_16A_des_Gubbins, Avg_E_No_water_per_nm_sq_16A_des_Gubbins,
                color='darkred',  marker='s', linestyle='--' , markersize=PointSizes+2, linewidth=ConnectionLineSizes,
                fillstyle='none', label= "Striolo - desorb", alpha=0.5)

ax1[0].tick_params(axis='both', which='minor', length=2, width=1, labelsize=axis_number_font_size, top=True, right=True, direction='in')
ax1[1].tick_params(axis='both', which='minor', length=2, width=1, labelsize=axis_number_font_size, top=True, right=True, direction='in')

ax1[0].tick_params(axis='both', which='major', length=4, width=2, labelsize=axis_number_font_size, top=True, right=True, direction='in')
ax1[1].tick_params(axis='both', which='major', length=4, width=2, labelsize=axis_number_font_size, top=True, right=True, direction='in')

ax1[0].legend(ncol=2,loc='upper left', fontsize=legend_font_size, prop={'family':'Arial','size': legend_font_size}, framealpha=1,bbox_to_anchor=(-0.22, 2.05))

ax1[0].text(0.0020, 6.1, "1.0 nm slit", fontsize=legend_font_size)
ax1[1].text(0.0020, 12.2, "1.6 nm slit", fontsize=legend_font_size)

plt.tight_layout()  # centers layout nice for final paper

plt.gcf().subplots_adjust(left=None, bottom=None, right=None, top=0.70, wspace=None, hspace=None) # moves plot  so x label not cutoff

plt.xscale("log")
fig1.subplots_adjust(hspace=0)

plt.xlim(Psat_div_Po_min, Psat_div_Po_max)  # set plot range on x axis
ax1[0].set_ylim(E_per_nm_sq_10A_min, E_per_nm_sq_10A_max)  # set plot range on y axis
ax1[1].set_ylim(E_per_nm_sq_16A_min, E_per_nm_sq_16A_max)  # set plot range on y axis

ax1[0].grid()
ax1[1].grid()


plt.show()
fig1.savefig(E_vs_P_Psat_saving_name)
#****************************************
#Plot Number 1 (end)
#****************************************


