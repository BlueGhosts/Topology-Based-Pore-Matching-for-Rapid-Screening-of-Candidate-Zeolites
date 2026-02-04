# python SeleteNTadoFile V1.0
# by wangjiaze on 2022-May-15

import os
import sys
sys.path.append(r'D:\Work\Programs\Normal')
import ExtractInformation
from GetNTList import GetNTList

def SeleteNTcifFile(adoDirpath, duelNetCifDirpath, outDirpath):
    structureName_NTname = GetNTList(adoDirpath)
    print(structureName_NTname)
    duelNetCiffilepaths = ["%s/%s.cif"%(duelNetCifDirpath, NTname.replace('/', '-').replace('PPT 1', 'PPT1')) if NTname else ''
                           for NTname in structureName_NTname.values()]
    ExtractInformation.CopyFiles(duelNetCiffilepaths, outDirpath, True)
    return [os.path.abspath(filepath).replace('\\', '/') for filepath in duelNetCiffilepaths]

if __name__ == "__main__":
    print("####################")
    print("SeleteNTadoFile V1.0")
    print("         2022-May-15")
    print("        by wangjiaze")
    print("####################")
    print()

    # adoDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\Framework\IZA-ado'
    # duelNetCifDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\#ado'
    # outDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\#NT-ado'
    import sys

    if len(sys.argv) > 1:
        adoDirpath = sys.argv[1]
        duelNetCifDirpath = sys.argv[2]
        outDirpath = sys.argv[3]
        SeleteNTadoFile(adoDirpath, duelNetCifDirpath, outDirpath)
    else:
        adoDirpath = input('Input Framework Ado Folder Path:\n')
        duelNetCifDirpath = input('Input duelNet cif Folder Path:\n')
        outDirpath = input('Output cif Folder Path:\n')
        SeleteNTcifFile(adoDirpath, duelNetCifDirpath, outDirpath)
        input('Press any key to continue.')
