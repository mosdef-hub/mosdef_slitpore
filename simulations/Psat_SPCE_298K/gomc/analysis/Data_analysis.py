import numpy as np
import matplotlib.pyplot as plt
import csv as csv
import pandas as pd
from scipy.stats import linregress


Set_List  = ['set1']
file_folder_list =     [ '1r1', '1r2', '1r3', '1r4', '1r5'   ]
phase_list     =        [ 'v',   'v',   'v',   'v',   'v'   ]
Start_Msteps_avg_list = [  20,   20,    20,    20,    20   ]
End_Msteps_avg_list   = [  60,   60,    60,    60,    60   ]



Box_data_save_file_name = 'SPCE_Pvap_at_298K'

Column_no_Step = 0
Column_no_Pressure = 10
Column_no_density = 12

Pressure_Box_1_List = []
Density_Box_1_List = []
for n in range(0, len(Set_List)):
	set_iteration = Set_List[n]

	for j in range(len(file_folder_list)):
		file_folder_list_run_file_file1= j

		reading_file_Box_1 ='../'+str(set_iteration)+'/'+str(file_folder_list[j])+'/Blk_Output_data_BOX_1.dat'

		Column_Step_Title = 'STEPS'
		Column_Pvap_Title = 'Pvap_bar'

		Column_Avg_Pvap_Title = 'Avg_Pvap_bar'
		Column_StdDev_Pvap_Title = 'StdDev_Pvap_bar'

		Column_Avg_density_Title = 'Avg_density_bar'
		Column_StdDev_density_Title = 'StdDev_density_bar'

		Extracted_Data_file_Titles = [Column_Step_Title, Column_Pvap_Title, Column_Avg_density_Title]

		Step_start_string = str(int(Start_Msteps_avg_list[j]*10**6))
		Step_finish_string = str(int(End_Msteps_avg_list[j]*10**6))

		data_Box_1 = pd.read_csv(reading_file_Box_1, sep='\s+', header=1,
								 na_values='NaN', names = Extracted_Data_file_Titles,
								 usecols=[Column_no_Step, Column_no_Pressure, Column_no_density ], index_col=False)


		data_Box_1 = pd.DataFrame(data_Box_1)
		data_Box_1 = data_Box_1.query(Step_start_string +' <= ' + 'STEPS'   + ' <= ' + Step_finish_string)


		Iteration_no_Box_1 = data_Box_1.loc[:,Column_Step_Title]
		Iteration_no_Box_1 = list(Iteration_no_Box_1)
		Iteration_no_Box_1 = np.transpose(Iteration_no_Box_1)


		Total_waters_list = []

		Total_Pvap_1 = data_Box_1.loc[:,Column_Pvap_Title]
		Total_Pvap_1 = list(Total_Pvap_1)
		Total_Pvap_1 = np.transpose(Total_Pvap_1)
		Total_Pvap_1_Mean = np.nanmean(Total_Pvap_1)

		Pressure_Box_1_List.append(Total_Pvap_1_Mean)

		Total_Density_1 = data_Box_1.loc[:, Column_Avg_density_Title ]
		Total_Density_1 = list(Total_Density_1)
		Total_Density_1 = np.transpose(Total_Density_1)
		Total_Density_1_Mean = np.nanmean(Total_Density_1)

		Density_Box_1_List.append(Total_Density_1_Mean)


Psat_total_mean = np.nanmean(Pressure_Box_1_List)
Psat_total_StdDev = np.std(Pressure_Box_1_List, ddof=1)

Density_total_mean = np.nanmean(Density_Box_1_List)
Density_total_StdDev = np.std(Density_Box_1_List, ddof=1)

print(Pressure_Box_1_List)

Box_0_data_dataframe =pd.DataFrame(np.column_stack([Psat_total_mean, Psat_total_StdDev,
													Density_total_mean,Density_total_StdDev
													]))

Box_0_data_dataframe.to_csv(Box_data_save_file_name + '_df.txt', sep="	",
							header=[Column_Avg_Pvap_Title, Column_StdDev_Pvap_Title,
									Column_Avg_density_Title, Column_StdDev_density_Title])

Box_0_data_dataframe.to_csv(Box_data_save_file_name + '_df.csv', sep=",",
							header=[Column_Avg_Pvap_Title, Column_StdDev_Pvap_Title,
									Column_Avg_density_Title, Column_StdDev_density_Title])
