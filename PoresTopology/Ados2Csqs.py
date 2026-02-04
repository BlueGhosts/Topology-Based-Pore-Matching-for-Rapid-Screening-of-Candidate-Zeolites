# Ados2Csqs V.0
# by wangjiaze on 2022-May-15

import os
import sys
sys.path.append(r'D:\Work\Programs\Normal')
sys.path.append(r'D:\Work\Programs\Software\ToposPro')

import ExtractInformation, WriteCsq
from AdoFile.AdoFile import AdoFile


def Ado2Csq(adoFilepath, csqFilepath):
    outFilepath =os.path.abspath(csqFilepath).replace('\\', '/')
    ado = AdoFile(adoFilepath)
    atom_csq = ado.atom_csq
    WriteCsq.WriteCsq(atom_csq, csqFilepath)
    return outFilepath

def Ados2Csqs(adoDirpath, outDirpath):
    outFilepaths = []
    adoFilepaths = ExtractInformation.GetFilenames(adoDirpath, 'ado')
    for adoFilepath in adoFilepaths:
        print(adoFilepath)
        outFilepath = r"%s/%s.csq"%(outDirpath, ExtractInformation.GetFilename(adoFilepath))
        outFilepath = Ado2Csq(adoFilepath, outFilepath)
        outFilepaths.append(outFilepath)
    return outFilepaths

if __name__ == '__main__':
    print()
    print("####################")
    print("      Ados2Csqs V1.0")
    print("         2022-May-15")
    print("        by wangjiaze")
    print("####################")
    print()

    # adoDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\#ado'
    # outDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\#csq'

    import sys
    if len(sys.argv) > 1:
        adoDirpath = sys.argv[1]
        outDirpath = sys.argv[2]
        Ados2Csqs(adoDirpath, outDirpath)
    else:
        adoDirpath = input('Input Ado Folder Path:\n')
        outDirpath = input('Output Csq Folder Path:\n')
        Ados2Csqs(adoDirpath, outDirpath)
        input('Press any key to continue.')