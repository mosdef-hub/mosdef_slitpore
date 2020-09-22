import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import csv as csv
import pandas as pd
import itertools as it
import statistics
from collections import defaultdict
import os
import shutil
import matplotlib.axis as axis
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from sklearn.linear_model import LinearRegression
from scipy import stats

#check all thermal expansion errors and cp errors before providing data

Step_start = 50 *10**6
Step_finish = 100 *10**6
Temp_K =298


Set_List  = ['set1', 'set2', 'set3', 'set4', 'set5']
ChemPot =  [-6295, -5573,  -4852, -4491, -4401, -4130, -4040, -3950]
run_No = [  '1r1', '1r2', '1r3', '1r4', '1r5', '1r6', '1r7', '1r8']
Volume_box_Ang_cubed = [5000**3, 2000**3, 1000**3, 600**3,  600**3, 400**3, 400**3, 300**3]
Column_no_Step = 0  # must be iteration value
Column_no_Pressure = 10  # column for PRESSURE
Column_Total_Molecules = 11  # column for TOT_MOL
Column_Density = 12  # column for TOT_DENS

Chemical_being_analyzed = 'water'


#*******************************************************************************************************************
#  need to insert blocking_std_dev method to calculate accuated Std. Deviations to get accurate results
#*******************************************************************************************************************

Psat_data_file = '../../../Psat_SPCE_298K/analysis/SPCE_Pvap_at_298K_df.csv'
Psat_data = pd.read_csv(Psat_data_file, sep=',', header=0, na_values='NaN',
						usecols=[0,1], index_col=False)

Psat_data = pd.DataFrame(Psat_data)
print(Psat_data)

Psat_SPEC_data_bar = Psat_data.loc[:,'Avg_Pvap_bar']
Psat_SPEC_data_bar = list(Psat_SPEC_data_bar)[0]
print('Psat_SPEC_data_bar = '+str(Psat_SPEC_data_bar))
Psat_at_298K = Psat_SPEC_data_bar

Temp_List = []
Pressure_Box_0_List = []
Total_Molecules_Box_0_List = []
Density_Box_0_List = []
P_from_IG_Density_Box_0_List =[]
Pressure_Box_1_List = []
Total_Molecules_Box_1_List = []
Density_Box_1_List = []


Pressure_Box_0_Final_Mean_List = []
Pressure_Box_0_Final_StdDev_List = []
Total_Molecules_Box_0_Final_Mean_List = []
Total_Molecules_Box_0_Final_StdDev_List = []
Density_Box_0_Final_Mean_List = []
Density_Box_0_Final_StdDev_List = []
P_from_IG_Density_Box_0_Final_Mean_List =[]
P_from_IG_Density_Box_0_Final_StdDev_List =[]
Pressure_Box_1_Final_Mean_List = []
Pressure_Box_1_Final_StdDev_List = []
Total_Molecules_Box_1_Final_Mean_List = []
Total_Molecules_Box_1_Final_StdDev_List = []
Density_Box_1_Final_StdDev_Final_Mean_List = []
Density_Box_1_Final_StdDev_List = []


Density_Avg_Box_0_and_1_List = []

Box_data_save_file_name = 'Avg_data_from Box_'
# ***********************
# calc the avg data from the liq and vap boxes (start)
# ***********************




for j in range(len(run_No)):
	run_No_run_file_file1 = j
	run_No_iteration = run_No[j]

	Pressure_Box_0_iteration_List = []
	Total_Molecules_Box_0_iteration_List = []
	Density_Box_0_iteration_List = []
	P_from_IG_Density_Box_0_iteration_List = []
	Pressure_Box_0_iteration_0_List = []

	for n in range(0, len(Set_List)):
		set_iteration = Set_List[n]




		first_part_run_path = '../'+str(set_iteration)

		reading_file_Box_0 = first_part_run_path+'/'+str(run_No[j])+'/'+'Blk_SPCE_Pvap_BOX_0.dat'




		#*******************************************************************************************************
		#end major variables
		# *******************************************************************************************************
		Column_Psat_ratio_Title = 'Psat_ratio'  #
		Column_ChemPot_Title = 'ChemPot_K'  # column title Title for PRESSURE
		Column_no_Step_Title = 'Step'  # column title Title for iteration value
		Column_no_Pressure_Title = 'P_bar'  # column title Title for PRESSURE
		Column_no_Pressure_from_IG_density = 'P_from_IG_Density_bar'
		Column_Total_Molecules_Title = "No_mol"  # column title Title for TOT_MOL
		Column_Density_Title = 'Density_kg_per_mcubed'  # column title Title for TOT_DENS


		Extracted_Data_file_Titles = [Column_no_Step_Title, Column_no_Pressure_Title,
									   Column_Total_Molecules_Title, Column_Density_Title]




		#Programmed data
		Step_start_string = str(int(Step_start))
		Step_finish_string = str(int(Step_finish))

		#*************************
		#drawing in data from single file and extracting specific rows for the liquid box (start)
		# *************************
		data_Box_0_iteration = pd.read_csv(reading_file_Box_0, names=Extracted_Data_file_Titles, sep='\s+', header=1, na_values='NaN',
							usecols=[Column_no_Step,Column_no_Pressure, Column_Total_Molecules,
									 Column_Density], index_col=False)

		data_Box_0_iteration = pd.DataFrame(data_Box_0_iteration)
		data_Box_0_iteration = data_Box_0_iteration.query(Step_start_string +' <= ' + Column_no_Step_Title  + ' <= ' + Step_finish_string)
		##print('Liquid data')
		#print(data_Box_0)

		No_Box_0_iteration = data_Box_0_iteration.loc[:,Column_no_Step_Title]
		No_Box_0_iteration = list(No_Box_0_iteration)
		No_Box_0_iteration = np.transpose(No_Box_0_iteration)

		Pressure_Box_0_iteration = data_Box_0_iteration.loc[:,Column_no_Pressure_Title]
		Pressure_Box_0_iteration = list(Pressure_Box_0_iteration)
		Pressure_Box_0_iteration = np.transpose(Pressure_Box_0_iteration)
		Pressure_Box_0_iteration_Mean = np.nanmean(Pressure_Box_0_iteration)

		Total_Molecules_Box_0_iteration = data_Box_0_iteration.loc[:,Column_Total_Molecules_Title]
		Total_Molecules_Box_0_iteration = list(Total_Molecules_Box_0_iteration)
		Total_Molecules_Box_0_iteration = np.transpose(Total_Molecules_Box_0_iteration)
		Total_Molecules_Box_0_iteration_Mean = np.nanmean(Total_Molecules_Box_0_iteration)

		Density_Box_0_iteration = data_Box_0_iteration.loc[:,Column_Density_Title]
		Density_Box_0_iteration = list(Density_Box_0_iteration)
		Density_Box_0_iteration = np.transpose(Density_Box_0_iteration)
		Density_Box_0_iteration_Mean = np.nanmean(Density_Box_0_iteration)


		#*************************
		#drawing in data from single file and extracting specific rows for the liquid box (end)
		# *************************


		#*************************
		#drawing in data from single file and extracting specific rows for the vapor box (start)
		# *************************


		ChemPot_List=ChemPot

		Pressure_Box_0_iteration_List.append(Pressure_Box_0_iteration_Mean)
		Total_Molecules_Box_0_iteration_List.append(Total_Molecules_Box_0_iteration_Mean)
		Density_Box_0_iteration_List.append(Density_Box_0_iteration_Mean)

		R_ang_cubed_bar_per_K_mol = 8.31446261815324E+025
		Avagadro_No = 6.022*10**23



	Pressure_Box_0_List.append(np.mean(Pressure_Box_0_iteration_List))
	Total_Molecules_Box_0_List.append(np.mean(Total_Molecules_Box_0_iteration_List))
	Density_Box_0_List.append(np.mean(Density_Box_0_iteration_List))


for i in range(0, len(Pressure_Box_0_List)):
	P_from_IG_Density_Box_0_List.append(
		R_ang_cubed_bar_per_K_mol * Total_Molecules_Box_0_List[i] * Temp_K / (Avagadro_No * Volume_box_Ang_cubed[i]))


ratio_of_Psat_ratio = [i/Psat_at_298K for i in Pressure_Box_0_List]



	#*************************
	#drawing in data from single file and extracting specific rows for the vapor box (end)
	# *************************
print('ratio_of_Psat_ratio = ' + str(ratio_of_Psat_ratio))
print('ChemPot_List = '+str(ChemPot_List))
print('Pressure_Box_0_List = '+str(Pressure_Box_0_List))
print('Total_Molecules_Box_0_List = '+str(Total_Molecules_Box_0_List))
print('Density_Box_0_List = '+str(Density_Box_0_List))


Box_0_data_dataframe =pd.DataFrame(np.column_stack([ratio_of_Psat_ratio,
													ChemPot_List,
													Pressure_Box_0_List,
													P_from_IG_Density_Box_0_List ,
													Total_Molecules_Box_0_List,
													Density_Box_0_List]))


Box_0_data_dataframe.to_csv(Box_data_save_file_name + '0_'+str(Chemical_being_analyzed)+'_df.txt', sep="	",
							header=[Column_Psat_ratio_Title, Column_ChemPot_Title, Column_no_Pressure_Title,
									Column_no_Pressure_from_IG_density,
									Column_Total_Molecules_Title, Column_Density_Title])
Box_0_data_dataframe.to_csv(Box_data_save_file_name + '0_'+str(Chemical_being_analyzed)+'_df.csv', sep=",",
							header=[Column_Psat_ratio_Title, Column_ChemPot_Title, Column_no_Pressure_Title,
								  Column_no_Pressure_from_IG_density,
								   Column_Total_Molecules_Title, Column_Density_Title])

