import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import json
import os,re

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
plt.rcParams["lines.markeredgewidth"] = 1

width = 5.90666
height = width / 1.7
# scale = 2
# width = 3.487*scale
# # height = width / 1.400
# height = width / 1.618

top_dir = "./data/"
# flist = "output-PAPER_EXPLICT_PSI_erode_NIL_600.0/"
flist = os.listdir(top_dir)
flist = flist[2]
output_dir = "{}/{}/".format(top_dir,flist)

df = pd.read_csv(output_dir+"timesteps.csv")

with open(output_dir+"./settings.json") as f:
    json_settings = json.load(f)
    h = json_settings["RESOLUTION"]
    xlim = [0,json_settings["DOMAIN-SIZE"][0]]
    ylim = [0,json_settings["DOMAIN-SIZE"][1]]
    thresh_energy = json_settings["CRITERIA-ENERGY"]
    thresh_oobf = json_settings["CRITERIA-OOBF"]

thresh_scale = 0.01

fig,ax = plt.subplots(figsize=(width,height),dpi=200)
ax_damage = ax.twinx()
ax.set_yscale("log")
time = df["time"].values
damage = df["damage"].values
energy = df["energy"].values
oobf = df["oobf"].values
# plt.xlim([00,400])
ax_damage.plot(time,damage,label="Damage",c="black",marker="x")
ax.plot(time,energy,label="Energy")
ax.plot(time,oobf,label="Residual")
ax.axhline(thresh_oobf,c="green",ls="--")

colour_map = {"QUASI-STATIC":"none","DYNAMIC":"black","ACCELERATE":"green"}
quasi_point = time[0]
quasi_type = df["step-type"].iloc[0]
for i in range(1,len(df)):
    step_type = df["step-type"].iloc[i]
    if not quasi_type == step_type:
        plt.axvspan(quasi_point,time[i-1],alpha=0.25,color=colour_map[quasi_type])
        quasi_type = step_type
        quasi_point = time[i-1]
        plt.axvspan(quasi_point,time[i],alpha=0.25,color=colour_map[quasi_type])

plt.xlabel("Time (s)")
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax_damage.get_legend_handles_labels()
ax_damage.legend(lines+lines2, labels+labels2, loc=0)
ax_damage.set_ylim(bottom=0)
ax.set_ylabel("Dynamic criteria")
ax.set_xlabel("Time (s)")
ax.set_ylim(bottom=1e-4)
ax_damage.set_ylabel("Mass-Damage (kg)")
# plt.tight_layout()
plt.savefig("de.pdf")
# plt.xlim([0,1e6])
# plt.savefig("de_cropped.pdf")
plt.show()
