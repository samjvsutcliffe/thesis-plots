import matplotlib as mpl
#mpl.use('pdf')
mpl.use("pgf")
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


def get_data(filename):
    global data_name
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
    dx = GetScalar("disp_x")
    damage = GetScalar("damage")
    damage_ybar = GetScalar("damage-ybar")
    #damage = GetScalar("plastic_strain")
    #damage = GetScalar("damage")
    return pd.DataFrame({"coord_x":xy[:,0],"dx":dx,"lx":lx,"ly":ly,"damage":damage,"damage-ybar":damage_ybar})

def get_data_all(folder,frame_number):
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
width = 3.487
height = width / 1.618

def get_damage(output_dir,i):
    files = os.listdir(output_dir)
    finalcsv = re.compile("sim(_0+)?_\d*\.vtk")
    files_csvs = list(filter(finalcsv.match,files))
    framenumber_regex = re.compile("\d+")
    files_csvs = list(map(lambda x: framenumber_regex.findall(x)[-1],files_csvs))
    files_csvs.sort(key=int)
    fname = files_csvs[i]
    df = get_data_all(output_dir,fname)
    x = []
    d = []
    dy = []
    for a_x, dx,lx,ly,damage,damage_ybar in zip(df["coord_x"],
                                     df["dx"],
                                     df["lx"],
                                     df["ly"],
                                     df["damage"],
                                     df["damage-ybar"]):
        x.append(a_x-dx)
        d.append(damage)
        dy.append(damage_ybar)
    return (x,d,dy)
plt.close("all")
def plot_2d(i):
    plt.clf()
    plt.xlim(0,10)
    plt.ylim(0,1.1)
    (x,d,dy) = get_damage("./data/output-1/",i)
    plt.plot(x,d,marker="o")
    (x,d,dy) = get_damage("./data/output-2/",i)
    plt.plot(x,d,marker="o")
    (x,d,dy) = get_damage("./data/output-4/",i)
    plt.plot(x,d,marker="o")
    plt.xlabel("Reference position (m)")
    plt.ylabel("Damage")
    plt.savefig("paper_2d.pgf")
    plt.show()

def plot_3d(ivals):
    width = 1*5.90666
    height = width / 1.4
    fig =plt.figure(figsize=(width,height))
    plt.clf()
    plt.gcf().add_subplot(projection='3d',computed_zorder=True)
    ax = plt.gca()
    ax.view_init(azim=-130,elev=20,vertical_axis="y")
    # plt.xlim(0,10)
    # plt.ylim(0,1.1)
    x_v = []
    d_v = []
    z_v = []
    for i in reversed(ivals):
        (x,d,dy) = get_damage("./data/output-1/",i)
        plt.plot(x,d,zs=i,marker="o",c="black")
        # (x,d,dy) = get_damage("./data/output-2/",i)
        # plt.plot(x,d,zs=i,marker="o",c="blue")
        # (x,d,dy) = get_damage("./data/output-4/",i)
        # plt.plot(x,d,zs=i,marker="o",c="orange")

    plt.xlabel("Reference position (m)")
    plt.ylabel("Damage")
    ax.set_zlabel("Load step")
    plt.savefig("paper_3d.pgf")
    plt.show()


def plot_3d_surface(ivals):
    plt.clf()
    plt.gcf().add_subplot(projection='3d',computed_zorder=True)
    ax = plt.gca()
    ax.view_init(azim=-130,elev=10,vertical_axis="y")
    # plt.xlim(0,10)
    # plt.ylim(0,1.1)
    x_v = []
    d_v = []
    z_v = []
    odir = "./data/output-1/"
    (x,d,dy) = get_damage(odir,0)
    ivals_array = np.array(ivals)
    print(x)
    print(ivals_array)
    X,Y = np.meshgrid(x,ivals_array)
    Z = np.zeros((len(ivals_array),len(x)))
    for iv,i in enumerate(ivals):
        (x,d,dy) = get_damage("./data/output-4/",i)
        for j,dv in enumerate(d):
            Z[iv,j] = dv
        #plt.plot(x,d,zs=i,marker="o",c="black")
        # (x,d,dy) = get_damage("./data/output-2/",i)
        # plt.plot(x,d,zs=i,marker="o",c="blue")
        # (x,d,dy) = get_damage("./data/output-4/",i)
        # plt.plot(x,d,zs=i,marker="o",c="orange")
    print("{} {} {}".format(X.shape,Y.shape,Z.shape))
    ax.plot_wireframe(X,Z,Y)
    plt.xlabel("Reference position (m)")
    plt.ylabel("Damage")
    ax.set_zlabel("Load step")
    plt.show()

width = 0.49*5.90666
height = width / 1.4
fig =plt.figure(figsize=(width,height))
# get_plot(10)
# plot_2d(49)
# plot_3d([0, 9, 19, 29, 39, 49])
plot_3d([0, 9, 19, 29, 39, 49])
# plot_3d_surface([x for x in range(0,49,2)])
