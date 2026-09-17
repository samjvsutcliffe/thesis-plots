import matplotlib as mpl
mpl.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os
import numpy as np
import re

from scipy import integrate


plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
plt.rcParams['figure.constrained_layout.use'] = True

mpl.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
        "pgf.preamble": "\n".join([
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[detect-all]{siunitx}",
        ])
    }
)
width = 0.5*5.90666
height = width / 1.3


B = 1
C = 1e6


def extract_vals(f):
    output,refine,load = f.split("-")
    #refine = float(refine)
    return refine,float(load)

top_dir = "./data/"
regex = re.compile(r'^output-.*')
folders = list(filter(regex.search,os.listdir(top_dir)))
print(folders)
names = folders
folders = [
    "output-16.0_2_1.0_1.0_1000.0-100000.0",
    "output-16.0_2_1.0_1.0_1000.0-200000.0",
    "output-16.0_2_1.0_1.0_1000.0-300000.0"
]
#
# top_dir = "./plastic-soft/"
# folders = [
#     "output-8.0_2_1.0_1.0_100.0-100000.0",
#     "output-8.0_2_1.0_1.0_100.0-200000.0",
#     "output-8.0_2_1.0_1.0_100.0-300000.0"
# ]
# top_dir = "./plastic-damage/"
# folders = [
#     "output-8.0_3_1.0_100.0-100000.0",
#     "output-8.0_3_1.0_100.0-200000.0",
#     "output-8.0_3_1.0_100.0-300000.0"
# ]
# names = folders
# folders = [
#     "output-4.0_4_1.0_100.0-100000.0",
#     "output-4.0_4_1.0_100.0-200000.0",
#     "output-4.0_4_1.0_100.0-300000.0"
#     # "output-SE_4.0_2_0.5_1.0_10000.0-50000.0" ,
#     # "output-SE_4.0_2_0.5_1.0_10000.0-100000.0",
#     # "output-SE_4.0_2_0.5_1.0_10000.0-150000.0",
#     # "output-SE_4.0_2_0.5_1.0_10000.0-200000.0",
#     # "output-SE_4.0_2_0.5_1.0_10000.0-250000.0",
#     # "output-SE_4.0_2_0.5_1.0_10000.0-300000.0"
# ]
names = [
    "Load: 100kPa",
    "Load: 200kPa",
    "Load: 300kPa"
]
print(folders)

prop_cycle = plt.rcParams['axes.prop_cycle']
colours = prop_cycle.by_key()['color']

load_zeroing = False
#load_zeroing = False
load_clipping = False

def get_load(filename):
    mpm = pd.read_csv(top_dir+filename)
    if load_clipping:
        mpm = mpm[mpm["disp"] >= 0.01e-3]
    if len(mpm["load"]) > 0:
        if load_zeroing:
            mpm["load"] = mpm["load"] - mpm["load"].values[0]
    return mpm

for i in folders:
    print("loading folder: ",i)
    mpm = get_load("./{}/disp.csv".format(i))
    if len(mpm["load"]) > 0:
        #if load_zeroing:
        #    mpm["load"] = mpm["load"] - mpm["load"].values[0]
        # l=plt.plot(1e3*mpm["disp"].values,(1e-3/0.06)*mpm["load"].values,label=i,marker=".")
        maxload = (1e-3/0.06)*mpm["load"].max()
# plt.xlabel("Displacement (mm)")
# plt.ylabel("Shear stress (kPa)")
# plt.legend(names)

fig = plt.figure(figsize=(width,height),dpi=200)
for i in folders:
    print("loading folder: ",i)
    mpm = get_load("./{}/disp.csv".format(i))
    if len(mpm["load"]) > 0:
        #if load_zeroing:
        #    mpm["load"] = mpm["load"] - mpm["load"].values[0]
        l=plt.plot(1e3*mpm["disp"].values,(1e-3/0.06)*mpm["load"].values,label=i,marker=".")
        # plt.plot(1e3*mpm["disp"].values,(1e-3/0.06)*mpm["l-left"].values,label=i,marker=".")
        # plt.plot(1e3*mpm["disp"].values,(1e-3/0.06)*mpm["l-right"].values,label=i,marker=".")
        maxload = 200
        maxp=mpm["plastic"].max()
        maxd=mpm["damage"].max()
        maxp=0.1e0
        maxd=1e3
plt.xlabel("Displacement (mm)")
plt.ylabel("Shear stress (kPa)")
plt.legend(names)
plt.tight_layout()
# plt.savefig("load-disp.pgf")
plt.savefig("load-disp.pdf")

surcharge = []
peak = []
residual = []
fig = plt.figure(figsize=(width,height),dpi=200)
for f in folders:
    refine,load = extract_vals(f)
    mpm = get_load("./{}/disp.csv".format(f))
    # mpm["load"] = mpm["l-left"]
    if len(mpm["load"]) > 0:
        #if load_zeroing:
        #    mpm["load"] = mpm["load"] - mpm["load"].values[0]
        width = 0.06
        p = mpm["load"].max()/width
        r = mpm["load"].values[-1]/width
        #residual_window = 0.25
        #residual_back = round(len(mpm["load"].values) * (1 - residual_window))
        #r = mpm["load"].values[residual_back:].mean()/width
        surcharge.append(load)
        peak.append(p)
        residual.append(r)
        # plt.scatter(load,r)
        # plt.scatter(load,p)


def plot_text_on_line(xpos,angle,c,offset_distance,text):
    ax = plt.gca()
    offsets = ax.transData.inverted().transform(ax.transAxes.transform((xpos,0)))
    xpos = offsets[0]
    m = np.tan(angle * np.pi/180)
    offset_dist_screen = offset_distance
    angle_o = angle + 90
    delta = ax.transData.inverted().transform(ax.transAxes.transform((offset_dist_screen * np.cos(angle_o * np.pi/180), offset_dist_screen * np.sin(angle_o * np.pi/180))))
    plt.text(xpos + delta[0], c + (xpos*m) + delta[1],
             text,
             rotation=angle,
             rotation_mode='anchor',
             transform_rotates_text=True)

if len(peak) > 0:
    peak = [x for y, x in sorted(zip(surcharge, peak))]
    residual = [x for y, x in sorted(zip(surcharge, residual))]
    surcharge = sorted(surcharge)

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colour=colors[0]
    m,b = np.polyfit(surcharge, peak, 1)
    plt.xlim([0,500e3])
    plt.ylim([0,500e3])
    #unique_id = "D_res = "+unique_id.split("_")[-1]
    plt.scatter(surcharge,peak,color=colour,label="Peak point")
    #p = plt.plot(surcharge,peak,color=colour)
    #plt.axline((0,b),slope=m,c=colour,ls="--",label="{:.2f} deg, {:.2f} kPa".format(np.arctan(m)*180/np.pi,b*1e-3))
    plt.axline((0,b),slope=m,c=colour,ls="--",label="Peak envelope".format(np.arctan(m)*180/np.pi,b*1e-3))

    # m,b = np.polyfit(surcharge, residual, 1)
    # plt.scatter(surcharge,residual,label="Residual - {:.2f} deg, {:.2f} kPa".format(np.arctan(m)*180/np.pi,b*1e-3),color=colour,marker="x")
    # #r = plt.plot(surcharge,residual,color=colour,ls="--")
    # plt.axline((0,b),slope=m,c=colour,ls="--")
    ax = plt.gca()


    plot_text_on_line(0.3,30,0,0.03,"$\phi = \SI{30}{\degree}$ - c = 0 kPa")
    plot_text_on_line(0.10,42,131e3,0.03,"$\phi = \SI{42}{\degree}$ - c = 131 kPa")
    plt.axline((0,0),slope=np.tan(30 * np.pi/180),ls="-")
    plt.axline((0,131e3),slope=np.tan(42 * np.pi/180),ls="-")
    ticformat = ticker.FuncFormatter(lambda x,pos: "{0:g}".format(x*1e-3))
    plt.gca().xaxis.set_major_formatter(ticformat)
    plt.gca().yaxis.set_major_formatter(ticformat)
    #arror = {"arrowstyle":"simple"}
    #plt.annotate("{:.2f} deg, {:.2f} kPa".format(42,131),(155e3,271e3),(0.2,0.80),textcoords="figure fraction",arrowprops=arrow,fontsize=8)
    #plt.annotate("{:.2f} deg, {:.2f} kPa".format(42,131),(155e3,271e3),(0.2,0.80),textcoords="figure fraction",arrowprops=arrow,fontsize=8)
    plt.xlabel("Normal load (kPa)")
    plt.ylabel("Shear stress (kPa)")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("frictional.pdf")
    # plt.savefig("frictional.pgf")
plt.show()
