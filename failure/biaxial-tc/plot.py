import matplotlib as mpl
#mpl.use('pdf')
#mpl.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os
import numpy as np
import re

plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)

mpl.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
        'figure.constrained_layout.use':True
    }
)
width = 0.6*5.90666
height = width / 1.4
plt.figure(figsize=(width,height))

from scipy import integrate

def extract_vals(f):
    output,refine,load = f.split("-")
    #refine = float(refine)
    return refine,float(load)

from scipy import integrate
def calculate_gf(disp,load):
    i = np.argmax(load)
    print("Max at {}mm".format(disp[i]*1e3))
    return integrate.trapz(load[i:],disp[i:])

top_dir = "./data/"
regex = re.compile(r'^output.*')
folders = list(filter(regex.search,os.listdir(top_dir)))
def get_load(filename):
    mpm = pd.read_csv(top_dir+filename)
    mpm["disp"] = mpm["disp"].abs()
    mpm["load"] = mpm["load"].abs()
    return mpm


folders.sort()
print(folders)
folders = ["output-C-MC-30.0-4.0", "output-T-MC-30.0-4.0",]

for i in folders:
    print("loading folder: ",i)
    loadfile = "./{}/load-disp.csv".format(i)
    if os.path.isfile(top_dir+loadfile):
        mpm = get_load(loadfile)
        if len(mpm["load"]) > 0:
            plt.plot(mpm["disp"].values*1e3,mpm["load"].values,label=i)
            print("GF ",i," :",calculate_gf(mpm["disp"],mpm["load"]))
plt.xlabel("Displacement (mm)")
plt.ylabel("Load (N)")
#plt.legend()
plt.legend(["Compression","Tension"])
plt.savefig("paper.pgf")
plt.show()
