import matplotlib.pyplot as plt
import json
import pandas as pd
import re
import os

plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
plt.rcParams['figure.constrained_layout.use'] = True

top_dir = "./data/"
output_regex = re.compile("output-*")
output_list = list(filter(output_regex.match,os.listdir(top_dir)))
output_list.sort()
for i,out in enumerate(output_list):
    print("{}: {}".format(i,out))


fig = plt.figure()
ax = fig.gca()
lines = ["dotted","dashed","dashdot",":","-"]
for ls,outdir in zip(lines,output_list):
    output_dir = "{}./{}/".format(top_dir,outdir)
    df = pd.read_csv(output_dir+"timesteps.csv")
    time = df["time"].values
    step = df["steps"].values
    damage = df["damage"].values
    plt.plot(time,damage ,label=outdir,marker="x",ls=ls)

plt.xlabel("Time (s)")
plt.ylabel("Mass-damage (Kg)")
plt.legend()
plt.savefig("damage-time.pdf")
plt.show()
