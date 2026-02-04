# python GetNTList V1.0
# by wangjiaze on 2022-May-15

import os
import sys
sys.path.append(r'D:\Work\Programs\Normal')
import ExtractInformation

def GetNTName(filepath):
    with open(filepath) as file:
        lines = file.readlines()
    structureName = ExtractInformation.GetFilename(filepath)
    NTname = False
    for i in range(len(lines)):
        line = lines[i]
        if 'All proper tilings' in line:
            i = i + 5
            line = lines[i]
            tilingName = line.split('|')[0].strip()
            NTname = "%s/%s"%(structureName, tilingName.split('/')[0]) if 'NT' in tilingName else False
            break
    return NTname

def GetNTList(adoDirpath):
    structureName_NTname = {}
    adoFilepaths = ExtractInformation.GetFilenames(adoDirpath, 'ado')
    for adoFilepath in adoFilepaths:
        print(adoFilepath)
        structureName = ExtractInformation.GetFilename(adoFilepath)
        NTname = GetNTName(adoFilepath)
        structureName_NTname[structureName] = NTname
    return structureName_NTname

def WriteNTList(name_NTname, outFilepath):
    outFilepath = os.path.abspath(outFilepath).replace('\\', '/')
    with open(outFilepath, 'w') as file:
        file.write('%s,%s\n' % ('name', 'NTname'))
        for name, NTname in name_NTname.items():
            file.write('%s,%s\n' % (name, NTname))
    return outFilepath

if __name__ == "__main__":
    print("####################")
    print("      GetNTList V1.0")
    print("         2022-May-15")
    print("        by wangjiaze")
    print("####################")
    print()

    # adoDirpath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\Framework\IZA-ado'
    # outFilepath = 'Output.csv'
    import sys

    if len(sys.argv) > 1:
        adoDirpath = sys.argv[1]
        outFilepath = sys.argv[2]
        structureName_NTname = GetNTList(adoDirpath)
        WriteNTList(structureName_NTname, outFilepath)
    else:
        adoDirpath = input('Input Ado Folder Path:\n')
        outFilepath = input('Output File Path:\n') + '.csv'
        structureName_NTname = GetNTList(adoDirpath)
        WriteNTList(structureName_NTname, outFilepath)
        input('Press any key to continue.')
