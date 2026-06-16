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

folder_name = "output-polar"
data = mpmplotter.load.load_folder("./data/{}/".format(folder_name))
ratio = 1.86 # 1.618
width = 5.9006*1
height = width / ratio
scale = 1
fig = plt.figure(figsize=(scale*width,scale*height),dpi=200)
mpmplotter.plot.plot_outline(data,-1)
plt.xlim([0,19])
plt.ylim([0,6])
plt.savefig("outframes/frame_{}.pgf".format(folder_name),dpi=1000)
plt.savefig("outframes/frame_{}.pdf".format(folder_name),dpi=1000)
plt.show()
