# python GetToposInformation V1.0
# by wangjiaze on 2024-May-24

import os
import sys
# sys.path.append(r'D:\Work\Programs\Software\ToposPro')
sys.path.append(r'..\..\ToposPro')

from AdoFile.AdoFile import AdoFile

def GetAdoInformation(adoFile):
    ado = AdoFile(adoFile)
    name = ado.name
    try:
        print('\r  ' + name, end='')
        TD10s = ado.TD10sByFramework
        csqs = ado.allCsqs
        return name, TD10s, csqs
    except:
        return name, False, [['False']]

def GetToposInformation(adoPath, outCsvPath):
    adoFiles = []
    for filename in os.listdir(adoPath):
        if filename.endswith(".ado"):
            adoFiles.append(os.path.join(adoPath, filename))

    with open(outCsvPath, 'w') as file:
        file.write('name,TD10s,csqs,nodeNumber\n')
        for adoFile in adoFiles[:]:
            # print(filename)
            name, TD10s, csqs = GetAdoInformation(adoFile)
            
            # print(name, TD10s, csqs)
            if len(TD10s) == 0:
                file.write(f'{name},NA,NA,NA\n')
            elif len(TD10s) > 1:
                for order in range(len(TD10s)):
                    csq = str(csqs[order]).replace(",",';')
                    file.write(f'{name}_{order+1},{TD10s[order]},{csq},{len(csqs[order])}\n')
            else:
                csq = str(csqs[0]).replace(",",';')
                file.write(f'{name},{TD10s[0]},{csq},{len(csqs[0])}\n')
                
    print('\rAll Done!')

if __name__ == "__main__":
    print("############################")
    print("#        Get_TD10_Csq V1.1 #")
    print("#              2024-Dec-04 #")
    print("#             by wangjiaze #")
    print("############################")
    print()

    # adoPath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology\Test'
    # outCsvPath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology\Test.csv'

    import sys
    if len(sys.argv) > 1:
        adoPath = sys.argv[1]
        outCsvPath = sys.argv[2]
        GetToposInformation(adoPath, outCsvPath)
    else:
        adoPath = input('Input Ado Files Folder Path:\n')
        outCsvPath =  input('Output File Path:\n') + '.csv'
        GetToposInformation(adoPath, outCsvPath)
        input('Press any key to Finish.')


