# python WriteCif V1.0
# by wangjiaze on 2022-May-17
import os
import sys

# import CoordinateTransformation as CoorTrans
import ExtractInformation
from Structure.CifFile.CifFile import CifFile
from WriteCif import WriteCif

def Topocif2MScif(cifDirpath, outDirpath):
    filepaths = ExtractInformation.GetFilenames(cifDirpath)
    for filepath in filepaths:
        print("\r%s running!"%filepath, end = "         ")
        filename = ExtractInformation.GetFilename(filepath)
        outFilepath =  "%s/%s.cif"%(outDirpath, filename)
        crystal = CifFile(filepath, software = 'ToposPro').cif2Crystal()
        WriteCif(crystal, outFilepath)
    print("\rAll Done!                                                                             \n")

if __name__ == "__main__":
    print("####################")
    print("# Topocif2MScif v1.0")
    print("#        2025-Feb-16")
    print("#       by wangjiaze")
    print("####################")
    print()

    import sys
    if len(sys.argv) > 1:
        cifDirpath = sys.argv[1]
        outDirpath = sys.argv[2]
        Topocif2MScif(cifDirpath, outDirpath)
    else:
        cifDirpath = input("IN Topos Cif Folder path:\n")
        outDirpath = input("Out MS Cif Folder path:\n")
        Topocif2MScif(cifDirpath, outDirpath)
        input("Please any key to continue.")