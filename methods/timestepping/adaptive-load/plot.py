import matplotlib as mpl
#mpl.use('pdf')
#mpl.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os
import numpy as np
import re

# plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)

mpl.rcParams.update(
    {
        # "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        # "pgf.rcfonts": False,
        'figure.constrained_layout.use':True
    }
)
width = 5.90666
height = width / 1.7
plt.figure(figsize=(width,height))

from scipy import integrate

def extract_vals(f):
    output,refine,load = f.split("-")
    #refine = float(refine)
    return refine,float(load)

from scipy import integrate
def calculate_gf(disp,load):
    i = 0#np.argmax(load)
    print("Max at {}mm".format(disp[i]*1e3))
    return integrate.trapz(load[i:],disp[i:])

top_dir = "./data/"
regex = re.compile(r'^output.*')
folders = list(filter(regex.search,os.listdir(top_dir)))


def get_load(filename):
    mpm = pd.read_csv(top_dir+filename)
    mpm["disp"] = mpm["disp"]
    mpm["load"] = mpm["load"]
    return mpm

regex = re.compile(r'^output-\d+')
folders = list(filter(regex.search,os.listdir(top_dir)))
folders.sort()
print(folders)
for i in folders:
    print("loading folder: ",i)
    mpm = get_load("./{}/disp.csv".format(i))
    if len(mpm["load"]) > 0:
        l = plt.plot(mpm["disp"].values*1e3,mpm["load"].values,marker="",label=i,ls="-")
        print("GF ",i," :",calculate_gf(mpm["disp"],mpm["load"]))

regex = re.compile(r'^output-adaptive-\d*')
folders = list(filter(regex.search,os.listdir(top_dir)))
folders.sort()
print(folders)
for i in folders:
    print("loading folder: ",i)
    mpm = get_load("./{}/disp.csv".format(i))
    if len(mpm["load"]) > 0:
        plt.plot(mpm["disp"].values*1e3,mpm["load"].values,marker="x",label=i,ls="--")
        print("GF ",i," :",calculate_gf(mpm["disp"],mpm["load"]))
plt.xlabel("Displacement (mm)")
plt.ylabel("Load (N)")
plt.legend()
#plt.legend()
# plt.legend(["Coarse","Medium","Fine"])
plt.legend(["8 load-steps","80 load-steps","Adaptive criteria $\Delta d_{max}=0.1$","Adaptive criteria $\Delta d_{max} = 0.8$"])
# plt.legend(["Eikonal localisation","Novel damage localisation", "Standard damage localisation", "Constant length"])
# plt.savefig("paper.pdf")
plt.savefig("paper.pgf")
plt.show()
