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
width = 1*5.90666
height = width / 1.4
plt.figure(figsize=(width,height))

E = 1
nu = 0.2
de3 = (E/((1+nu) * (1-(2*nu)))) * np.array([[1-nu,nu,nu], [nu,1-nu,nu], [nu,nu,1-nu]])


eps1 = np.linspace(-10,10,100)
plt.plot(eps1, (de3[0,0]*eps1 + de3[0,1]*eps1))

plt.show()
