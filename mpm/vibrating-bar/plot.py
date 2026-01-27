import matplotlib as mpl
#mpl.use('pdf')
mpl.use("pgf")
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import re

from scipy import integrate
PDF_OUTPUT = False


#plt.rc('font', family='serif', serif='Times')
## plt.rc('text', usetex=True)
#plt.rc('xtick', labelsize=8)
#plt.rc('ytick', labelsize=8)
#plt.rc('axes', labelsize=8)
plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)

mpl.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
    }
)
width = 5.90666
height = width / 1.618

data = pd.read_csv("data.csv")

time = data["time"].values
energy_usf = data["energy-USF"].values
energy_usl = data["energy-USL"].values
energy_musl = data["energy-MUSL"].values

plt.figure(figsize=(width,height))
plt.plot(time,energy_usf,label="USF")
plt.plot(time,energy_usl,label="USL")
plt.plot(time,energy_musl,label="MUSL")
plt.xlabel("Time (s)")
plt.ylabel("Energy (J)")
plt.tight_layout()
plt.legend()
plt.savefig("paper.pgf")
plt.show()
