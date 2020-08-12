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
Psat_at_298K = 0.01017


Step_start = 50 *10**6
Step_finish = 100 *10**6
Temp_K =298

Use_Last_No_Temps_for_Critical_calcs = 4
ChemPot =  [-6295, -5934, -5573, -5212, -4852, -4671, -4491 , -4401 , -4310, -4130, -4085, -4040 , -3950] # [-6295, -5934, -5573, -5212, -4852, -4671, -4491 , -4401 , -4310, -4130, 4085, -4040 , -3950, -3769]
ratio_of_Psat = [  'u_n_6295', 'u_n_5934', 'u_n_5573', 'u_n_5212', 'u_n_4852', 'u_n_4671', 'u_n_4491', 'u_n_4401', 'u_n_4310', 'u_n_4130' ,'u_n_4085' , 'u_n_4040', 'u_n_3950']  # [  'u_n_6295', 'u_n_5934', 'u_n_5573', 'u_n_5212', 'u_n_4852', 'u_n_4671', 'u_n_4491', 'u_n_4401', 'u_n_4310', 'u_n_4130' ,'u_n_4085' , 'u_n_4040', 'u_n_3950', 'u_n_3769']
Volume_box_Ang_cubed = [ 5000**3, 3000**3, 2000**3, 1500**3, 1000**3, 800**3, 600**3, 600**3, 500**3, 400**3 , 400**3, 400**3, 300**3]  #  [ 5000**3, 3000**3, 2000**3, 1500**3, 1000**3, 800**3, 600**3, 600**3, 500**3, 400**3 , 400**3, 400**3, 300**3, 300**3]

Column_no_Step = 0  # must be iteration value
Column_no_Pressure = 10  # column for PRESSURE
Column_Total_Molecules = 11  # column for TOT_MOL
Column_Density = 12  # column for TOT_DENS
#Column_Box_Volume = 13  # column for VOLUME
#Column_Box_Hv = 14  # column for HEAT_VAP

Antoine_coeff_reading_file_name = '../../Exp_Antoine_Coeffs.txt'
Chemical_being_analyzed = 'water'

Use_Antoine_Eqn = 0   # 1 =yes , 0 = no

Beta_for_Critical_points = 0.326
#*******************************************************************************************************************
#  need to insert blocking_std_dev method to calculate accuated Std. Deviations to get accurate results
#*******************************************************************************************************************
Temp_List = []
Pressure_Box_0_List = []
Total_Molecules_Box_0_List = []
Density_Box_0_List = []
P_from_IG_Density_Box_0_List =[]
Pressure_Box_1_List = []
Total_Molecules_Box_1_List = []
Density_Box_1_List = []


Density_Avg_Box_0_and_1_List = []

Tc_calcd = "Tc_K"
DENSITYc_calcd = "DENSITYc_kg/m_cubed"
Pc_calcd = "Pc_bar"

Critical_Point_List_Titles = [Tc_calcd, DENSITYc_calcd, Pc_calcd]


if Use_Antoine_Eqn==1:

	Antoine_coeff_save_file_name = 'Antoine_coeff_data_'+str(Chemical_being_analyzed)

	Antoine_coeff_data_Chemical_name_Title = 'name'
	Antoine_coeff_data_Temp_min_K_Title = 'Temp_min_K'
	Antoine_coeff_data_Temp_max_K_Title = 'Temp_max_K'
	Antoine_coeff_data_P_scalar_Title = 'P_scalar'
	Antoine_coeff_data_A_Title = 'A'
	Antoine_coeff_data_B_Title = 'B'
	Antoine_coeff_data_C_Title = 'C'

	Antoine_Data_file_Titles_List = [Antoine_coeff_data_Chemical_name_Title,
									 Antoine_coeff_data_Temp_min_K_Title, Antoine_coeff_data_Temp_max_K_Title,
									 Antoine_coeff_data_P_scalar_Title, Antoine_coeff_data_A_Title,
									 Antoine_coeff_data_B_Title, Antoine_coeff_data_C_Title]

	# names = Antoine_Data_file_Titles_List
	# *******************************************************************************************************
	# end major variables
	# dont need to change anything below
	# *******************************************************************************************************
	Antoine_Coeff_Temp_range_List = []
	Antoine_Coeff_Psat_bar_List = []
	Antoine_Coeff_Temp_No_Points = 50

	Antoine_coeff_data = pd.read_csv(Antoine_coeff_reading_file_name, sep='\s+', header=1, na_values='NaN',
									 usecols=[Antoine_coeff_data_Chemical_name_Title,
											  Antoine_coeff_data_Temp_min_K_Title, Antoine_coeff_data_Temp_max_K_Title,
											  Antoine_coeff_data_P_scalar_Title, Antoine_coeff_data_A_Title,
											  Antoine_coeff_data_B_Title, Antoine_coeff_data_C_Title], index_col=0)

	Antoine_coeff_data = pd.DataFrame(Antoine_coeff_data)
	Antoine_coeff_Chemical_Tmin_K = Antoine_coeff_data.loc[Chemical_being_analyzed, 'Temp_min_K']
	Antoine_coeff_Chemical_Tmax_K = Antoine_coeff_data.loc[Chemical_being_analyzed, 'Temp_max_K']
	Antoine_coeff_Chemical_P_scalar = Antoine_coeff_data.loc[Chemical_being_analyzed, 'P_scalar']
	Antoine_coeff_Chemical_A = Antoine_coeff_data.loc[Chemical_being_analyzed, 'A']
	Antoine_coeff_Chemical_B = Antoine_coeff_data.loc[Chemical_being_analyzed, 'B']
	Antoine_coeff_Chemical_C = Antoine_coeff_data.loc[Chemical_being_analyzed, 'C']

	# ***********************
	# caluate the Anoine Psat within the temp range (start)
	# ***********************
	Antoine_Temp_Step = (Antoine_coeff_Chemical_Tmax_K-Antoine_coeff_Chemical_Tmin_K)/Antoine_Coeff_Temp_No_Points
	for i in range(0,Antoine_Coeff_Temp_No_Points+1):
		Antoine_Temp_iteration = Antoine_coeff_Chemical_Tmin_K + i * Antoine_Temp_Step
		Antoine_Psat_iteration = Antoine_coeff_Chemical_P_scalar * 10**(Antoine_coeff_Chemical_A
																		- Antoine_coeff_Chemical_B/(Antoine_Temp_iteration+ Antoine_coeff_Chemical_C))

		Antoine_Coeff_Temp_range_List.append(Antoine_Temp_iteration)
		Antoine_Coeff_Psat_bar_List.append(Antoine_Psat_iteration)


	Antoine_Coeff_dataframe =pd.DataFrame(np.column_stack([Antoine_Coeff_Temp_range_List, Antoine_Coeff_Psat_bar_List]))
	Antoine_Coeff_dataframe.to_csv(Antoine_coeff_save_file_name + "_df.txt", sep="	", header=['ChemPot_bar', 'P_bar'])
# ***********************
# caluate the Anoine Psat within the temp range (end)
# ***********************

# ***********************
# calc the avg data from the liq and vap boxes (start)
# ***********************
Box_data_save_file_name = 'Avg_data_from Box_'
for j in range(len(ratio_of_Psat)):
	#concentration 1 files and inputs
	ratio_of_Psat_run_file_file1= j
	ratio_of_Psat_iteration = ratio_of_Psat[j]
	first_part_run_path = '../'

	reading_file_Box_0 = first_part_run_path+str(ratio_of_Psat[j])+'/'+'Blk_Output_data_BOX_0.dat'

	#reading_file_Box_1 = first_part_run_path+ str(ratio_of_Psat[j]) + '/' + 'Blk_Output_data_BOX_1.dat'



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
	data_Box_0 = pd.read_csv(reading_file_Box_0, names=Extracted_Data_file_Titles, sep='\s+', header=1, na_values='NaN',
						usecols=[Column_no_Step,Column_no_Pressure, Column_Total_Molecules,
								 Column_Density], index_col=False)

	data_Box_0 = pd.DataFrame(data_Box_0)
	data_Box_0 = data_Box_0.query(Step_start_string +' <= ' + Column_no_Step_Title  + ' <= ' + Step_finish_string)
	##print('Liquid data')
	#print(data_Box_0)

	Iteration_no_Box_0 = data_Box_0.loc[:,Column_no_Step_Title]
	Iteration_no_Box_0 = list(Iteration_no_Box_0)
	Iteration_no_Box_0 = np.transpose(Iteration_no_Box_0)

	Pressure_Box_0 = data_Box_0.loc[:,Column_no_Pressure_Title]
	Pressure_Box_0 = list(Pressure_Box_0)
	Pressure_Box_0 = np.transpose(Pressure_Box_0)
	Pressure_Box_0_Mean = np.nanmean(Pressure_Box_0)

	Total_Molecules_Box_0 = data_Box_0.loc[:,Column_Total_Molecules_Title]
	Total_Molecules_Box_0 = list(Total_Molecules_Box_0)
	Total_Molecules_Box_0 = np.transpose(Total_Molecules_Box_0)
	Total_Molecules_Box_0_Mean = np.nanmean(Total_Molecules_Box_0)

	Density_Box_0 = data_Box_0.loc[:,Column_Density_Title]
	Density_Box_0 = list(Density_Box_0)
	Density_Box_0 = np.transpose(Density_Box_0)
	Density_Box_0_Mean = np.nanmean(Density_Box_0)



	#*************************
	#drawing in data from single file and extracting specific rows for the liquid box (end)
	# *************************


	#*************************
	#drawing in data from single file and extracting specific rows for the vapor box (start)
	# *************************


	ChemPot_List=ChemPot

	Pressure_Box_0_List.append(Pressure_Box_0_Mean)
	Total_Molecules_Box_0_List.append(Total_Molecules_Box_0_Mean)
	Density_Box_0_List.append(Density_Box_0_Mean)

	R_ang_cubed_bar_per_K_mol = 8.31446261815324E+025
	Avagadro_No = 6.022*10**23

	P_from_IG_Density_Box_0_bar =[]
	for i in range(0,len(Iteration_no_Box_0)):
		P_from_IG_Density_Box_0_bar.append( R_ang_cubed_bar_per_K_mol*Total_Molecules_Box_0[i]*Temp_K/ (Avagadro_No * Volume_box_Ang_cubed[j]) )

	P_from_IG_Density_Box_0_Mean = np.nanmean(P_from_IG_Density_Box_0_bar)
	P_from_IG_Density_Box_0_List.append(P_from_IG_Density_Box_0_Mean)

for i in range(0,len(Pressure_Box_0_List)):
	ratio_of_Psat_ratio = [i/Psat_at_298K for i in Pressure_Box_0_List]

	#*************************
	#drawing in data from single file and extracting specific rows for the vapor box (end)
	# *************************

Box_0_data_dataframe =pd.DataFrame(np.column_stack([ratio_of_Psat_ratio , ChemPot_List, Pressure_Box_0_List,
													P_from_IG_Density_Box_0_List ,
													Total_Molecules_Box_0_List, Density_Box_0_List]))
Box_0_data_dataframe.to_csv(Box_data_save_file_name + '0_'+str(Chemical_being_analyzed)+'_df.txt', sep="	",
							header=[Column_Psat_ratio_Title, Column_ChemPot_Title, Column_no_Pressure_Title,
								  Column_no_Pressure_from_IG_density,
								   Column_Total_Molecules_Title, Column_Density_Title])

