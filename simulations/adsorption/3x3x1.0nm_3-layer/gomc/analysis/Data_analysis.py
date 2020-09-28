import numpy as np
import matplotlib.pyplot as plt
import csv as csv
import pandas as pd
from scipy.stats import linregress


adsoption_or_desorbtion = 'adsorption' # 'adsoption' or 'desorbtion'
pore_size_A = 10

Set_List =     [ 'set1', 'set2', 'set3', 'set4', 'set5'] #  [ 'set1', 'set2','set3','set4','set5']

ChemPot_List =     [   -5573, -5212, -4852, -4491, -4370,          -4250, -4130, -3769] # for 10A adsorption [-5573, -5212, -4852, -4491, -4370, -4250, -4130, -3769]
file_folder_list = [    '1r1', '1r2', '1r3', '1r4', '1r5_restart', '1r6', '1r7', '1r8']
phase_list     = [       'v',   'v',   'v',   'v',   'l',            'l',   'l',   'l']
Start_Msteps_avg_list = [ 100,  100,   100,   100,    90,             20,    20,    20]
End_Msteps_avg_list   = [ 150,  150,   150,   150,    150,             50,    50,    50]



calc_data_reading_name = '../../../../bulk-water/gomc/analysis/Avg_data_from Box_0_water_df.txt'
calc_data = pd.read_csv(calc_data_reading_name,  sep='\s+', index_col=0)
calc_data_df = pd.DataFrame(calc_data)
print(calc_data_df)
mu_K_list = calc_data_df.loc[:, 'ChemPot_K' ].tolist()
P_div_Psat = calc_data_df.loc[:, 'Psat_ratio' ].tolist()
ln_P_div_Psat = [np.log(x) for x in P_div_Psat]

Chempot_correction_to_abs_Chempot = -1282.30449445439

mu_K_list_corrected = [x + Chempot_correction_to_abs_Chempot for x in mu_K_list]

ChemPot_List_corrected = [x + Chempot_correction_to_abs_Chempot for x in ChemPot_List]

slope, intercept, r_value, p_value, stderr = linregress(mu_K_list_corrected, y = ln_P_div_Psat )



Temp_K =298

R_kJ_per_mol_K = 8.314/1000
kB_kJ_per_K =  1.380649*10**(-23)/1000
surface_area_nm_sq = (29.472)/10 * (29.777)/10 *2

Chemical_being_analyzed = 'slit'
Box_data_save_file_name = str(adsoption_or_desorbtion)+'_'+str(pore_size_A)+'A'

Column_no_Step = 0
Column_no_Total_Molecules = 9
Column_no_Density = 10
Column_no_Water_or_fake_water_molp_1 = 13
Column_no_Water_or_fake_water_molp_2  = 14

Psat_ratio_for_sets_list = []
E_No_water_for_sets_list = []
No_waters_for_sets_list = []

for n in range(0, len(Set_List)):
	Psat_ratio_list = []
	set_iteration = Set_List[n]

	Temp_List = []
	Pressure_Box_0_List = []
	Total_waters_Box_0_List = []
	Total_Molecules_Box_1_List = []
	E_No_water_per_nm_sq_list = []


	for j in range(len(file_folder_list)):
		file_folder_list_run_file_file1= j

		reading_file_Box_0 ='../'+str(set_iteration)+'/'+str(file_folder_list[j])+'/Blk_SPCE_PORE_'+str(pore_size_A)+'_BOX_0.dat'

		Column_Psat_ratio_Title = 'Psat_ratio'
		Column_ChemPot_Title = 'ChemPot_K'
		Column_Step_Title = 'Step'
		Column_Water_molp_Title = 'molp_H2O'
		Column_Total_Molecules_Title = "No_mol"
		Column_Total_water_Molecules_Title = "No_waters"

		Column_Avg_Water_molp_Title = 'Avg_molp_H2O'
		Column_StdDev_Water_molp_Title = 'StdDev_molp_H2O'
		Column_Avg_E_Title = 'Avg_E_No_water_per_nm_sq'
		Column_StdDev_E_Title = 'StdDev_E_No_water_per_nm_sq'

		Extracted_Data_file_Titles = [Column_Step_Title, Column_Total_Molecules_Title, Column_Water_molp_Title ]
		Psat_ratio_list.append(np.exp (slope * ChemPot_List_corrected[j]  + intercept ))

		Step_start_string = str(int(Start_Msteps_avg_list[j]*10**6))
		Step_finish_string = str(int(End_Msteps_avg_list[j]*10**6))

		Column_Step_read_title = '#STEPS'
		Column_Step_read_title_mod = 'STEPS'
		Column_TOT_MOL_read_title =  'TOT_MOL'
		Column_MOLFRACT_H2O_read_title =  'MOLFRACT_H2O'
		Column_MOLFRACT_h2o_read_title =  'MOLFRACT_h2o'

		data_Box_0 = pd.read_csv(reading_file_Box_0, sep='\s+', header=0,
								 na_values='NaN',
								 usecols=[Column_no_Step, Column_no_Total_Molecules,
										  Column_no_Water_or_fake_water_molp_1,
										  Column_no_Water_or_fake_water_molp_2], index_col=False)

		header_orig = list(data_Box_0)
		header_mod = []
		for q in range(0, len(header_orig)):
			if header_orig[q]==Column_Step_read_title:
				header_mod.append(Column_Step_read_title_mod)
			else:
				header_mod.append(header_orig[q])

		data_Box_0.columns = header_mod


		data_Box_0 = pd.DataFrame(data_Box_0)

		data_Box_0 = data_Box_0.query(Step_start_string +' <= ' + 'STEPS'   + ' <= ' + Step_finish_string)

		Iteration_no_Box_0 = data_Box_0.loc[:,Column_Step_read_title_mod]
		Iteration_no_Box_0 = list(Iteration_no_Box_0)
		Iteration_no_Box_0 = np.transpose(Iteration_no_Box_0)

		Total_waters_list = []

		Total_Molecules_Box_0 = data_Box_0.loc[:,Column_TOT_MOL_read_title]
		Total_Molecules_Box_0 = list(Total_Molecules_Box_0)
		Total_Molecules_Box_0 = np.transpose(Total_Molecules_Box_0)

		molp_water_Box_0 = data_Box_0.loc[:, Column_MOLFRACT_H2O_read_title]
		molp_water_Box_0 = list(molp_water_Box_0)
		molp_water_Box_0 = np.transpose(molp_water_Box_0)

		molp_fake_water_Box_0 = data_Box_0.loc[:, Column_MOLFRACT_h2o_read_title]
		molp_fake_water_Box_0 = list(molp_fake_water_Box_0)
		molp_fake_water_Box_0 = np.transpose(molp_fake_water_Box_0)


		for m in range(0, len(Total_Molecules_Box_0)):
			if molp_water_Box_0[m] > molp_fake_water_Box_0[m]:
				No_water_iteration = Total_Molecules_Box_0[m] * (molp_water_Box_0[m] + molp_fake_water_Box_0[m])
			else:
				No_water_iteration = Total_Molecules_Box_0[m] * (molp_water_Box_0[m])
			Total_waters_list.append(No_water_iteration)

		for z in range(0, len(molp_water_Box_0)):
			if z > 0 and (molp_water_Box_0[z - 1] < 0.1):
				molp_water_Box_0_last = 0.1
			else:
				molp_water_Box_0_last = molp_water_Box_0[z - 1]

			if z > 0 and (molp_water_Box_0[z] < 0.1):
				molp_water_Box_0_first = 0.1
			else:
				molp_water_Box_0_first = molp_water_Box_0[z]

			if z > 0 and (molp_water_Box_0_first > 1.1 * (molp_water_Box_0_last)):
				print('**************************')
				print('Warning in ' + str(Set_List[n]) + '/' + str(
					file_folder_list[j]) + ': water may not be in a single phase for this calculation please check manually. Water may have condensed.')
				print(
					'At Step # '+str(Iteration_no_Box_0[z])+': and mol_%_water[current step] =  ' + str(molp_water_Box_0[z]) + ', and mol_%_water[previous ste] = ' + str(
						molp_water_Box_0[z - 1]))
				print('**************************')
			if z > 0 and (molp_water_Box_0_first *1.1  <  (molp_water_Box_0_last)):
				print('**************************')
				print('Warning in ' + str(Set_List[n]) + '/' + str(
					file_folder_list[j]) + ': water may not be in a single phase for this calculation please check manually. Water may have evaporated.')
				print(
					'At Step # '+str(Iteration_no_Box_0[z])+': mol_%_water[current step] =  ' + str(molp_water_Box_0[z]) + ', and and mol_%_water[previous step] = ' + str(
						molp_water_Box_0[z - 1]))
				print('**************************')
				print('')

		Total_waters_Box_0 = list(Total_waters_list)
		Total_waters_Box_0 = np.transpose(Total_waters_list)
		Total_waters_Box_0_Mean = np.nanmean(Total_waters_list)

		E_No_water_per_nm_sq = Total_waters_Box_0_Mean/surface_area_nm_sq

		Total_waters_Box_0_List.append(Total_waters_Box_0_Mean)
		E_No_water_per_nm_sq_list.append(E_No_water_per_nm_sq)

	No_waters_for_sets_list.append(Total_waters_Box_0_List)
	E_No_water_for_sets_list.append(E_No_water_per_nm_sq_list)


Avg_No_waters_for_sets_list = []
StdDev_No_waters_for_sets_list = []

Avg_E_No_water_per_nm_sq_for_sets_list = []
StdDev_E_No_water_per_nm_sq_for_sets_list = []

for h in range(0, len(No_waters_for_sets_list[0])):
	for g in range(0, len(No_waters_for_sets_list)):
		if g ==0:
			No_waters_for_sets_interation_list = [No_waters_for_sets_list[g][h]]
		else:
			No_waters_for_sets_interation_list.append(No_waters_for_sets_list[g][h])

	Avg_No_waters_for_sets_list.append(np.nanmean(No_waters_for_sets_interation_list))
	StdDev_No_waters_for_sets_list.append(np.std(No_waters_for_sets_interation_list, ddof=1))

for h in range(0, len(E_No_water_for_sets_list[0])):
	for g in range(0, len(E_No_water_for_sets_list)):
		if g ==0:
			E_No_water_for_sets_interation_list = [E_No_water_for_sets_list[g][h]]
		else:
			E_No_water_for_sets_interation_list.append(E_No_water_for_sets_list[g][h])

	Avg_E_No_water_per_nm_sq_for_sets_list.append(np.nanmean(E_No_water_for_sets_interation_list))
	StdDev_E_No_water_per_nm_sq_for_sets_list.append(np.std(E_No_water_for_sets_interation_list, ddof=1))




Box_0_data_dataframe =pd.DataFrame(np.column_stack([Psat_ratio_list,
													Avg_E_No_water_per_nm_sq_for_sets_list, StdDev_E_No_water_per_nm_sq_for_sets_list,
													Avg_No_waters_for_sets_list, StdDev_No_waters_for_sets_list,
													ChemPot_List_corrected]))

Box_0_data_dataframe.to_csv(Box_data_save_file_name + '_'+str(Chemical_being_analyzed)+'_df.txt', sep="	",
							header=[Column_Psat_ratio_Title,
									Column_Avg_E_Title, Column_StdDev_E_Title,
									Column_Avg_Water_molp_Title , Column_StdDev_Water_molp_Title,
									Column_ChemPot_Title])

Box_0_data_dataframe.to_csv(Box_data_save_file_name + '_'+str(Chemical_being_analyzed)+'_df.csv', sep=",",
							header=[Column_Psat_ratio_Title,
									Column_Avg_E_Title, Column_StdDev_E_Title,
									Column_Avg_Water_molp_Title, Column_StdDev_Water_molp_Title,
									Column_ChemPot_Title])

