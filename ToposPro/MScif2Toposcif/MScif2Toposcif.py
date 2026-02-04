# python MScif2Toposcif V1.0
# by wangjiaze on 2025-Feb-23
import os
import sys

import ExtractInformation
from Structure.CifFile.CifFile import CifFile
from WriteCif import WriteCif

def MScif2Toposcif(cifDirpath, outDirpath):
    filepaths = ExtractInformation.GetFilenames(cifDirpath)
    for filepath in filepaths:
        print("\r%s running!"%filepath, end = "         ")
        filename = ExtractInformation.GetFilename(filepath)
        outFilepath =  "%s/%s.cif"%(outDirpath, filename)
        crystal = CifFile(filepath, software = 'MS').cif2Crystal()
        WriteCif(crystal, outFilepath, software = 'ToposPro')
    print("\rAll Done!                                                                             \n")

if __name__ == "__main__":
    print("######################")
    print("# MScif2Toposcif v1.0#")
    print("#          2025-Feb-23")
    print("#         by wangjiaze")
    print("######################")
    print()

    # cifDirpath = r"P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology\02_Cif\07_Table-MS-NT-DeleteNotConnection-DeleteBridge-Topos\TEST\MS"
    # outDirpath = r"P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology\02_Cif\07_Table-MS-NT-DeleteNotConnection-DeleteBridge-Topos\TEST\MS-Topo"
    import sys
    if len(sys.argv) > 1:
        cifDirpath = sys.argv[1]
        outDirpath = sys.argv[2]
        MScif2Toposcif(cifDirpath, outDirpath)
    else:
        cifDirpath = input("IN MS Cif Folder path:\n")
        outDirpath = input("Out ToposPro Cif Folder path:\n")
        MScif2Toposcif(cifDirpath, outDirpath)
        input("Please any key to continue.")