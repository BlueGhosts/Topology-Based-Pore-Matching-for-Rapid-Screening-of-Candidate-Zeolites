# python GetToposInformation V1.0
# by wangjiaze on 2024-May-24

import os
import sys
sys.path.append(r'D:\Work\Programs\Software\ToposPro')

from AdoFile.AdoFile import AdoFile

def GetAdoInformation(adoFile):
    ado = AdoFile(adoFile)
    name = ado.name
    try:
        print('\r  ' + name, end='')
        TD10 = ado.TD10
        csq = ado.csqs
        return name, TD10, csq
    except:
        return name, False, ['False']

def GetToposInformation(adoPath, outCsvPath):
    adoFiles = []
    for filename in os.listdir(adoPath):
        if filename.endswith(".ado"):
            adoFiles.append(os.path.join(adoPath, filename))

    with open(outCsvPath, 'w') as file:
        file.write('name,TD10,csq\n')
        for adoFile in adoFiles[:]: 
            name, TD10, csq = GetAdoInformation(adoFile)
            csq = str(csq).replace(",",';')
            file.write(f'{name},{TD10},{csq}\n')
			
    print('\rAll Done!')

if __name__ == "__main__":
    print("############################")
    print("#        Get_TD10_Csq V1.1 #")
    print("#              2024-Dec-04 #")
    print("#             by wangjiaze #")
    print("############################")
    print()

    # adoPath = r'D:\Work\Programs\Software\ToposPro\SplitAdo\Output'
    # outCsvPath = r'D:\Work\Programs\Software\ToposPro\SplitAdo\Output.csv'

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


