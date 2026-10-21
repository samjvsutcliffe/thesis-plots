
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


top_dir = "./data/" # "/mnt/c/Temp/mici/"
flist = os.listdir(top_dir)
# flist = ["output-erode_NIL_400.0","output-erode_NIL_600.0","output-erode_NIL_800.0"]

for fname in flist:
    folder_name = "{}/{}".format(top_dir,fname)
    print(fname)
    data = mpmplotter.load.load_folder("{}/".format(folder_name))
    offset = 2
    dpi = 100
    h = data["settings"]["RESOLUTION"]
    d_width = data["settings"]["DOMAIN-SIZE"][0]
    d_height = data["settings"]["DOMAIN-SIZE"][1] - (offset * h)
    d_width_0 = d_width
    h_glacier = 800
    d_height = h_glacier +100
    d_width_0 = d_width
    d_left = 0000
    d_right = h_glacier*6 + 100#d_width
    d_width = d_right-d_left
    ratio = d_height / d_width
    # width = 10
    width = 2*5.90666
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
    # for i in range(len(data["frames"])):#[-1]:
    nameiter = 0
    for i in [10,15,63]:#[-1]:
        plt.clf()
        p = mpmplotter.plot.plot(data,i,colour_name=colour_name,extract_vals=["disp_x","disp_y"],df_transform=transform)
        water_height = data["settings"]["OCEAN-HEIGHT"] - (h * offset)
        patch = Rectangle(xy=(0,0),
                          width=d_width_0,
                          height=water_height,
                          fill="light blue",
                          hatch="x",
                          zorder=-5)
        ax = plt.gca()
        ax.add_patch(patch)
        plt.xlim([d_left,d_right])
        plt.ylim([0,d_height])
        # cmap = cm.get_cmap(None, 10)
        # p.set_cmap(cmap)
        p.set_clim([0,1])
        # plt.colorbar(p)
        plt.xlabel("(m)")
        plt.ylabel("(m)")
        day_in_second = 60*60*24
        plt.title("t = {:.2f} days".format(data["timesteps"]["time"].values[i]/day_in_second))
        plt.savefig("outframes/frame_{}_{}.png".format(fname,nameiter),bbox_inches='tight')
        plt.savefig("outframes/frame_{}_{}.pdf".format(fname,nameiter),bbox_inches='tight')
        nameiter = nameiter +1

# def wrapper(x):
#         get_plot(x[0],x[1])
# if __name__ == '__main__':
#     with Pool(16) as p:
#         p.map(wrapper, enumerate(files_csvs))
plt.close("all")
plt.show()
