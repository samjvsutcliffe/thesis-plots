import matplotlib.pyplot as plt
import mpmplotter
import mpmplotter.load
import mpmplotter.plot

plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
plt.rcParams['figure.constrained_layout.use'] = True

folder_name = "output-ms-1"
data = mpmplotter.load.load_folder("./data/{}/".format(folder_name))
offset = 2
ratio = 4.1 #1.86 # 1.618
width = 5.9006*1
height = width / ratio
scale = 1

for i in [-1]:
    fig = plt.figure(figsize=(scale*width,scale*height),dpi=200)
    p = mpmplotter.plot.plot(data,i,colour_name="damage")
    plt.xlim([0,29])
    plt.ylim([2,9])
    p.set_clim([0,1])
    fig.colorbar(p,location="right",label="damage")
    plt.savefig("outframes/frame_{}.pdf".format(i),dpi=1000)
    fig = plt.figure(figsize=(scale*width,scale*height),dpi=200)
    p = mpmplotter.plot.plot_outline(data,i)
    plt.xlim([0,29])
    plt.ylim([2,9])
    plt.savefig("outframes/frame_outline_{}.pdf".format(i),dpi=1000)
plt.show()
