# FindSameCsq V.0
# by wangjiaze on 2022-May-19

import os
import sys
sys.path.append(r'../../lib')
sys.path.append(r'../../ToposPro')
# sys.path.append(r'D:\Work\Programs\software\ToposPro')

import ExtractInformation
from AdoFile.AdoFile import AdoFile
from CoordinationSequence.CoordinationSequence import CoordinationSequence as Csq

def FindSameCsq(targetAdopath, checkAdoDirpath, outCsvpath, csqlength = 10):
    targetAdo = AdoFile(targetAdopath)
    targetAtom_csq = targetAdo.atom_csqByFramework
    # targetcsq = Csq(targetAdo.csqs, unique = False)
    targetcsq = Csq([ csq[:csqlength] for csq in targetAdo.csqs], unique = False)
    # print(targetcsq)
    print(targetAdo.name, targetcsq)
    # print(targetcsq)
    # ado_csq = []
    for adoFilepath in ExtractInformation.GetFilenames(checkAdoDirpath, 'ado'):
        ado = AdoFile(adoFilepath)
        # print(ado.name)
        # print(ado.allCsqs)
        try:
            csqs = [csq for csqlist in ado.allCsqs for csq in csqlist]
            csqs = Csq([ csq[:10] for csq in csqs], unique = False)
        except:
            print('ERROR:', ado.name, ado.allCsqs)
            exit()
        

        if targetcsq == csqs:
            print(ado.name)
            # print(ado.name, csqs)


if __name__ == '__main__':
    print()
    print("########################################")
    print("#              FindSameCsq V1.0")
    print("#                            2022-May-19")
    print("#                           by wangjiaze")
    print("########################################")
    print()

    targetAdopath = r'P:\Project\PoreTopology\01_IZA\02_Process\04_PoreTopology_Deletebridge\01_Ado\Table_NT\CHA-PPT1.ado'
    # targetAdopath = r'P:\Project\PoreTopology\01_IZA\02_Process\04_PoreTopology_Deletebridge\01_Ado\Table_NT\AEN-PPT1.ado'
    # checkAdoDirpath = r'P:\Project\PoreTopology\01_IZA\02_Process\04_PoreTopology_Deletebridge\01_Ado\Table_NT'
    checkAdoDirpath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology\01_Ado\Table_NT'
    checkAdoDirpath = r'P:\Project\PoreTopology\03_Deem\02_Process\03_PoreTopology\01_#Ado\03_Deem-NT-DB'
    outCsvpath = r'output'

    import sys
    if len(sys.argv) > 1:
        adoDirpath = sys.argv[1]
        outDirpath = sys.argv[2]
        FindSameCsq(targetAdopath, checkAdoDirpath, outCsvpath)
    else:
        # adoDirpath = input('Input Ado Folder Path:\n')
        # outDirpath = input('Output Csq Folder Path:\n')
        FindSameCsq(targetAdopath, checkAdoDirpath, outCsvpath)
        # input('Press any key to continue.')