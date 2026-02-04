# Ados2Csqs V.0
# by wangjiaze on 2022-May-19

import os
import sys
sys.path.append(r'D:\Work\Programs\Normal')
sys.path.append(r'D:\Work\Programs\software\ToposPro')

import ExtractInformation, WriteCsq
from AdoFile.AdoFile import AdoFile


def Ado2Csq(adoFilepath, outDirpath):
    outFilepaths = []
    ado = AdoFile(adoFilepath)
    atom_csqs = ado.atom_csqByFramework
    for i in range(len(atom_csqs)):
        atom_csq = atom_csqs[i]
        if len(atom_csqs) == 1:
            nameSuffix = ''
        else:
            nameSuffix = '_%s'%(i+1)
        # csqFilepath = r"%s/%s%s(TD10=%s).csq" % (outDirpath, ExtractInformation.GetFilename(adoFilepath).split('-')[0], nameSuffix, TD10s[i])
        csqFilepath = r"%s/%s%s.csq" % (outDirpath, ExtractInformation.GetFilename(adoFilepath).split('-')[0], nameSuffix)
        outFilepath = os.path.abspath(csqFilepath).replace('\\', '/')
        WriteCsq.WriteCsq(atom_csq, csqFilepath)
        outFilepaths.append(outFilepath)
    return outFilepaths


def Ados2Csqs(adoDirpath, outDirpath):
    outFilepaths = []
    adoFilepaths = ExtractInformation.GetFilenames(adoDirpath, 'ado')
    for adoFilepath in adoFilepaths:
        print(adoFilepath)
        outFilepath = Ado2Csq(adoFilepath, outDirpath)
        outFilepaths += outFilepath
    return outFilepaths


if __name__ == '__main__':
    print()
    print("########################################")
    print("#              Ados2CsqsByFramework V1.0")
    print("#                            2022-May-19")
    print("#                           by wangjiaze")
    print("########################################")
    print()

    # adoDirpath = r'input'
    # outDirpath = r'output'

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