# ToposCif2MSCif V.0
# by wangjiaze on 2022-May-16



import os
import sys
sys.path.append(r'D:\Work\Programs\Normal')
sys.path.append(r'D:\Work\Programs\Normal\Structure')

import ExtractInformation
from WriteCif import WriteCif
from CifFile.CifFile import CifFile

def ToposCifs2MSCifs(inCifDirpath, outCifDirpath):
    inCifFilepaths = ExtractInformation.GetFilenames(inCifDirpath, 'cif')
    outCifFilepaths = []
    for inCifFilepath in inCifFilepaths:
        print(inCifFilepath)
        outCifFilepath = "%s/%s.cif"%(outCifDirpath, ExtractInformation.GetFilename(inCifFilepath))
        cif = CifFile(inCifFilepath, software = 'ToposPro')
        WriteCif(cif.cif2Crystal(), outCifFilepath)
        outCifFilepaths.append(os.path.abspath(outCifFilepath).replace('\\', '/'))
    return outCifFilepaths


if __name__ == '__main__':
    print()
    print("########################################")
    print("#                 ToposCifs2MSCifs V1.0")
    print("#                            2022-May-16")
    print("#                           by wangjiaze")
    print("########################################")
    print()


    import sys

    # inCifDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\#cif'
    # outCifDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\#cif-MS'
    if len(sys.argv) > 1:
        inCifDirpath = sys.argv[1]
        outCifDirpath = sys.argv[2]
        ToposCifs2MSCifs(inCifDirpath, outCifDirpath)
    else:
        inCifDirpath = input('Input ToposPro Cif Folder Path:\n')
        outCifDirpath = input('Output Cif Folder Path:\n')
        ToposCifs2MSCifs(inCifDirpath, outCifDirpath)
        input('Press any key to continue.')
