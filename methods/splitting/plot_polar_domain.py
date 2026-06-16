import matplotlib.pyplot as plt
import mpmplotter
import mpmplotter.load
import mpmplotter.plot
import matplotlib.ticker as plticker
import os,re

plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
plt.rcParams['figure.constrained_layout.use'] = True

ratio = 1.86 # 1.618
width = 5.9006*1
height = width / ratio
scale = 1
chalk_dir = "./data/"
output_regex = re.compile("output-*")
output_list = list(filter(output_regex.match,os.listdir(chalk_dir)))
# output_list.sort(key=lambda x: int(x.split("-")[-1]))
displacements = []
mps = []
for output_name in output_list:
    folder_name = output_name
    data = mpmplotter.load.load_folder("./data/{}/".format(folder_name))
    # df = mpmplotter.load.load_data(data,0)
    for i in range(len(data["frames"])):
    # i = -1
        fig = plt.figure(figsize=(scale*width,scale*height),dpi=200)
        h=data["settings"]["RESOLUTION"]
        ax = plt.gca()
        mpmplotter.plot.plot_polar_outline(data,i)
        # loc = plticker.MultipleLocator(base=h)
        # ax.xaxis.set_major_locator(loc)
        # locy = plticker.MultipleLocator(base=h)
        # ax.yaxis.set_major_locator(locy)
        # ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)
        plt.xlim([0,20])
        plt.ylim([0,9])
        plt.savefig("outframes/frame_{}_{}.png".format(folder_name,i),dpi=1000)
        plt.close("all")
    plt.show()
