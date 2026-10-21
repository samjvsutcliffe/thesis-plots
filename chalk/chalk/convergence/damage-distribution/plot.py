import matplotlib as mpl
# mpl.use("pgf")
import os
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import mpmplotter
import mpmplotter.load
import mpmplotter.plot
from matplotlib import cm

plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
plt.rcParams['figure.constrained_layout.use'] = True


top_dir = "../data/"
flist = os.listdir(top_dir)

for fname in flist:
    folder_name = "{}/{}".format(top_dir,fname)
    print(fname)
    data = mpmplotter.load.load_folder("./{}/".format(folder_name))
    offset = 2
    dpi = 100
    h = data["settings"]["RESOLUTION"]
    d_width = data["settings"]["DOMAIN-SIZE"][0]
    d_height = data["settings"]["DOMAIN-SIZE"][1]
    ratio = d_height / d_width
    width = 10
    height = width * ratio
    scale = 10
    def transform(df):
        # coord_0 = df["coord_x"] - df["disp_x"]
        # df["coord_x"] = coord_0 +  df["disp_x"] * 0
        # coord_0 = df["coord_y"] - df["disp_y"]
        # df["coord_y"] = coord_0 +  df["disp_y"] * 0
        # print("max {} min {}".format(df["disp_x"].max(),df["disp_x"].min()))
        df["coord_y"] -= (offset * h)
        return df
    fig = plt.figure(figsize=(width,height),dpi=dpi)
    colour_name = "damage"
    # colour_name = "disp_x"
    for i in [-1]:#range(len(data["frames"])):
        p = mpmplotter.plot.plot(data,i,colour_name=colour_name,df_transform=transform)
        ax = plt.gca()
        plt.xlim([0,d_width])
        plt.ylim([0,d_height])
        # cmap = cm.get_cmap(None, 1)
        # p.set_cmap(cmap)
        plt.colorbar(p)
        plt.xlabel("(m)")
        plt.ylabel("(m)")
        plt.savefig("outframes/frame_{}.png".format(fname,i))
        plt.savefig("outframes/frame_{}.pdf".format(fname,i))
        plt.close("all")
plt.show()
