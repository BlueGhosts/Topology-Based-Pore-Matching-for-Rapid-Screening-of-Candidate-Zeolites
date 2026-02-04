# GetAdoBaseIFs V1.0
# by wangjiaze on 2022-May-14

import sys
sys.path.append(r'D:\Work\Programs\Normal')
sys.path.append(r'D:\Work\Programs\Software\ToposPro')


import ExtractInformation
from AdoFile.AdoFile import AdoFile


def GetToposIFs(adoDirpath, outFilepath):
    adoFilepaths = ExtractInformation.GetFilenames(adoDirpath, 'ado')
    with open(outFilepath, 'w') as file:
        file.write('name,NaturalTiling,nodesNumber,TD10,ringsInFramework,Transivity\n')
        for adoFilepath in adoFilepaths:
            ado = AdoFile(adoFilepath)
            print(ado.name)
            file.write("%s,%s,%s,%s,%s,%s\n" %(ado.name, ado.isNT(), ado.nodesNumber, ado.TD10, ';'.join(ado.ringsInFramework), ado.transitivity))
    return outFilepath


if __name__ == '__main__':
    print()
    print("####################")
    print("  GetAdoBaseIFs V1.0")
    print("         2022-May-14")
    print("        by wangjiaze")
    print("####################")
    print()

    if len(sys.argv) > 1:
        adoDirpath = sys.argv[1]
        outFilepath = sys.argv[2]
        GetToposIFs(adoDirpath, outFilepath)
    else:
        adoDirpath = input('Input Ado Folder Path:\n')
        outFilepath = input('Output File Name:\n') + '.csv'
        GetToposIFs(adoDirpath, outFilepath)
        input('Press any key to continue.')