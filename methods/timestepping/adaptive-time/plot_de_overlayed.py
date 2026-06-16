import matplotlib as mpl
import matplotlib.pyplot as plt
import json
import pandas as pd
import re
import os

# plt.style.use("seaborn-paper")
# plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
# plt.rc('xtick', labelsize=8)
# plt.rc('ytick', labelsize=8)
# plt.rc('axes', labelsize=8)
# plt.rcParams['figure.constrained_layout.use'] = True


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
fig = plt.figure(figsize=(width,height))

top_dir = "./data/"
output_regex = re.compile("output-*")
output_list = list(filter(output_regex.match,os.listdir(top_dir)))
output_list.sort()
for i,out in enumerate(output_list):
    print("{}: {}".format(i,out))


ax = fig.gca()
lines = ["dotted","dashed","-","-"]
mk = ["x","o","",""]
for ls,outdir,m in zip(lines,output_list,mk):
    output_dir = "{}./{}/".format(top_dir,outdir)
    df = pd.read_csv(output_dir+"timesteps.csv")
    time = df["time"].values
    step = df["steps"].values
    damage = df["damage"].values
    plt.plot(time,damage ,label=outdir,ls=ls,marker=m)

plt.xlabel("Time (s)")
plt.ylabel("Mass-damage (Kg)")
plt.legend(["Adaptive $\Delta d_{max}=0.1$",
"Adaptive $\Delta d_{max}=0.5$",
"Constant $\Delta t=0.5$ (s)",
"Constant $\Delta t=10$ (s)",
            ])
# plt.legend([])
plt.savefig("damage-time.pdf")
plt.show()
