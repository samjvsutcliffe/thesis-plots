import matplotlib as mpl
#mpl.use('pdf')
mpl.use("pgf")
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import re

from scipy import integrate
PDF_OUTPUT = False


#plt.rc('font', family='serif', serif='Times')
## plt.rc('text', usetex=True)
#plt.rc('xtick', labelsize=8)
#plt.rc('ytick', labelsize=8)
#plt.rc('axes', labelsize=8)
plt.style.use("seaborn-paper")
plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)

mpl.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
        "pgf.preamble": "\n".join([
        r"\usepackage{siunitx}",
        ])
    }
)
width = 0.48*5.90666
height = width / 1.3


B = 1
C = 1e6

plt.figure(figsize=(width,height))

top_dir = "./data/"
regex = re.compile(r'^output.*')
folders = list(filter(regex.search,os.listdir(top_dir)))

output_regex = re.compile(".*\.csv")
output_list = list(filter(output_regex.match,os.listdir(top_dir)))
output_list.sort()
plt.axhline(0.5,ls="--",color="black",label="mu = 0.5")
load_scale = 1.0
for odir in folders:
    data = pd.read_csv("{}/{}/disp.csv".format(top_dir,odir))
    # values = r[:-4].split("_")
    plt.plot(data["disp"].values*1e3,load_scale*data["load"].values,ls="-")#,label="refine: {}".format(r[:-3].split("_")[-1]))
plt.legend(["Penalty scale $$\\num{1e0}$$",
"Penalty scale $$\\num{1e-1}$$",
"Penalty scale $$\\num{1e-2}$$"
            ])
plt.xlabel("Displacement (mm)")
plt.ylabel("Normalised frictional force")
#plt.xlim(0,2)
plt.ylim(bottom=0)
plt.tight_layout()
plt.savefig("paper.pgf")
plt.show()
