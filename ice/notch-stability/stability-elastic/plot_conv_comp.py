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



top_dir = "./data/"
output_regex = re.compile("output-*")
output_list = list(filter(output_regex.match,os.listdir(top_dir)))
output_list.sort()
fig = plt.figure()


for i,out in enumerate(output_list):
    print("{}: {}".format(i,out))

lslist = ["-","--","-.",":","-"]
for ls,out in zip(lslist,output_list):
    output_dir = "{}./{}/".format(top_dir,out)
    df = pd.read_csv(output_dir+"conv.csv")
    # df = df[df["step"]==1]
    # x = out.split("-")[-1]
    # refine = float(x)
    # mps = int(y)
    # h = 1 / float((refine)**1)
    h=1
    # iters = df["iter"].values
    # oobf = df["oobf"].values
    # plt.plot(iters,oobf,label=out)
    c = None
    for name,group in df.groupby("step"):
        iters = group["iter"].values * h 
        oobf = group["oobf"].values
        if c == None:
            l = plt.plot(iters,oobf,label=out,ls=ls)
            c = l[0].get_color()
        else:
            plt.plot(iters,oobf,c=c,ls=ls)

plt.xlabel("Iterations")
plt.ylabel("Convergence criteria")
plt.yscale("log")
plt.legend()
plt.show()
