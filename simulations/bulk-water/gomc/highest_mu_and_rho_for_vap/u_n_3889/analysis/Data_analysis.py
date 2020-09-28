import numpy as np
import matplotlib.pyplot as plt
import csv as csv
import pandas as pd
from scipy.stats import linregress

GOMC_Chempot_K = -3889
Set_List  = ['set1']
file_folder_list =     [ '1r1', '1r2', '1r3', '1r4', '1r5'   ]
phase_list     =        [ 'v',   'v',   'v',   'v',   'v'   ]
Start_Msteps_avg_list = [  50,   50,    50,    50,    50   ]
End_Msteps_avg_list   = [ 100,  100,   100,   100,   100   ]

Box_data_save_file_name = 'SPCE_Rho_o_and_P_o_at_298K'
mu_folder = 'u_n_3950'

Column_no_Step = 0  # must be iteration value
Column_no_Pressure = 10
Column_no_Density = 12

Pressure_Box_1_List = []
Density_Box_1_List = []


Chempot_correction_to_abs_Chempot = -1282.30449445439
Abs_Chempot_K = GOMC_Chempot_K + Chempot_correction_to_abs_Chempot


for n in range(0, len(Set_List)):
	set_iteration = Set_List[n]


	for j in range(len(file_folder_list)):
		file_folder_list_run_file_file1= j

		reading_file_Box_1 ='../'+str(set_iteration)+'/'+str(file_folder_list[j])+'/Blk_Output_data_BOX_0.dat'

		Column_Step_Title = 'STEPS'
		Column_Po_Title = 'Po_bar'
		Column_Density_Title = 'Rho_o'

		Column_Avg_Po_Title = 'Avg_Po_bar'
		Column_Avg_Density_Title = 'Avg_Rho_o_kg_m_cub'
		Column_StdDev_Po_Title = 'StdDev_Po_bar'
		Column_StdDev_Density_Title = 'StdDev_Rho_kg_m_cub'
		Column_GOMC_Chempot_K_Title = 'GOMC_ChemPot_K'
		Column_ABS_Chempot_K_Title = 'ABS_ChemPot_K'
		Extracted_Data_file_Titles = [Column_Step_Title, Column_Po_Title, Column_Density_Title]

		Step_start_string = str(int(Start_Msteps_avg_list[j]*10**6))
		Step_finish_string = str(int(End_Msteps_avg_list[j]*10**6))

		data_Box_1 = pd.read_csv(reading_file_Box_1, sep='\s+', header=1,
								 na_values='NaN', names = Extracted_Data_file_Titles,
								 usecols=[Column_no_Step, Column_no_Pressure, Column_no_Density], index_col=False)


		data_Box_1 = pd.DataFrame(data_Box_1)

		data_Box_1 = data_Box_1.query(Step_start_string +' <= ' + 'STEPS'   + ' <= ' + Step_finish_string)

		Iteration_no_Box_1 = data_Box_1.loc[:,Column_Step_Title]
		Iteration_no_Box_1 = list(Iteration_no_Box_1)
		Iteration_no_Box_1 = np.transpose(Iteration_no_Box_1)

		Total_waters_list = []

		Total_Po_1 = data_Box_1.loc[:,Column_Po_Title]
		Total_Po_1 = list(Total_Po_1)
		Total_Po_1 = np.transpose(Total_Po_1)
		Total_Po_1_Mean = np.nanmean(Total_Po_1)

		Pressure_Box_1_List.append(Total_Po_1_Mean)

		Total_Density_1 = data_Box_1.loc[:,Column_Density_Title]
		Total_Density_1 = list(Total_Density_1)
		Total_Density_1 = np.transpose(Total_Density_1)
		Total_Density_1_Mean = np.nanmean(Total_Density_1)

		Density_Box_1_List.append(Total_Density_1_Mean)


Po_total_mean = np.nanmean(Pressure_Box_1_List)
Po_total_StdDev = np.std(Pressure_Box_1_List, ddof=1)
Density_total_mean = np.nanmean(Density_Box_1_List)
Density_total_StdDev = np.std(Density_Box_1_List, ddof=1)

print(Pressure_Box_1_List)

Box_0_data_dataframe =pd.DataFrame(np.column_stack([Po_total_mean, Po_total_StdDev,
													Density_total_mean, Density_total_StdDev,
													GOMC_Chempot_K,
													Abs_Chempot_K]))

Box_0_data_dataframe.to_csv(Box_data_save_file_name + '_df.txt', sep="	",
							header=[Column_Avg_Po_Title, Column_StdDev_Po_Title,
									Column_Avg_Density_Title, Column_StdDev_Density_Title,
									Column_GOMC_Chempot_K_Title, Column_ABS_Chempot_K_Title])

Box_0_data_dataframe.to_csv(Box_data_save_file_name + '_df.csv', sep=",",
							header=[Column_Avg_Po_Title, Column_StdDev_Po_Title,
									Column_Avg_Density_Title, Column_StdDev_Density_Title,
									Column_GOMC_Chempot_K_Title, Column_ABS_Chempot_K_Title])

