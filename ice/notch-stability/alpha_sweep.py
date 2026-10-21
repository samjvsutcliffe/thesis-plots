
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


top_dir = "/mnt/c/Temp/notch-stability-alpha/"
flist = os.listdir(top_dir)

alphas = ["0.0","0.25","0.5","0.75","1.0"]
notches = ["0.0","0.25","0.5","0.75","1.0"]


def replot():
    alpha = alphas[alpha_index]
    notch = notches[notch_index]
    plt.cla()
    folder_name = "{}/output-400.0-0.9-{}-{}/".format(top_dir,alpha,notch)
    data = mpmplotter.load.load_folder("{}/".format(folder_name))
    offset = 2
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
        df["coord_y"] -= (offset * h)
        return df
    fig = plt.figure(figsize=(width,height),dpi=dpi)
    colour_name = "damage"
    # colour_name = "disp_x"
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


alpha_index = 0
notch_index = 0
def on_press(event):
    global current_frame,data_name
    # print('press', event.key)
    sys.stdout.flush()
    # print(event.key)
    # if event.key in data_map:
    #     data_name = data_map[event.key]
    #     replot()

    if event.key == 'right':
        alpha_index = min(alpha_index + 1,len(alphas))
        replot()
    if event.key == 'left':
        alpha_index = max(alpha_index - 1,0)
        replot()
    if event.key == 'up':
        notch_index = min(notch_index + 1,len(alphas))
        replot()
    if event.key == 'down':
        notch_index = max(notch_index - 1,0)
        replot()


# print("Plotting {}, {}",current_frame,files_csvs[current_frame])

fig = plt.figure()#plt.figure(figsize=(16,9),dpi=200)
fig.canvas.mpl_connect('key_press_event', on_press)
replot()
plt.show()
