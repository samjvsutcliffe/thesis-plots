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

ratio = 1.618
width = 5.9006*1
height = width / ratio
scale = 1
fig = plt.figure(figsize=(scale*width,scale*height),dpi=200)


top_dir = "./data/"
output_regex = re.compile("output-*")
output_list = list(filter(output_regex.match,os.listdir(top_dir)))
output_list.sort()

# for i,out in enumerate(output_list):
#     print("{}: {}".format(i,out))

# for out in output_list:
#     output_dir = "{}./{}/".format(top_dir,out)
#     df = pd.read_csv(output_dir+"conv.csv")
#     iters = df["iters"].values
#     oobf = df["residual"].values
#     plt.plot(iters,oobf,label=out)

print(output_list)
# names = ["K constant","K updated","P elastic","P elastoplastic"]
#names = output_list
lss = ["-","-.",":","--","-","-","-","-"]
names = ["Non-aggregated","Aggregated"]
# lss = ["-","-","-","-"]
for n,out,ls in zip(names,output_list,lss):
    output_dir = "{}./{}/".format(top_dir,out)
    df = pd.read_csv(output_dir+"conv.csv")
    c = None
    for name,group in df.groupby("step"):
        iters = group["iter"].values
        oobf = group["oobf"].values
        if c == None:
            l = plt.plot(iters,oobf,ls=ls,label=n)
            c = l[0].get_color()
        else:
            plt.plot(iters,oobf,ls=ls,c=c)
    print(out)
    print(df["iter"].values[-1])

# plt.axhline(thresh_scale,c="green",ls="--")
# ax.set_ylim(bottom=0,top=thresh_scale_damage*2)
plt.xlabel("Iterations")
plt.ylabel("Convergence criteria")
plt.yscale("log")
#plt.legend(["Aggregated","Non-aggregated"])
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig("conv_comp.pdf")
plt.show()
