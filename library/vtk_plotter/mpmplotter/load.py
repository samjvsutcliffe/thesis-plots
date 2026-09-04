import pandas as pd
import numpy as np
from vtk import vtkUnstructuredGridReader
from vtk.util import numpy_support as VN
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
import re
import os
import json

def get_data(filename,colour_name="sig_xx",extract_vals=[]):
    reader = vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.ReadAllVectorsOn()
    reader.ReadAllScalarsOn()
    reader.Update()

    data = reader.GetOutput()

    vtk_points = data.GetPoints()
    xyz3d = vtk_to_numpy( vtk_points.GetData() )
    xy = xyz3d[:,0:2]
    scalar_names = [reader.GetScalarsNameInFile(i) for i in range(0, reader.GetNumberOfScalarsInFile())]
    scalar_data = data.GetPointData()
    #scalar_names = scalar_data.GetArrayNames()
    def GetScalar(scalar_name):
        return vtk_to_numpy(scalar_data.GetArray(scalar_names.index(scalar_name)))
    lx = GetScalar("size_x")
    ly = GetScalar("size_y")

    lxx = GetScalar("size_x")
    lyy = GetScalar("size_y")
    lxy = GetScalar("size_x")
    lyx = GetScalar("size_y")
    # lxx = GetScalar("size_xx")
    # lyy = GetScalar("size_yy")
    # lxy = GetScalar("size_xy")
    # lyx = GetScalar("size_yx")

    damage = GetScalar(colour_name)
    uid = GetScalar("unique-id")
    output_data = {
        "coord_x":xy[:,0],
        "coord_y":xy[:,1],
        "lx":lx,"ly":ly,
        "colour":damage,
        "uid":uid,
        "lxx":lxx,
        "lyy":lyy,
        "lxy":lxy,
        "lyx":lyx
    }
    for v in extract_vals:
        output_data[v] = GetScalar(v)
    return pd.DataFrame(output_data)

def get_data_all(folder,frame_number,colour_name="sig_xx",extract_vals=[]):
    print(frame_number)
    regex = re.compile(r'sim(_\d+)?_{}.vtk'.format(frame_number))
    files = list(filter(regex.search,os.listdir(folder)))
    subframes = [get_data(folder + "/" + f,colour_name,extract_vals) for f in files]
    df = pd.concat(subframes)
    return df


def load_data(folder_data,frame_number,colour_name="sig_xx",extract_vals=[]):
    return get_data_all(folder_data["folder"],folder_data["frames"][frame_number],colour_name,extract_vals)

def load_folder(folder):
    settings_file = "{}/settings.json".format(folder)
    settings = {}
    if os.path.isfile(settings_file):
        with open(settings_file) as f:
            settings = json.load(f)

    files = os.listdir(folder)
    finalcsv = re.compile("sim(_0+)?_\d*\.vtk")
    files_csvs = list(filter(finalcsv.match,files))
    framenumber_regex = re.compile("\d+")
    framenumbers = list(map(lambda x: framenumber_regex.findall(x)[-1],files_csvs))
    framenumbers.sort(key=int)
    files_csvs.sort(key=lambda x:int(framenumber_regex.findall(x)[-1]))
    return {"folder":folder,"settings":settings,"files":files_csvs,"frames":framenumbers}

