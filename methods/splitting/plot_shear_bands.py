import matplotlib.pyplot as plt
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

ratio = 1.86 # 1.618
width = 5.9006*1
height = width / ratio
scale = 1
chalk_dir = "./data/"
output_regex = re.compile("output-.*")
output_list = list(filter(output_regex.match,os.listdir(chalk_dir)))
# output_list.sort(key=lambda x: int(x.split("-")[-1]))
displacements = []
mps = []
for output_name in output_list:
    folder_name = output_name
    data = mpmplotter.load.load_folder("./data/{}/".format(folder_name))
    df = mpmplotter.load.load_data(data,0)
    # uid = df[(df["coord_x"]==df["coord_x"].max()) & (df["coord_y"]==df["coord_y"].max())]["uid"].values[0]
    # df = mpmplotter.load.load_data(data,-1)
    # print(output_name)
    # #max_x = (df["coord_x"]+df["lx"]).max()
    # max_x = df[df["uid"]==uid]["coord_x"].values[0]
    # displacements.append(max_x)
    # mps.append(int(output_name.split("-")[-1]))
    # print("Max pos {}".format(max_x))
    fig = plt.figure(figsize=(scale*width,scale*height),dpi=200)
    mpmplotter.plot.plot_outline(data,-1)
    plt.xlim([0,20])
    plt.ylim([0,9])
    plt.savefig("outframes/frame_{}.pdf".format(folder_name),dpi=1000)
plt.close("all")

# plt.figure()
# plt.plot(mps,displacements)
# plt.show()

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
