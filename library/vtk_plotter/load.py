
def get_data(filename):
    global reader
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
    damage = GetScalar("sig_xx")
    #damage = GetScalar("plastic_strain")
    return pd.DataFrame({"coord_x":xy[:,0], "coord_y":xy[:,1],"lx":lx,"ly":ly,"damage":damage})

def get_data_all(folder,frame_number):
    print(frame_number)
    regex = re.compile(r'sim(_\d+)?_{}.vtk'.format(frame_number))
    files = list(filter(regex.search,os.listdir(folder)))
    subframes = [get_data(folder + "/" + f) for f in files]
    df = pd.concat(subframes)
    return df



def load_folder(folder):
