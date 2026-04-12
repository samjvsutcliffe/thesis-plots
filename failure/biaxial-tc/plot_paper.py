PDF_OUTPUT = True
import matplotlib as mpl
if PDF_OUTPUT:
    mpl.use('pdf')
else:
    mpl.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib import cm
import matplotlib.ticker as plticker
import re
import os
import json
import numpy as np
import pandas as pd
import json
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
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
plt.rcParams['figure.constrained_layout.use'] = True

width = 3.487
height = width / 1.618

# NO_OVERWRITE = False
NO_OVERWRITE = True


reader = None
def get_data(filename):
    global reader
    reader = vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.ReadAllVectorsOn()
    reader.ReadAllScalarsOn()
    reader.Update()

    data = reader.GetOutput()

    vtk_points = data.GetPoints()
    xyz3d = vtk_to_numpy( vtk_points.GetData() )
    xy = xyz3d[:,0:2]
    scalar_names = [reader.GetScalarsNameInFile(i) for i in range(0, reader.GetNumberOfScalarsInFile())]
    scalar_data = data.GetPointData()
    #scalar_names = scalar_data.GetArrayNames()
    def GetScalar(scalar_name):
        return vtk_to_numpy(scalar_data.GetArray(scalar_names.index(scalar_name)))
    lx = GetScalar("size_x") 
    ly = GetScalar("size_y") 
    damage = GetScalar("damage")
    #damage = GetScalar("plastic_strain")
    return pd.DataFrame({"coord_x":xy[:,0], "coord_y":xy[:,1],"lx":lx,"ly":ly,"damage":damage})

def get_data_all(folder,frame_number):
    print(frame_number)
    regex = re.compile(r'sim(_\d+)?_{}.vtk'.format(frame_number))
    files = list(filter(regex.search,os.listdir(folder)))
    subframes = [get_data(folder + "/" + f) for f in files]
    df = pd.concat(subframes)
    return df




import subprocess

plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
width = 0.1*5.90666
height = width / 1

chalk_dir ="./data/"
output_regex = re.compile("output*")
output_list = list(filter(output_regex.match,os.listdir(chalk_dir)))
output_list.sort()

for output_name in output_list:
    output_dir = chalk_dir + "./{}/".format(output_name)
    plt.close("all")
    files = os.listdir(output_dir)
    finalcsv = re.compile("sim(_0+)?_\d*\.vtk")
    files_csvs = list(filter(finalcsv.match,files))
    print(files_csvs)

    framenumber_regex = re.compile("\d+")
    files_csvs = list(map(lambda x: framenumber_regex.findall(x)[-1],files_csvs))
    files_csvs.sort(key=int)
    print("files: {}".format(files_csvs))

    trim = 80e-3
    xlim = [0+trim,0.24-trim]
    ylim = [0,0.18]

    aspect = (xlim[1]-xlim[0])/(ylim[1]-ylim[0])

    def get_plot(i):
        fig = plt.figure(figsize=(width,height/aspect),dpi=200)
        fname = files_csvs[i]
        df = get_data_all(output_dir,fname)
        print("Plot frame {}".format(i),flush=True)
        ax = fig.add_subplot(111,aspect="equal")
        loc = plticker.MultipleLocator(base=0.25)
        ax.xaxis.set_major_locator(loc)
        locy = plticker.MultipleLocator(base=0.25)
        ax.yaxis.set_major_locator(locy)
        ax.set_axisbelow(True)
        patch_list=[]
        for a_x, a_y,lx,ly,damage in zip(df["coord_x"],
                                         df["coord_y"],
                                         df["lx"],
                                         df["ly"],
                                         df["damage"]):
            patch = Rectangle(
                xy=(a_x-lx/2, a_y-ly/2) ,width=lx, height=ly,
                fill=damage)
            patch_list.append(patch)
        #p = PatchCollection(patch_list,fc="none",ec="black")
        p = PatchCollection(patch_list, cmap=cm.jet, alpha=1)
        p.set_array(df["damage"])
        p.set_clim([0,1])
        ax.add_collection(p)
        #fig.colorbar(p,location="bottom",label="sig_{xx}")
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        ax.set_yticklabels([])
        ax.set_xticklabels([])

        for tick in ax.xaxis.get_major_ticks():
            tick.tick1line.set_visible(False)
            tick.tick2line.set_visible(False)
            tick.label1.set_visible(False)
            tick.label2.set_visible(False)
        for tick in ax.yaxis.get_major_ticks():
            tick.tick1line.set_visible(False)
            tick.tick2line.set_visible(False)
            tick.label1.set_visible(False)
            tick.label2.set_visible(False)

        plt.axis('off')
        ax.grid(color='grey',which="both", linestyle='-',lw=0.1)
        #plt.tight_layout()
        plt.savefig("outframes/frame_{}_{:05}.pgf".format(output_name,i),dpi=1000)
        plt.savefig("outframes/frame_{}_{:05}.png".format(output_name,i),dpi=1000)
        plt.clf()
        #plt.show()
    if not os.path.isdir("./outframes/"):
        os.mkdir("./outframes/")

    if len(files_csvs)>0:
        get_plot(len(files_csvs)-1);
