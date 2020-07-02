import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import csv as csv
import pandas as pd
import itertools as it
from collections import defaultdict
import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.axis as axis
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import math
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
import pylab as plot

#********************************
#Notes
#********************************

#Plots 2 item:
#1) a pairwise energy for indiviual peeling strands, and non-peeling strands
#2)
#********************************
#End Notes
#********************************
# only change the below reading_file
Chemical_name = 'water'
Psat_at_298K = 0.0031505367196597

axis_Label_font_size = 24
legend_font_size = 18
axis_number_font_size = 20

PointSizes = 8
ConnectionLineSizes = 2
Reg_Density_Linestyle = '--'  #'-' =  solid, '--' = dashed, ':'= dotted
Critical_Density_Linestyle = None


#**************
# P vs T plot ranges (start)
#*************
P_min = 0.0
P_max = 0.2

P_ticks_major = 0.05
P_ticks_minor = 0.1


#**************
# P vs T plot ranges (end)
#*************

calc_data_reading_name = "Avg_data_from Box_0_"+str(Chemical_name)+"_df.txt"

P_vs_Fugacity_saving_name = "Pvap_vs_Antoine_data_"+str(Chemical_name)+".pdf"


Color_for_Plot_Data = 'saddlebrown' 		#black
Color_for_Plot_Critical_Data_calc =  'b'  #gray
Color_for_Plot_Critical_Data_exp =  'r'  #gray




#********************************
#  File importing 
#********************************



calc_data = pd.read_csv(calc_data_reading_name,  sep='\s+', index_col=0)
calc_data_df = pd.DataFrame(calc_data)

Psat_ratio = calc_data_df.loc[:, 'Psat_ratio' ]


Fugacity_calc = calc_data_df.loc[:, 'Fugacity_bar']
Fugacity_ln_P_calc = Fugacity_calc
#Fugacity_ln_P_calc = [np.log(i) for i in Fugacity_calc]


P_calc = calc_data_df.loc[:, 'P_bar']
ln_P_calc = P_calc
#ln_P_calc = [np.log(i) for i in P_calc]

P_from_IG_calc = calc_data_df.loc[:, 'P_from_IG_Density_bar']

#********************************
#  End File importing for Final States
#********************************



# ********************************
#  End File importing
# ********************************




#****************************************
#Plot Number 2  (P vs T) (start)
#****************************************

# Plotting curve data below

fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)
#ax2 = ax1.twiny()

for tick in ax1.xaxis.get_ticklabels():
    tick.set_fontname('Arial')
for tick in ax1.yaxis.get_ticklabels():
    tick.set_fontname('Arial')

plt.xlabel('f = Fugacity (bar)', fontname="Arial", fontsize=axis_Label_font_size)
plt.ylabel('$P_{vap}$ (bar)', fontname="Arial", fontsize=axis_Label_font_size)

File_label_Density = 'Calc'
File_label_Density_Critical_calc = 'Calc'
File_label_Density_Critical_exp = 'Exp'

print('Fugacity, = '+str(Fugacity_calc))
print(' P_calc, = '+str( P_calc))
# Matplotlib colors b : blue, g : green, r : red, c : cyan, m : magenta, y : yellow, k : black, w : white, gray='x' (x=0 to 1)
plt.plot(Fugacity_calc, P_calc  , color='b', marker='D', linestyle='none' , markersize=PointSizes, linewidth=ConnectionLineSizes, fillstyle='full', label= "$P_{virial}$") #label=File_label_No1
plt.plot(P_from_IG_calc, P_calc  , color='r', marker='o', linestyle='none' , markersize=PointSizes, linewidth=ConnectionLineSizes, fillstyle='full', label= "$P_{I.G. calc}$") #label=File_label_No1
plt.plot([0, P_max], [0, P_max] , color='k', marker=None, linestyle=':' , markersize=PointSizes, linewidth=ConnectionLineSizes, fillstyle='none', label= "$P_{I.G.}$ = f") #label=File_label_No1
legend1 = ax1.legend(loc='upper center', shadow=True, fontsize=legend_font_size )

major_xticks = np.arange(P_min, P_max+0.001, P_ticks_major)
major_yticks = np.arange(P_min, P_max+0.001, P_ticks_major)

minor_xticks = np.arange(P_min, P_max+0.001, P_ticks_minor )
minor_yticks = np.arange(P_min, P_max+0.001, P_ticks_minor)


#plt.gca().set_xlim(left=2, right=105)

ax1.set_xticks(major_xticks)
ax1.set_xticks(minor_xticks, minor=True)
ax1.set_yticks(major_yticks)
ax1.set_yticks(minor_yticks, minor=True)


ax1.tick_params(axis='both', which='major', length=4, width=2, labelsize=axis_number_font_size, top=True, right=True)
ax1.tick_params(axis='both', which='minor', length=4, width=1, labelsize=axis_number_font_size, top=True, right=True)
"""
new_tick_locations = np.array(P_calc)
def tick_function(X):
    P_sat_ratio =  P_calc#X/Psat_at_298K
    return ["%.3f" % z for z in P_sat_ratio]

ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(tick_function(new_tick_locations))
ax2.set_xlabel(r"Modified x-axis: $1/(1+X)$")

ax2.tick_params(axis='both', which='major', length=4, width=2, labelsize=axis_number_font_size, top=True, right=True)
ax2.tick_params(axis='both', which='minor', length=4, width=1, labelsize=axis_number_font_size, top=True, right=True)
"""
leg1 = ax1.legend(loc='upper left', shadow=True, fontsize=legend_font_size ,prop={'family':'Arial','size': legend_font_size})

plt.tight_layout()  # centers layout nice for final paper
# plt.gcf().subplots_adjust(bottom=0.15) # moves plot up so x label not cutoff
plt.xlim(P_min, P_max)  # set plot range on x axis
plt.ylim(P_min, P_max)  # set plot range on y axis

plt.gcf().subplots_adjust(left=0.25, bottom=None, right=0.90, top=None, wspace=None, hspace=None) # moves plot  so x label not cutoff

frame1 = legend1.get_frame()
frame1.set_facecolor('0.90')

plt.legend(ncol=1,loc='upper left', fontsize=legend_font_size, prop={'family':'Arial','size': legend_font_size})
plt.show()



plt.show()
fig1.savefig(P_vs_Fugacity_saving_name)
#****************************************
#Plot Number 1  P vs T) (end)
#****************************************

