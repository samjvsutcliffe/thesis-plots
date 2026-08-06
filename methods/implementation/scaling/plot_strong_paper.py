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
#plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
plt.rcParams['figure.constrained_layout.use'] = True

width = 3.487
height = width / 1.618
scale = 1
fig = plt.figure(figsize=(scale*width,1.3*scale*height),dpi=200)

output_regex = re.compile("data_.*STRONG.*\.csv")                                 
output_list = list(filter(output_regex.match,os.listdir("./")))
output_list.sort()
#if len(output_list) == 1:
#    data_file = output_list[0]
#else:
#    for i,out in enumerate(output_list):                                    
#        print("{}: {}".format(i,out))                                       
#    data_file = output_list[int(input())]

output_list = ["data_STRONG.csv"]
solvername = {"DR":"Dynamic relaxation","IMPLICIT":"Newton-Raphson","CPPDR":"C++ Dynamic relaxation"}
for data_file in output_list:
    df = pd.read_csv(data_file)
    df = df[df["refine"]==16.0]
    numeric_cols = ["threads", "refine","throughput","mp-throughput"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
    for solver,row in df.groupby("solver"):
        name =  "{}".format(solvername[solver])
        print(name)
        means = row.groupby("threads")["throughput"].mean()
        vs_0 = means.values[0]
        vs=means.values/vs_0
        ls = plt.plot(means.index.values,vs,label=name)
        c = ls[0].get_color()
        threads = row["threads"].values
        mp_throughputs = row["throughput"].values
        print(threads)
        print(mp_throughputs)
        plt.scatter(threads,mp_throughputs/vs_0,c=c)
ax = plt.gca()
ax.axline((0,0),slope=1,label="Ideal",ls="--",c="black")
plt.legend(loc="upper left")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Thread count")
plt.ylabel("Speedup")
plt.savefig("strong.pgf",dpi=1000)#,bbox_inches="tight",pad_inches=0)
plt.savefig("strong.pdf",dpi=1000)#,bbox_inches="tight",pad_inches=0)

plt.show()

#means = df.groupby("threads")["mp-throughput"].mean()

