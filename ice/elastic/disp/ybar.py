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


top_dir = "./data/"
flist = os.listdir(top_dir)

for fname in flist:
    folder_name = "{}/{}".format(top_dir,fname)
    print(fname)
    data = mpmplotter.load.load_folder("./{}/".format(folder_name))
    offset = 0
    dpi = 100
    h = data["settings"]["RESOLUTION"]
    d_width = data["settings"]["DOMAIN-SIZE"][0]
    d_height = data["settings"]["DOMAIN-SIZE"][1] - (offset * h)
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
        return df
    fig = plt.figure(figsize=(width,height),dpi=dpi)
    colour_name = "damage-ybar"
    for i in [-1]:#range(len(data["frames"])):
        p = mpmplotter.plot.plot(data,i,colour_name=colour_name,extract_vals=["disp_x","disp_y"],df_transform=transform)
        water_height = data["settings"]["OCEAN-HEIGHT"] - (h * offset)
        patch = Rectangle(xy=(0,0),
                          width=d_width,
                          height=water_height,
                          fill="light blue",
                          hatch="x",
                          zorder=-5)
        ax = plt.gca()
        ax.add_patch(patch)
        plt.xlim([0,d_width])
        plt.ylim([0,d_height])
        cmap = cm.get_cmap(None, 10)
        p.set_cmap(cmap)
        # p.set_clim([-0.3,0.8])
        plt.colorbar(p)
        plt.xlabel("(m)")
        plt.ylabel("(m)")
        plt.savefig("outframes/frame_{}.png".format(fname,i))
plt.show()
