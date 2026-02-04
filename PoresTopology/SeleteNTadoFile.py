# python SeleteNTadoFile V1.0
# by wangjiaze on 2022-May-15

import os
import sys
sys.path.append(r'D:\Work\Programs\Normal')
import ExtractInformation
from GetNTList import GetNTList

def SeleteNTadoFile(adoDirpath, duelNetAdoDirpath, outDirpath):
    structureName_NTname = GetNTList(adoDirpath)
    duelNetAdofilepaths = ["%s/%s.ado"%(duelNetAdoDirpath, NTname.replace('/', '-')) if NTname else ''
                           for NTname in structureName_NTname.values()]
    ExtractInformation.CopyFiles(duelNetAdofilepaths, outDirpath, True)
    return [os.path.abspath(filepath).replace('\\', '/') for filepath in duelNetAdofilepaths]

if __name__ == "__main__":
    print("####################")
    print("SeleteNTadoFile V1.0")
    print("         2022-May-15")
    print("        by wangjiaze")
    print("####################")
    print()

    # adoDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\Framework\IZA-ado'
    # duelNetAdoDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\#ado'
    # outDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\#NT-ado'
    import sys

    if len(sys.argv) > 1:
        adoDirpath = sys.argv[1]
        duelNetAdoDirpath = sys.argv[2]
        outDirpath = sys.argv[3]
        SeleteNTadoFile(adoDirpath, duelNetAdoDirpath, outDirpath)
    else:
        adoDirpath = input('Input Framework Ado Folder Path:\n')
        duelNetAdoDirpath = input('Input duelNet Ado Folder Path:\n')
        outDirpath = input('Output Ado Folder Path:\n')
        SeleteNTadoFile(adoDirpath, duelNetAdoDirpath, outDirpath)
        input('Press any key to continue.')
