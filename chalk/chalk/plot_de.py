import matplotlib.pyplot as plt
import pandas as pd
import json
import os,re

chalk_dir ="/nobackup/rmvn14/ham-chalk-conv/" 
output_regex = re.compile("output*")                                 
output_list = list(filter(output_regex.match,os.listdir(chalk_dir)))
output_list.sort()
for i,out in enumerate(output_list):                                    
    print("{}: {}".format(i,out))                                       

output_dir = chalk_dir + "./{}/".format(output_list[int(input())]) 
df = pd.read_csv(output_dir+"timesteps.csv")

with open(output_dir+"./settings.json") as f:
    json_settings = json.load(f)
    h = json_settings["RESOLUTION"]
    xlim = [0,json_settings["DOMAIN-SIZE"][0]]
    ylim = [0,json_settings["DOMAIN-SIZE"][1]]
    thresh_energy = [0,json_settings["DOMAIN-SIZE"][1]]
    thresh_energy = json_settings["CRITERIA-ENERGY"]
    thresh_oobf = json_settings["CRITERIA-OOBF"]
    #ylim[0] = 20

fig,ax = plt.subplots()
ax_damage = ax.twinx()
thresh_scale = 0.1
#thresh_energy = 1e-1
#thresh_oobf = 1e-1

time = df["time"].values
#time = df["steps"].values
print(df)
ax_damage.plot(time,df["damage"] ,label="Damage",color="black")
ax.plot(time,df["energy"] ,label="Energy")
ax.plot(time,df["oobf"] ,label="OOBF")
ax.axhline(thresh_oobf,c="green",ls="--")

quasi_point = None
for i in range(len(df)-1):
    if df["step-type"].iloc[i] == "COLLAPSE":
        if quasi_point == None:
            quasi_point = time[i]
    else:
        if quasi_point:
            plt.axvspan(quasi_point,time[i],alpha=0.25,color="black")
            quasi_point = None
if quasi_point:
    plt.axvspan(quasi_point,time[i],alpha=0.25,color="black")
ax.set_yscale("log")
ax.set_ylabel("Dynamic criteria")
ax.set_xlabel("Time (s)")
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax_damage.get_legend_handles_labels()
ax_damage.legend(lines+lines2, labels+labels2, loc=0)
#plt.legend()
plt.savefig("de.pdf")
plt.show()
