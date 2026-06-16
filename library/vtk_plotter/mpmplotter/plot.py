import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle,Ellipse
from matplotlib.collections import PatchCollection
from matplotlib import cm
import matplotlib.pyplot as plt
import mpmplotter.load
from numpy.linalg import eig,eigh
import numpy as np

def plot(folder_data,frame_number,colour_name="sig_xx"):
    fig = plt.gcf()
    ax = fig.add_subplot(111,aspect="equal")
    # loc = plticker.MultipleLocator(base=0.25)
    # ax.xaxis.set_major_locator(loc)
    # locy = plticker.MultipleLocator(base=0.25)
    # ax.yaxis.set_major_locator(locy)
    # ax.set_axisbelow(True)
    df = mpmplotter.load.get_data_all(folder_data["folder"],folder_data["frames"][frame_number],colour_name=colour_name)
    patch_list=[]
    for a_x, a_y,lx,ly,damage in zip(df["coord_x"],
                                     df["coord_y"],
                                     df["lx"],
                                     df["ly"],
                                     df["colour"]):
        patch = Rectangle(
            xy=(a_x-lx/2, a_y-ly/2) ,width=lx, height=ly,
            fill=damage)
        patch_list.append(patch)
    p = PatchCollection(patch_list, cmap=cm.jet, alpha=1)
    p.set_array(df["colour"])
    # p.set_clim([-1e6,1e6])
    ax.add_collection(p)
    # fig.colorbar(p,location="bottom",label="sig_{xx}")
    xlim = [0,folder_data["settings"]["DOMAIN-SIZE"][0]]
    ylim = [0,folder_data["settings"]["DOMAIN-SIZE"][1]]
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    return p


def plot_outline(folder_data,frame_number):
    fig = plt.gcf()
    ax = fig.add_subplot(111,aspect="equal")
    df = mpmplotter.load.get_data_all(folder_data["folder"],folder_data["frames"][frame_number])
    patch_list=[]
    for a_x, a_y,lx,ly,damage in zip(df["coord_x"],
                                     df["coord_y"],
                                     df["lx"],
                                     df["ly"],
                                     df["colour"]):
        patch = Rectangle(
            xy=(a_x-lx/2, a_y-ly/2) ,width=lx, height=ly,
            fill=None,edgecolor="black"
        )
        patch_list.append(patch)
    p = PatchCollection(patch_list, cmap=cm.jet, alpha=1,facecolor="none",edgecolor="black")
    # p.set_array(df["colour"])
    # p.set_clim([-1e6,1e6])
    ax.add_collection(p)
    # fig.colorbar(p,location="bottom",label="sig_{xx}")
    xlim = [0,folder_data["settings"]["DOMAIN-SIZE"][0]]
    ylim = [0,folder_data["settings"]["DOMAIN-SIZE"][1]]
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    return p


def plot_polar_outline(folder_data,frame_number):
    fig = plt.gcf()
    ax = fig.add_subplot(111,aspect="equal")
    df = mpmplotter.load.get_data_all(folder_data["folder"],folder_data["frames"][frame_number])
    patch_list=[]
    for a_x, a_y,lx,ly,lxx,lyy,lxy,lyx,damage in zip(df["coord_x"],
                                         df["coord_y"],
                                         df["lx"],
                                         df["ly"],
                                         df["lxx"],
                                         df["lyy"],
                                         df["lxy"],
                                         df["lyx"],
                                         df["colour"]):
        tl = np.array([[lxx,lxy],
                       [lyx,lyy]])
        (egval,egvec) = eig(tl)
        # print(egvec)
        wlx = egval[0]
        wly = egval[1]
        angle = np.arccos(egvec[0,0]) * 180/3.14
        # print(angle)
        patch = Ellipse(
            xy=(a_x, a_y) ,width=wlx, height=wly,angle=angle,
            fill=None,edgecolor="black"
        )
        patch_list.append(patch)
    p = PatchCollection(patch_list, cmap=cm.jet, alpha=1,facecolor="none",edgecolor="black")
    # p.set_array(df["colour"])
    # p.set_clim([-1e6,1e6])
    ax.add_collection(p)
    # fig.colorbar(p,location="bottom",label="sig_{xx}")
    xlim = [0,folder_data["settings"]["DOMAIN-SIZE"][0]]
    ylim = [0,folder_data["settings"]["DOMAIN-SIZE"][1]]
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    return p
