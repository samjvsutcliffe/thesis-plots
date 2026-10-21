import matplotlib as mpl
mpl.use('pdf')
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
f_width = 1*5.90666
f_height = f_width / 1.8


import matplotlib.pyplot as plt
import pandas as pd
import json
import os,re
import numpy as np

#chalk_dir ="./data-cliff-stability_no_stress/"
chalk_dir ="./data/"
#chalk_dir = "/nobackup/rmvn14/ham-chalk-conv-fbar/"
output_regex = re.compile("data.*json")
output_list = list(filter(output_regex.match,os.listdir(chalk_dir)))
output_list.sort()
print(output_list)

h = 20

x = []
y = []
t = []
plot_cliff = False
data_stable = []
tau = 1e4
h = 20
float_point = ( 918 / 1028)

plt.figure(figsize=(f_width,f_height))
for i,out in enumerate(output_list):
    #output_dir = chalk_dir + "./{}/".format(out)
    with open(chalk_dir+out) as f:
        js = json.load(f)
        height = float(js["HEIGHT"])
        notch = float(js["NOTCH"])
        floatation = float(js["FLOATATION"])
        alpha = float(js["ALPHA"])
        time = min(float(js["TIME"])/tau,100)
        stable = js["STABLE"]==True

        #lw = round((height*floatation)/h)*h
        lw=height*floatation*float_point
        #lw=round((lw)/h)*h
        #y.append(height)
        x.append(notch)
        #x.append(height)
        # y.append(notch)
        y.append(alpha)
        #if plot_cliff:
        #    y.append(height - lw)
        #else:
        #    y.append(lw)
        t.append(time)
        data_stable.append(stable)

x = np.array(x)
y = np.array(y)
t = np.array(t)
data_stable = np.array(data_stable)
# plt.scatter(x[data_stable==True],y[data_stable==True],c=t[data_stable==True])
#plt.scatter(x[data_stable==True],y[data_stable==True],c=t[data_stable==True])
#plt.tricontour(x,y,t)
cmin = t.min()
cmax = t.max()
dst = data_stable==True
plt.scatter(x[dst],y[dst],c=t[dst])
plt.clim(cmin,cmax)
dsf = data_stable==False
plt.scatter(x[dsf],y[dsf],c=t[dsf],marker="x")
plt.clim(cmin,cmax)
plt.ylabel("Pressure factor $\\beta$")
plt.xlabel("Notch ratio $r$")
plt.scatter([],[],label="Stable")
plt.scatter([],[],marker="x",label="Unstable")
plt.legend()
# plt.colorbar()
plt.savefig("stability.pdf")
plt.show()
