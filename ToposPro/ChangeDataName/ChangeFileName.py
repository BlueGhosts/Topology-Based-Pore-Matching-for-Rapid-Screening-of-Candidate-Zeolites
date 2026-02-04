import re

# python ChangeDataName -v1.0
# by wangjiaze on 2019-Dec-14

import ExtractInformation
import sys
sys.path.append(r'..\..\lib')


def ChangeFileName(cifFilename, outputPath):
    filename = cifFilename.split('/')[-1].split('\\')[-1]
    with open(cifFilename, 'r') as file:
        contents = file.read()
    newName = re.search('data_(.*)', contents).group(1)
    # newNameContents = re.sub('data_.*', 'data_' + filename.split('.')[0], contents, 1)
    # print(newNameContents)
    with open(outputPath + '/' + newName+ '.cif', 'w') as file:
        file.write(contents)


def ChangeFileNames(inputPath, outputPath):
    cifFilenames = ExtractInformation.GetFilenames(inputPath, 'cif')
    i = 0
    number = len(cifFilenames)
    for cifFilename in cifFilenames:
        print(str(i) + '/' + str(number) + '\t:' + inputPath + '/' + cifFilename.split('/')[-1].split('\\')[-1] + ' > '+ outputPath + '/' + cifFilename.split('/')[-1].split('\\')[-1])
        ChangeFileName(cifFilename, outputPath)
        i += 1


if __name__ == '__main__':
    print()
    print('################################')
    print('            ChangeDataName v-1.0')
    print('                     2019-Dec-14')
    print('                    by wangjiaze')
    print('################################')
    print()

    inputPath = input('input cif folder path:\n')
    outputPath = input('output cif folder path:\n')
    # inputPath = 'D:\Data\FraGen_73\\73_Cif_Ori'
    # outputPath = 'D:\Data\FraGen_73\\73_Cif'
    ChangeFileNames(inputPath, outputPath)