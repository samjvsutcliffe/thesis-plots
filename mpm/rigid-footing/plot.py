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

line_standard, = plt.plot(0,0,ls="--",c="black",label="Standard")
line_fbar, = plt.plot(0,0,ls="-",c="black",label="F-bar")

colours = ["C0","C1","C2","C3","C4","C5","C6","C7","C8","C9"]


output_regex = re.compile("data_.*_NIL.*")
output_list = list(filter(output_regex.match,os.listdir(top_dir)))
output_list.sort()
load_scale = 1/(B*C)
for r,c in zip(output_list,colours):
    data = pd.read_csv(top_dir+r)
    values = r[:-4].split("_")
    plt.plot(data["disp"].values*-1e3,load_scale*data["load"].values,ls="--",c=c)
    #plt.plot(data["disp"].values*-1e3,load_scale*data["load"].values,ls="--",label="Standard - {}".format(values[1]))

output_regex = re.compile("data_.*_T.*")
output_list = list(filter(output_regex.match,os.listdir(top_dir)))
output_list.sort()
load_scale = 1/(B*C)
for r,c in zip(output_list,colours):
    data = pd.read_csv(top_dir+r)
    values = r[:-4].split("_")
    #plt.plot(data["disp"].values*-1e3,load_scale*data["load"].values,ls="-",label="F-bar - {}".format(values[1]))
    plt.plot(data["disp"].values*-1e3,load_scale*data["load"].values,ls="-",c=c)

analytic_solution = 2+np.pi
line_analytic = plt.axhline(analytic_solution,ls="-.",c="black",label="Analytic")
line_h1, = plt.plot(0,0,ls="-",c="C0",label="Coarse")
line_h2, = plt.plot(0,0,ls="-",c="C1",label="Medium")
line_h3, = plt.plot(0,0,ls="-",c="C2",label="Fine")

#lines = axes.get_lines()
ax = plt.gca()
legend1 = ax.legend(handles=[line_analytic,line_standard,line_fbar], loc="upper left")
ax.add_artist(legend1)
# legend2 = ax.legend(handles=[line_h1,line_h2,line_h3],["Coarse","Medium","Fine"], loc=4)
legend2 = ax.legend(handles=[line_h1,line_h2,line_h3], loc=4)
ax.add_artist(legend2)
# plt.legend()
plt.xlabel("Displacement (mm)")
plt.ylabel("Normalised Load")
plt.xlim(0,2)
plt.ylim(bottom=0)
plt.tight_layout()
plt.savefig("paper.pgf")
plt.show()
