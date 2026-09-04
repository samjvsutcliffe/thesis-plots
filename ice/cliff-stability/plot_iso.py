import matplotlib as mpl
#mpl.use('pdf')
#mpl.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os
import numpy as np
import re
import matplotlib.pyplot as plt
import pandas as pd
import json
import os,re
import numpy as np

plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)

mpl.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
        'figure.constrained_layout.use':True
    }
)
f_width = 0.49*5.90666
f_height = f_width / 1.4
# plt.figure(figsize=(width,height))

#chalk_dir ="./data-cliff-stability_no_stress/"
chalk_dir ="./data-cliff-stability/"
#chalk_dir = "/nobackup/rmvn14/ham-chalk-conv-fbar/"
output_regex = re.compile("data.*json")
output_list = list(filter(output_regex.match,os.listdir(chalk_dir)))
output_list.sort()
print(output_list)

h = 20

plot_cliff = True
for plot_cliff in [True,False]:
    plt.figure(figsize=(f_width,f_height))
    # plt.title("slip")
    x = []
    y = []
    t = []
    data_stable = []
    tau = 1e5
    h = 20
    float_point = ( 918 / 1028)
    for i,out in enumerate(output_list):
        #output_dir = chalk_dir + "./{}/".format(out)
        with open(chalk_dir+out) as f:
            js = json.load(f)
            height = float(js["HEIGHT"])
            floatation = float(js["FLOATATION"])
            time = min(float(js["TIME"])/tau,100)
            stable = js["STABLE"]==True

            #lw = round((height*floatation)/h)*h
            lw=height*floatation*float_point
            #lw=round((lw)/h)*h
            x.append(height)
            if plot_cliff:
                y.append(height - lw)
            else:
                y.append(lw)
            t.append(time)
            data_stable.append(stable)

    x = np.array(x)
    y = np.array(y)
    t = np.array(t)
    data_stable = np.array(data_stable)
    # plt.scatter(x[data_stable==True],y[data_stable==True],c=t[data_stable==True])
    # plt.scatter(x[data_stable==True],y[data_stable==True],c=t[data_stable==True])
    # plt.tricontour(x,y,t)
    cmin = t.min()
    cmax = t.max()
    dst = data_stable==True
    #plt.scatter(x[dst],y[dst],c=t[dst])
    plt.scatter(x[dst],y[dst],c="C0")
    plt.clim(cmin,cmax)
    dsf = data_stable==False
    #plt.scatter(x[dsf],y[dsf],c=t[dsf],marker="x")
    plt.scatter(x[dsf],y[dsf],c="C1",marker="x")
    plt.clim(cmin,cmax)
    plt.xlabel("Height (m)")
    if plot_cliff:
        plt.ylabel("Cliff height (m)")
    else:
        plt.ylabel("Water height (m)")
    plt.scatter([],[],label="Stable", c="C0")
    plt.scatter([],[],marker="x",label="Unstable", c="C1")
    plt.legend()
    # plt.colorbar()
    plt.savefig("paper_cliff_{}.pdf".format(plot_cliff))
plt.show()
