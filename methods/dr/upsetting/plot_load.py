import matplotlib.pyplot as plt
import pandas as pd
import mpmplotter
import mpmplotter.load
import mpmplotter.plot
import os,re

plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
plt.rcParams['figure.constrained_layout.use'] = True

ratio = 1.16 # 1.618
width = 5.9006*0.5
height = width / ratio
scale = 1
chalk_dir = "./data/"
output_regex = re.compile("output-\d+")
output_list = list(filter(output_regex.match,os.listdir(chalk_dir)))
output_list.sort(key=lambda x: int(x.split("-")[-1]))
displacements = []
mps = []
output_regex = re.compile("output-.*")
output_list = list(filter(output_regex.match,os.listdir(chalk_dir)))
# output_list.sort(key=lambda x: int(x.split("-")[-1]))
displacements = []
mps = []
force_scale = 1e-3
for output_name in output_list:
    data = pd.read_csv("./data/{}/load.csv".format(output_name))
    disp = -data["step"].values
    load = data["load"].values
    plt.plot(disp,force_scale*load,label="MPs - {} split".format(output_name.split("-")[-1]))

plt.xlabel("Displacement (m)")
plt.ylabel("Force (kN)")
# plt.legend()
plt.savefig("outframes/load.pdf".format(),dpi=1000)
plt.show()

# folder_name = "output-split"
# data = mpmplotter.load.load_folder("./data/{}/".format(folder_name))
# df = mpmplotter.load.load_data(data,0)
# print("Max pos {}".format((df["coord_x"]+df["lx"]).max()))


# folder_name = "output-polar"
# data = mpmplotter.load.load_folder("./data/{}/".format(folder_name))
# ratio = 1.86 # 1.618
# width = 5.9006*1
# height = width / ratio
# scale = 1
# fig = plt.figure(figsize=(scale*width,scale*height),dpi=200)
# mpmplotter.plot.plot_outline(data,-1)
# plt.xlim([0,19])
# plt.ylim([0,6])
# plt.savefig("outframes/frame_{}.pgf".format(folder_name),dpi=1000)
# plt.savefig("outframes/frame_{}.pdf".format(folder_name),dpi=1000)
plt.show()
