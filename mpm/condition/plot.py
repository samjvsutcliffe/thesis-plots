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
    }
)
width = 1*5.90666
height = width / 1.4
plt.figure(figsize=(width,height))

output_dir = "data.csv"
df = pd.read_csv(output_dir)
x = df["X"].values
ma = df["MA"].values
mii = df["M-LUMPED"].values
plt.plot(x+0.5,ma,label="Aggregate")
plt.plot(x+0.5,mii,label="Lumped")


df = pd.read_csv("data_1e-15.csv")
x = df["X"].values
ma = df["MA"].values
mii = df["M-LUMPED"].values
plt.plot(x+0.5,mii,label="Filtered lumped $f_m = 10^{-15}$")

plt.xlabel("Normalised displacement (x/h)")
plt.ylabel("Condition number")
plt.yscale("log")
plt.xlim(0.5,1.5)
plt.gca().set_xticks(np.linspace(0.5,1.5,5))
plt.legend()
plt.tight_layout()
plt.savefig("paper.pgf")
plt.show()
