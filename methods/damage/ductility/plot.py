import matplotlib as mpl
#mpl.use('pdf')
#mpl.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os
import numpy as np
import re

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

from scipy import integrate

def extract_vals(f):
    output,refine,load = f.split("-")
    #refine = float(refine)
    return refine,float(load)

from scipy import integrate
def calculate_gf(disp,load):
    i = 0#np.argmax(load)
    print("Max at {}mm".format(disp[i]*1e3))
    return integrate.trapz(load[i:],disp[i:])

top_dir = "./data/"
for top_dir in [
        "data-standard/",
        "data-ll/",
        "data-ll-standard/",
        "data-ekl/",
        # "/home/samsu/quicklisp/local-projects/cl-mpm/data-ll-standard/",
        # "/home/samsu/quicklisp/local-projects/cl-mpm/data-ekl/",
                ]:
    print(top_dir)
    width = 0.49*5.90666
    height = width / 1.4
    plt.figure(figsize=(width,height))
    plt.title(top_dir)
    regex = re.compile(r'^output.*')
    folders = list(filter(regex.search,os.listdir(top_dir)))
    regex_numbers = re.compile(r'\d+\.\d+')
    def get_load(filename):
        mpm = pd.read_csv(top_dir+filename)
        mpm["disp"] = mpm["disp"]
        mpm["load"] = mpm["load"]
        return mpm

    E = 1e9
    ft = 1e5
    e0 = ft/E

    folders.sort(key=lambda x:float(regex_numbers.findall(x)[0]))
    print(folders)
    folders = folders[:]

    ductility = []
    gf = []

    for i in folders:
        print("loading folder: ",i)
        mpm = get_load("./{}/disp.csv".format(i))
        if len(mpm["load"]) > 0:
            plt.plot(mpm["disp"].values*1e3,mpm["load"].values,label=i)
            d = float(regex_numbers.findall(i)[0])
            g = calculate_gf(mpm["disp"],mpm["load"])
            E = 1e9
            e0 = 1e5/E
            k=2
            R = 1
            gest = (d*k*R*E*(e0*e0))/2
            # gf.append(g)
            # ductility.append(d)

            gf.append(gest)
            ductility.append(g)
            print("{} - GF {}, GF est {}, ratio {}".format(i,g,gest,gest/g))

    plt.xlabel("Displacement (mm)")
    plt.ylabel("Load (N)")
    #plt.legend()
    plt.legend()
    plt.savefig("paper.pdf")
    plt.figure(figsize=(width,height))
    plt.title(top_dir)
    gf = np.array(gf)
    ductility = np.array(ductility)
    plt.scatter(ductility,gf)
    m,b = np.polyfit(ductility, gf, 1)
    plt.axline((0,b),slope=m,ls="--")
    print("{} - offset {} - gradient {}".format(top_dir,b,m))
    plt.savefig("paper_eta-gf.pdf")
plt.show()
