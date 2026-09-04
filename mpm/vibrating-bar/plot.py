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
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
mpl.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "font.serif": ["Computer Modern"],
        "text.usetex": True,
        "pgf.rcfonts": False,
        'figure.constrained_layout.use':True
    }
)

width = 5.90666
height = width / 1.618

data = pd.read_csv("data.csv")

time = data["time"].values
energy_usf = data["energy-USF"].values
energy_usl = data["energy-USL"].values
energy_musl = data["energy-MUSL"].values

fig = plt.figure(figsize=(width,height))
# plt.plot(time,energy_usf,label="USF")
# plt.plot(time,energy_usl,label="USL")
# plt.plot(time,energy_musl,label="MUSL")
# plt.xlabel("Time (s)")
# plt.ylabel("Energy (J)")

ax = fig.gca()
e_init = 250
top_dir = "./data/"
output_regex = re.compile("output-*")
output_list = list(filter(output_regex.match,os.listdir(top_dir)))
output_list.sort()
output_list = [
    "./output-USF/",
    "./output-USL/",
    "./output-MUSL/"]
for outdir in output_list:
    output_dir = "{}./{}/".format(top_dir,outdir)
    print(output_dir)
    df = pd.read_csv(output_dir+"timesteps.csv")
    time = df["time"].values
    step = df["steps"].values
    ke = df["ke"].values
    se = df["se"].values
    gpe = df["gpe"].values
    plt.plot(time,(ke + se)/e_init)
plt.xlabel("Time (s)")
plt.ylabel("Normalised energy ratio")
plt.legend(["USF","USL","MUSL"])
plt.savefig("paper.pdf")
# plt.savefig("paper.pgf")
plt.show()
