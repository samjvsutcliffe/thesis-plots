import matplotlib.pyplot as plt
import pandas as pd
import json
import os,re
import numpy as np

plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
#scale = 1
#width = 3.487*scale
#height = width / 1.618
#width = 3.487 * 1
#height = width / 1.5
width = 3.487
height = width / 1.5

#chalk_dir ="/nobackup/rmvn14/ham-chalk/" 
chalk_dir = "/nobackup/rmvn14/ham-chalk-conv/"
output_regex = re.compile("output*")                                 
output_list = list(filter(output_regex.match,os.listdir(chalk_dir)))
output_list.sort()
with open(chalk_dir+output_list[-1]+"/settings.json") as f:
    json_settings = json.load(f)
    thresh_energy = json_settings["CRITERIA-ENERGY"]
    thresh_oobf = json_settings["CRITERIA-OOBF"]
    #thresh_hist = json_settings["CRITERIA-HIST"]
    #final_step = json_settings["MAX-STEPS"]-1
    tau = 1#json_settings["DELAY-TIME"]
fig,ax_damage = plt.subplots(figsize=(width,height),dpi=200)
# ax_oobf = ax_oobf.twinx()
#ax_oobf.set_ylim(0,thresh_energy*thresh_hist*2)
#ax_oobf.axhline(thresh_energy*(thresh_hist),c="green",ls="--")
#ax_oobf.axhline(thresh_energy/(thresh_hist),c="red",ls="--")
#ax_oobf.set_ylim(0,thresh_energy*thresh_hist*2)
#ax_oobf.axhline(thresh_oobf,c="green",ls="--")

print(tau)
key_lines = []
key_labels = []
for i,out in enumerate(output_list):                                    
    output_dir = chalk_dir + "./{}/".format(out)
    if os.path.isfile(output_dir+"timesteps.csv"):
        ms = float(out.split("-")[-1])
        df = pd.read_csv(output_dir+"timesteps.csv")

        time = df["time"].values
        #time = df["steps"].values

        oobf = df["oobf"].values
        energy = df["energy"].values
        damage = df["damage"].values
        first = True
        first_time = -2
        collapse = (energy > thresh_energy) | (oobf > thresh_oobf)
        for i in range(len(df)-1):
            if collapse[i] != collapse[i+1] and first:
                ##Transition found
                first = False
                x = time[i+1]
                first_time=i+1
                #plt.axvline(x,c=colour)
                ax_damage.scatter(time[i+1],damage[i+1],marker="x",c="black")
                #plt.text(x+1,0,'Transition to {}'.format(df["step-type"].values[i+1]),rotation=90)
        l = ax_damage.plot(time,damage,label="h = {:.3f} m".format(ms))
        key_lines.append(l[0])
        key_labels.append("h = {:.3f} m".format(ms))
        colour = l[0].get_color()
        l = ax_damage.plot(time,damage,label="s = {}".format(ms),ls="--",color=colour)
        #lss = ax_oobf.plot(time,oobf,label="s = {}".format(ms),ls="--",c=colour)
        #quasi_point = None
        #for i in range(len(df)-1):
        #    if df["step-type"].iloc[i] == "COLLAPSE":
        #        if quasi_point == None:
        #            quasi_point = time[i]
        #    else:
        #        if quasi_point:
        #            plt.axvspan(quasi_point,time[i],alpha=0.25,color=colour)
        #            quasi_point = None
        #if quasi_point:
        #    plt.axvspan(quasi_point,time[i],alpha=0.25,color=colour)
        #if len(df)>0 and df["steps"].values[-1] == final_step:
        #    ax_damage.scatter(time[-1],damage[-1],marker="x",c="black")
plt.ylabel("Mass-Damage (Kg)")
plt.xlabel("Time (s)")
#with open(output_dir+"./settings.json") as f:
#    json_settings = json.load(f)
#    h = json_settings["RESOLUTION"]
#    xlim = [0,json_settings["DOMAIN-SIZE"][0]]
#    ylim = [0,json_settings["DOMAIN-SIZE"][1]]
#    thresh_energy = [0,json_settings["DOMAIN-SIZE"][1]]
#    thresh_energy = json_settings["CRITERIA-ENERGY"]
#    thresh_oobf = json_settings["CRITERIA-OOBF"]
#    thresh_hist = json_settings["CRITERIA-HIST"]
#    #ylim[0] = 20
#
#thresh_scale = 0.1
##thresh_energy = 1e-1
##thresh_oobf = 1e-1
#
##df["time"] = np.arange(0,len(df))
#print(df)
#plt.plot(df["time"],df["damage"]/df["damage"].max() ,label="Damage")
#plt.plot(df["time"],thresh_scale*df["energy"]/thresh_energy ,label="Energy")
#plt.plot(df["time"],thresh_scale*df["oobf"]/thresh_oobf ,label="OOBF")
##plt.plot(df["time"],df["mass"]/thresh_oobf ,label="Mass")
#plt.axhline(thresh_scale*(thresh_hist),c="green",ls="--")
#plt.axhline(thresh_scale/(thresh_hist),c="red",ls="--")
#for i in range(len(df)-1):
#    if df["step-type"].iloc[i] != df["step-type"].iloc[i+1]:
#        ##Transition found
#        x = df["time"].values[i+1]
#        plt.axvline(x)
#        plt.text(x+1,0,'Transition to {}'.format(df["step-type"].values[i+1]),rotation=90)
ax_damage.set_ylim(bottom=0,top=None)
#lines, labels = ax_oobf.get_legend_handles_labels()
#lines2, labels2 = ax_damage.get_legend_handles_labels()
#ax_damage.legend(lines2, labels2, loc=0)
print(key_lines)
#plt.legend()
#ax_oobf.set_yscale("log")
#ax_oobf.set_xlim(right=1000)
ax_damage.set_xlim(left=0,right=800)
#ax_oobf.set_ylabel("Dynamic criteria")
ax_damage.set_ylabel("Mass-Damage (kg)")
#ax_oobf.set_xlabel("Time (s)")
ax_damage.legend(key_lines,key_labels,loc="lower right")
ax_damage.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.tight_layout()
plt.savefig("decomb.pdf")
#plt.savefig("de.pdf")
plt.show()
