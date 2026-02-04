# GetBaseIFsByFramework V.0
# by wangjiaze on 2022-May-16

import os
import sys
sys.path.append(r'D:\Work\Programs\Normal')
sys.path.append(r'D:\Work\Programs\software\ToposPro')

import ExtractInformation, WriteCsq
from AdoFile.AdoFile import AdoFile

def GetBaseIFByFramework(adoFilepath):
    name_nodeNumber = {}
    name_TD10 = {}
    ado = AdoFile(adoFilepath)
    atom_csqs = ado.atom_csqByFramework
    TD10s = ado.TD10sByFramework
    for i in range(len(atom_csqs)):
        if len(atom_csqs) == 1:
            nameSuffix = ''
        else:
            nameSuffix = '_%s'%(i+1)
        name = '%s%s'%(ExtractInformation.GetFilename(adoFilepath).split('-')[0], nameSuffix)
        nodeNumber = len(atom_csqs[i])
        TD10 = TD10s[i]
        name_nodeNumber[name] = nodeNumber
        name_TD10[name] = TD10
    return name_nodeNumber, name_TD10

def GetBaseIFsByFramework(adoDirpath, outFilepath):
    allName_nodeNumber = {}
    allName_TD10 = {}
    adoFilepaths = ExtractInformation.GetFilenames(adoDirpath, 'ado')
    for adoFilepath in adoFilepaths:
        print(adoFilepath)
        name_nodeNumber, name_TD10 = GetBaseIFByFramework(adoFilepath)
        allName_nodeNumber.update(name_nodeNumber)
        allName_TD10.update(name_TD10)

    with open(outFilepath, 'w') as file:
        file.write('%s,%s,%s\n'%('name', 'poreTopologyNode', 'TD10'))
        for name in allName_nodeNumber:
            nodeNumber = allName_nodeNumber[name]
            TD10 = allName_TD10[name]
            file.write('%s,%s,%s\n'%(name, nodeNumber, TD10))
    return os.path.abspath(outFilepath).replace('\\', '/')

if __name__ == '__main__':
    print()
    print("########################################")
    print("#             GetBaseIFsByFramework V1.0")
    print("#                            2022-May-16")
    print("#                           by wangjiaze")
    print("########################################")
    print()

    # adoDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\#NT-ado'
    # outFilepath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\IZA_PoresTopology_ToposByFramework.csv'

    import sys
    if len(sys.argv) > 1:
        adoDirpath = sys.argv[1]
        outFilepath = sys.argv[2]
        GetBaseIFsByFramework(adoDirpath, outFilepath)
    else:
        adoDirpath = input('Input Ado Folder Path:\n')
        outFilepath = input('Output File Path:\n') + '.csv'
        GetBaseIFsByFramework(adoDirpath, outFilepath)
        input('Press any key to continue.')
