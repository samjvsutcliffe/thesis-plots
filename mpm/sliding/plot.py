import matplotlib as mpl
#mpl.use('pdf')
#mpl.use("pgf")
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
width = 0.5*5.90666
height = width / 1.3


B = 1
C = 1e6

plt.figure(figsize=(width,height))

top_dir = "./results/"


output_regex = re.compile(".*\.csv")
output_list = list(filter(output_regex.match,os.listdir(top_dir)))
output_list.sort()
load_scale = 1/(B*C)
for r in output_list:
    data = pd.read_csv(top_dir+r)
    values = r[:-4].split("_")
    plt.plot(data["disp"].values*1e3,load_scale*data["load"].values,ls="--",label="Standard")

plt.legend()
plt.xlabel("Displacement (mm)")
plt.ylabel("Fricional load (Pa)")
#plt.xlim(0,2)
plt.ylim(bottom=0)
plt.tight_layout()
plt.savefig("paper.pgf")
plt.show()
