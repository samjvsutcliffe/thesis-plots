import matplotlib.pyplot as plt
import pandas as pd
import json
import os,re

plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
scale = 2
width = 3.487*scale
# height = width / 1.400
height = width / 1.618

top_dir = "/mnt/c/Temp/mici/"#"./data/"
output_dir = top_dir+"output-CRYO-0.25-800.0-0.8/"

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
ax_damage.plot(time,damage ,label="Damage",color="black")
ax.plot(time,energy,label="Energy")
ax.plot(time,oobf,label="OOBF")
ax.axhline(thresh_oobf,c="green",ls="--")
quasi_point = None
for i in range(len(df)-1):
    if df["step-type"].iloc[i] == "DYNAMIC":
        if quasi_point == None:
            quasi_point = time[i]
    else:
        if quasi_point:
            plt.axvspan(quasi_point,time[i],alpha=0.25,color="black")
            quasi_point = None
if quasi_point:
    plt.axvspan(quasi_point,time[i],alpha=0.25,color="black")

plt.axvspan(0,0,alpha=0.25,color="black",label="Collapse stage")

plt.xlabel("Time (s)")
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax_damage.get_legend_handles_labels()
ax_damage.legend(lines+lines2, labels+labels2, loc=0)
ax_damage.set_ylim(bottom=0)
ax.set_ylabel("Dynamic criteria")
ax.set_xlabel("Time (s)")
ax.set_ylim(bottom=1e-4)
ax_damage.set_ylabel("Mass-Damage (kg)")
plt.tight_layout()
plt.savefig("de.pdf")
plt.show()
