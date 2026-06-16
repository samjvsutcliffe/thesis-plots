import mpmplotter
import mpmplotter.load
import matplotlib as mpl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib import cm
import re
import os
import json
import numpy as np
import pandas as pd
import json
import sys
from vtk import vtkUnstructuredGridReader
from vtk.util import numpy_support as VN
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib import cm
from multiprocessing import Pool

plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)

mpl.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
        'figure.constrained_layout.use':True
    }
)
def plot_interaction(dir_name):
    topdir = "./data/{}/".format(dir_name)
    frame = 0
    inter_regex = re.compile("interaction_\d+.csv")
    inter_list = list(filter(inter_regex.match,os.listdir(topdir)))
    data = mpmplotter.load.load_folder(topdir)
    df = mpmplotter.load.load_data(data,-1,"damage")
    i = (df["coord_x"]-4.8).abs().argmin()
    uid = int(df["uid"][i])
    fig = plt.figure(figsize=(scale*width,scale*height),dpi=200)
    fig,ax = plt.subplots()
    ax_inter = ax.twinx()
    ax.plot(df["coord_x"].values,df["colour"].values)
    inter_list.sort(key=lambda x: int(x.split(".")[0].split("_")[-1]))
    # inter_list = ["interaction_{}.csv".format(uid)]
    for i in inter_list[1::3*2]:
        interaction_data = pd.read_csv("./data/{}/{}".format(dir_name,i))
        print(interaction_data)
        plt.plot(interaction_data["x"].values,interaction_data["w"].values,ls="-",c="black")
    # plt.title(topdir)
    ax.set_xlabel("Location (m)")
    ax.set_ylabel("Damage (m)")
    # ax_inter.set_ylabel("Weight")
    ax_inter.set_ylabel("Interaction weight")
    ax_inter.set_ylim([0,0.3])
    plt.savefig("./outframes/inter_{}.pdf".format(dir_name))
    # return interaction_data

ratio = 1.86 # 1.618
width = 5.9006*0.5
height = width / ratio
scale = 1

folder_list = os.listdir("./data/")
print(folder_list)
for o in folder_list:
    df = plot_interaction(o)
plt.show()
