import matplotlib.pyplot as plt
import pandas as pd
import re
import os

top_dir = "./data/tpb/gf_24/"
#top_dir = "/nobackup/rmvn14/thesis/tpb/vtk_data/"
output_regex = re.compile("output-*")
output_list = list(filter(output_regex.match,os.listdir(top_dir)))
output_list.sort()

data = pd.read_csv("load-disp.csv")
plt.plot(data["disp"].values ,data["load"].values,label="Data")

for f in output_list:
    mpm = pd.read_csv("{}/{}/".format(top_dir,f)+"disp.csv")
    plt.plot(-1e3*mpm["disp"].values,0.013*mpm["load"].values,label=f,marker="x")

plt.legend()
plt.show()
