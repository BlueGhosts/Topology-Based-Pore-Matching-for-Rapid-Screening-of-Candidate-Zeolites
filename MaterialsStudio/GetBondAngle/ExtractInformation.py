# ExtractInformation V2.0
# by wangjiaze on 2022-May-15

# V2.0 (2022-May-15):
#        Delete Function ReadCif(filename, software = 'MS')
#        Delete Function WriteCif(cifFilename, spaceGroup, groupNumber, cellParameter, atom_atomElement, atom_coordinate)
#        AddFuntion AppendCsvLines(infilename1, infilename2, outfilename)   // Original function name MeltingIF
# V1.6.4 (2020-Mar-17) :
#        AddFuntion CombineFiles(filenames, outputFilename, titleLineNumber = 0)
#        Rewrite Funtion CopyFiles(filenames, outputPath, export = False)  Add export and error
#        Rewrite Funtion MoveFiles(filenames, outputPath, export = False)  Add export and error
#        AddFuntion SplitFiles(filenames, OutputPath, numberFileInOneDir, OutputTitle)
# V1.6.3 Rewrite Funtion ReadCif(filename, software = 'MS')
#        AddFuntion GetFilename(filepath)
# V1.6.2 spaceGroup = GetInformation(filename, "_symmetry_space_group_name_H-M\s*(\S*)", 1).strip().replace('\'', '')
# V1.6.1 ReadCif.RenameAtom
# V1.6 GetAllFilenames(FolderName, ExtensionName = False), CopyFile(filenames, outputPath), MoveFile(filenames, outputPath)
# V1.5 AddFuntion GetLinesInformation(lines, MatchPattern, GroupNumber)
# V1.4 ReadCif(filename, software = 'MS') support  GULP cif
# V1.3 AddFuntion GetAfterInformation
# V1.2 AddFuntion WriteCif ReadCif
# V1.1.1 ExtensionName = False

import os
import re
import shutil

def GetFilename(filepath):
    return filepath.split('\\')[-1].split('/')[-1].split('.')[0]


def GetFilenames(FolderName, ExtensionName = False):
    filenames = []
    for filename in os.listdir(FolderName):
        if ExtensionName:
            if filename.split('.')[-1] == ExtensionName:
                filenames.append(FolderName + '/' +filename)
        else:
            filenames.append(FolderName + '/' + filename)
    return filenames


def GetAllFilenames(FolderName, ExtensionName = False):
    filenames = []
    for home, dirs, files in os.walk(FolderName):
        for filename in files:
            if ExtensionName:
                if filename.split('.')[-1] == ExtensionName:
                    filenames.append(os.path.join(home, filename))
            else:
                filenames.append(os.path.join(home, filename))
    return filenames


def GetInformation(Filename, MatchPattern, GroupNumber):
    file = open(Filename, 'r')
    information = False
    while True:
        line = file.readline()
        if not line:
            if information == False:
                information = 'error'
                return information
        match = re.search(MatchPattern, line)
        if match:
            information = re.search(MatchPattern, line).group(GroupNumber)
            return information


def GetInformations(Filename, MatchPattern, GroupNumber):
    file = open(Filename, 'r')
    informations = []

    while True:
        line = file.readline()
        if not line:
            return informations
        match = re.search(MatchPattern, line)
        if match:
            informations.append(re.search(MatchPattern, line).group(GroupNumber))


def GetLinesInformation(lines, MatchPattern, GroupNumber):
    for line in lines:
        match = re.search(MatchPattern, line)
        if match:
            information = re.search(MatchPattern, line).group(GroupNumber)
            return information
    return False


def GetAfterInformation(file, MatchPattern, GroupNumber):
    position = file.tell()
    information = False
    while True:
        line = file.readline()
        if not line:
            if information == False:
                information = 'error'
                file.seek(position)
                return information
        match = re.search(MatchPattern, line)
        if match:
            information = re.search(MatchPattern, line).group(GroupNumber)
            file.seek(position)
            return information


def CopyFiles(filenames, outputPath, export = False):
    i = 1
    number = len(filenames)
    for filename in filenames:
        if export:
            print('%d / %d : %s'%(i, number, filename), end = '\t')
            try:
                shutil.copy(filename, outputPath)
                print('Done!')
            except FileNotFoundError:
                print('FileNotFoundError!')
        else:
            try:
                shutil.copy(filename, outputPath)
            except FileNotFoundError:
                pass
        i += 1


def MoveFiles(filenames, outputPath, export = False):
    i = 1
    number = len(filenames)
    for filename in filenames:
        if export:
            print('%d / %d : %s'%(i, number, filename), end = '\t')
            try:
                shutil.move(filename, outputPath)
                print('Done!')
            except FileNotFoundError:
                print('FileNotFoundError!')
        else:
            try:
                shutil.move(filename, outputPath)
            except FileNotFoundError:
                pass
        i += 1


def SplitFiles(filenames, OutputPath, numberFileInOneDir, OutputTitle):
    def mkdir(path):
        path = path.strip()
        path = path.rstrip("\\").rstrip("/")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False

    order = 1
    i = 1
    newDir = OutputPath + '/'+ OutputTitle + '_' + str(order)
    mkdir(newDir)
    for filepath in filenames:
        if i > numberFileInOneDir:
            i = 1
            order += 1
            newDir = OutputPath+ '/'+ OutputTitle + '_' +str(order)
            mkdir(newDir)
        filename = filepath.split('/')[-1].split('\\')[-1]
        shutil.copyfile(filepath, newDir+'/'+filename)
        i += 1


def CombineFiles(filenames, outputFilename, titleLineNumber = 0):
    with open(outputFilename, 'w') as file:
        with open(filenames[0], 'r') as f:
            lines = f.readlines()
        for line in lines[0: titleLineNumber]:
            file.write(line)
        for filename in filenames:
            with open(filename, 'r') as f:
                lines = f.readlines()
            for line in lines[titleLineNumber: -1]:
                file.write(line)
            file.write(lines[-1].rstrip() + '\n')


def AppendCsvLines(infilename1, infilename2, outfilename):
    def GetName_linelist(filename):
        name_linelist = {}
        with open(filename, 'r') as file:
            lines = file.readlines()
        for line in lines[1:]:
            name = line.split(',')[0]
            name_linelist[name] = line.strip().split(',')[1:]
        return name_linelist

    def GetTitles(filename):
        with open(filename, 'r') as file:
            titles = file.readline().strip().split(',')
        return titles

    name_linelist1 = GetName_linelist(infilename1)
    title1 = GetTitles(infilename1)
    name_linelist2 = GetName_linelist(infilename2)
    title2 = GetTitles(infilename2)

    title = title1 + title2[1:]
    with open(outfilename, 'w') as file:
        file.write(','.join(title) + '\n')
        for name in name_linelist1:
            linelist1 = name_linelist1[name]
            if name not in name_linelist2:
                linelist = linelist1 +  ['False'] * len(title2[1:])
            else:
                linelist2 = name_linelist2[name]
                linelist = linelist1 + linelist2
            file.write("%s,%s\n"%(name, ','.join(linelist)))



if __name__ == '__main__':
    # infilename1 = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Cif\GULP\Round3\IZA-Table_OptimizationHistory_origin1.csv'
    # infilename2 = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Cif\GULP\Round3\OptimizationHistory_origin2.csv'
    # outfilename = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Cif\GULP\Round3\IZA-Table_OptimizationHistory_origin1_origin2.csv'
    # AppendCsvLines(infilename1, infilename2, outfilename)
    pass