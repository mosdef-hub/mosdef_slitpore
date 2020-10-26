import numpy as np
import matplotlib.pyplot as plt
import csv as csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']


Chemical_name = 'water'

axis_Label_font_size = 24
legend_font_size = 18
axis_number_font_size = 20

PointSizes = 8
ConnectionLineSizes = 2
Reg_Density_Linestyle = '--'  #'-' =  solid, '--' = dashed, ':'= dotted
Critical_Density_Linestyle = None


ChemPot_min = -6000
ChemPot_max = -3000

ChemPot_ticks_major = 1000
ChemPot_ticks_minor = 100

P_min = 0.0
P_max = 0.2

P_ticks_major = 0.05
P_ticks_minor = 0.1



Psat_data_file = '../../../Psat_SPCE_298K/gomc/analysis/SPCE_Pvap_at_298K_df.csv'
Psat_data = pd.read_csv(Psat_data_file, sep=',', header=0, na_values='NaN',
						usecols=[0,1], index_col=False)

Psat_data = pd.DataFrame(Psat_data)
print(Psat_data)

Psat_SPEC_data_bar = Psat_data.loc[:,'Avg_Pvap_bar']
Psat_SPEC_data_bar = list(Psat_SPEC_data_bar)[0]
print('Psat_SPEC_data_bar = '+str(Psat_SPEC_data_bar))
Psat_at_298K = Psat_SPEC_data_bar

calc_data_reading_name = "Avg_data_from Box_0_"+str(Chemical_name)+"_df.txt"

P_vs_ChemPot_saving_name = "Pvap_vs_Antoine_data_"+str(Chemical_name)+".pdf"


Color_for_Plot_Data = 'saddlebrown' 		#black
Color_for_Plot_Critical_Data_calc =  'b'  #gray
Color_for_Plot_Critical_Data_exp =  'r'  #gray


calc_data = pd.read_csv(calc_data_reading_name,  sep='\s+', index_col=0)
calc_data_df = pd.DataFrame(calc_data)

Psat_ratio = calc_data_df.loc[:, 'Psat_ratio' ].tolist()

ChemPot_calc = calc_data_df.loc[:, 'ChemPot_K'].tolist()

P_calc = calc_data_df.loc[:, 'P_bar'].tolist()


P_from_IG_calc = calc_data_df.loc[:, 'P_from_IG_Density_bar'].tolist()


# Plotting curve data below
fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)


for tick in ax1.xaxis.get_ticklabels():
    tick.set_fontname('Arial')
for tick in ax1.yaxis.get_ticklabels():
    tick.set_fontname('Arial')

plt.xlabel('$\mu$ = ChemPot (K)', fontname="Arial", fontsize=axis_Label_font_size)
plt.ylabel('$P_{vap}$ (bar)', fontname="Arial", fontsize=axis_Label_font_size)

File_label_Density = 'Calc'
File_label_Density_Critical_calc = 'Calc'
File_label_Density_Critical_exp = 'Exp'

print('ChemPot, = '+str(ChemPot_calc))
print(' P_calc, = '+str( P_calc))

plt.plot(ChemPot_calc, P_calc  , color='b', marker='D', linestyle='none' , markersize=PointSizes, linewidth=ConnectionLineSizes, fillstyle='full', label= "$P_{virial}$") #label=File_label_No1
plt.plot(ChemPot_calc, P_from_IG_calc  , color='r', marker='o', linestyle='none' , markersize=PointSizes, linewidth=ConnectionLineSizes, fillstyle='full', label= "$P_{I.G. calc}$") #label=File_label_No1
legend1 = ax1.legend(loc='upper center', shadow=True, fontsize=legend_font_size )

major_xticks = np.arange(ChemPot_min, ChemPot_max+0.001, ChemPot_ticks_major)
major_yticks = np.arange(P_min, P_max+0.001, P_ticks_major)

minor_xticks = np.arange(ChemPot_min, ChemPot_max+0.001, ChemPot_ticks_minor )
minor_yticks = np.arange(P_min, P_max+0.001, P_ticks_minor)



ax1.set_xticks(major_xticks)
ax1.set_xticks(minor_xticks, minor=True)
ax1.set_yticks(major_yticks)
ax1.set_yticks(minor_yticks, minor=True)


ax1.tick_params(axis='both', which='major', length=4, width=2, labelsize=axis_number_font_size, top=True, right=True)
ax1.tick_params(axis='both', which='minor', length=4, width=1, labelsize=axis_number_font_size, top=True, right=True)

leg1 = ax1.legend(loc='upper left', shadow=True, fontsize=legend_font_size ,prop={'family':'Arial','size': legend_font_size})

plt.tight_layout()
plt.xlim(ChemPot_min, ChemPot_max)
plt.ylim(P_min, P_max)

plt.gcf().subplots_adjust(left=0.25, bottom=None, right=0.90, top=None, wspace=None, hspace=None)

frame1 = legend1.get_frame()
frame1.set_facecolor('0.90')

plt.legend(ncol=1,loc='upper left', fontsize=legend_font_size, prop={'family':'Arial','size': legend_font_size})
plt.show()



plt.show()
fig1.savefig(P_vs_ChemPot_saving_name)
#****************************************
#Plot Number 1  P vs T) (end)
#****************************************

