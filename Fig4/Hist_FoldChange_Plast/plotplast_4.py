import os
import time
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import matplotlib

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import histarrows as histarrows
n_bins = 20

number = 4

matplotlib.rcParams.update({'font.weight':'bold', 'xtick.color':'0.3', 'ytick.color':'0.3', 'axes.labelweight':'bold', 'axes.titleweight':'bold', 'figure.titleweight':'bold', 'text.color':'0.3', 'axes.labelcolor':'0.3', 'axes.titlecolor':'0.3', 'font.size': '30', 'axes.titlesize':'40', 'axes.labelsize':'35', 'xtick.labelsize':'33', 'ytick.labelsize':'30', 'legend.fontsize':'30'})

topofiles= [os.path.splitext(f)[0] for f in listdir("topofiles4/") if isfile(join("topofiles4/", f))]

topofiles.sort()

print(topofiles)


plast=np.loadtxt("plastnetwork.txt")



#---------------------------------------------
number = 4
n_bins  = 20  
r = 2
matplotlib.rcParams.update({'font.size': 10*r})  
fig,ax = plt.subplots()
valarr = plast
names = ["GRHL2" , "GRHL2wa", "OVOL", "OVOLsi"]
colours = ['r', 'g', 'm', 'k']
coords = [0.770996398,0.848018925,0.782366951,0.790414021]
histarrows.histogram(ax, valarr, coords, names, colours, n_bins)   

plt.xlabel("Avg. fold change in Plasticity", fontweight="bold" , c='0.3')
plt.ylabel("No. of Random networks" , fontweight="bold" , c='0.3')
#plt.title("Networks (Size {})".format(number), fontweight="bold" , c='0.3')

f=r*np.array(plt.rcParams["figure.figsize"])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(f)
ax.set_ylim([0,28])
plt.tight_layout()

plt.savefig("plastfoldhist4.png", transparent = True)


plt.clf()
#---------------------------------------------

        



    