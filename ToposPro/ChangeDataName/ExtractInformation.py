import os
import re
import shutil


# ExtractInformation v1.6.5
# by wangjiaze on 2020-Jul-12
# V1.1.1 ExtensionName = False
# V1.2 AddFunction WriteCif ReadCif
# V1.3 AddFunction GetAfterInformation
# V1.4 ReadCif(filename, software = 'MS') support  GULP cif
# V1.5 AddFunction GetLinesInformation(lines, MatchPattern, GroupNumber)
# V1.6 GetAllFilenames(FolderName, ExtensionName = False), CopyFile(filenames, outputPath), MoveFile(filenames, outputPath)
# V1.6.1 ReadCif.RenameAtom
# V1.6.2 spaceGroup = GetInformation(filename, "_symmetry_space_group_name_H-M\s*(\S*)", 1).strip().replace('\'', '')
# V1.6.3 Rewrite Funtion ReadCif(filename, software = 'MS')
#        AddFunction GetFilename(filepath)
# V1.6.4 AddFunction CombineFiles(filenames, outputFilename, titleLineNumber = 0)
#        Rewrite Funtion CopyFiles(filenames, outputPath, export = False)  Add export and error
#        Rewrite Funtion MoveFiles(filenames, outputPath, export = False)  Add export and error
#        AddFunction SplitFiles(filenames, OutputPath, numberFileInOneDir, OutputTitle)
# V1.6.5 AddFunction GetAllDirnames(FolderName)


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


def GetAllDirnames(FolderName):
    dirnames = []
    for home, dirs, files in os.walk(FolderName):
        for filename in dirs:
            dirnames.append(os.path.join(home, filename))
    return dirnames


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


def WriteCif(cifFilename, spaceGroup, groupNumber, cellParameter, atom_atomElement, atom_coordinate):
    from RL_OptimizeStructure0 import CoordinateTransformation as CoorTrans

    file = open(cifFilename, 'w')
    form = "{0:<35}\t{1:<20}\n"
    file.write('data_FraGen(' + str(groupNumber) + '_' + cifFilename.split('/')[-1].split('\\')[-1].split('.')[0] + ')\n')
    file.write(form.format('_audit_creation_method','data-Out2Cif'))
    file.write(form.format('_symmetry_space_group_name_H-M', spaceGroup))
    file.write(form.format('_symmetry_Int_Tables_number', str(groupNumber)))
    file.write(form.format('_symmetry_cell_setting', CoorTrans.Groupnum2CrystalSystem(groupNumber)))
    file.write(form.format('_cell_length_a', cellParameter[0]))
    file.write(form.format('_cell_length_b', cellParameter[1]))
    file.write(form.format('_cell_length_c', cellParameter[2]))
    file.write(form.format('_cell_angle_alpha', cellParameter[3]))
    file.write(form.format('_cell_angle_beta', cellParameter[4]))
    file.write(form.format('_cell_angle_gamma', cellParameter[5]))

    symmetryEquivPosAsXyzs = CoorTrans.GetSymmetryEquivPosAsXyz(spaceGroup)
    file.write('loop_\n')
    file.write('_symmetry_equiv_pos_as_xyz\n')
    for symmetryEquivPosAsXyz in symmetryEquivPosAsXyzs:
        file.write(symmetryEquivPosAsXyz + '\n')

    file.write('loop_\n')
    file.write('_atom_site_label\n')
    file.write('_atom_site_type_symbol\n')
    file.write('_atom_site_fract_x\n')
    file.write('_atom_site_fract_y\n')
    file.write('_atom_site_fract_z\n')

    formAtom = "{0:<10}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\n"
    for atom in atom_atomElement:
        # print(atom)
        atomElement = atom_atomElement[atom]
        coordinate = atom_coordinate[atom]
        file.write(formAtom.format(atom, atomElement, coordinate[0], coordinate[1], coordinate[2]))
    file.close()


def ReadCif(filename, software = 'MS'):
    def RenameAtom(atomName):
        if '_' not in atomName:
            atomName = atomName + '_1'
        else:
            order = int(atomName.split('_')[-1]) + 1
            atomName = atomName.split('_')[0] + '_' + str(order)
        return atomName

    if software == 'MS':
        atom_coordinate = {}
        atom_atomElement = {}
        with open(filename, 'r') as file:
            contents = file.read()
        spaceGroup = re.search("_symmetry_space_group_name_H-M\s*(\S*)", contents).group(1).replace('\'', '')
        groupNumber = int(re.search("_symmetry_Int_Tables_number\s*(\S*)", contents).group(1))
        a = float(re.search("_cell_length_a\s+(\S*)", contents).group(1))
        b = float(re.search("_cell_length_b\s+(\S*)", contents).group(1))
        c = float(re.search("_cell_length_c\s+(\S*)", contents).group(1))
        A = float(re.search("_cell_angle_alpha\s+(\S*)", contents).group(1))
        B = float(re.search("_cell_angle_beta\s+(\S*)", contents).group(1))
        C = float(re.search("_cell_angle_gamma\s+(\S*)", contents).group(1))
        cellParameter = [a, b, c, A, B, C]

        AtomInformations = []
        for line in contents.split('\n'):
            match = re.search('(\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+)', line)
            if match:
                AtomInformations.append(match.group(1))
        for AtomInformation in AtomInformations:
            Atom = AtomInformation.split()
            AtomName = Atom[0]
            while AtomName in atom_atomElement:
                AtomName = RenameAtom(AtomName)

            AtomElement = Atom[1]
            AtomCoordinate = [float(Atom[2]), float(Atom[3]), float(Atom[4])]
            atom_atomElement[AtomName] = AtomElement
            atom_coordinate[AtomName] = AtomCoordinate
        return spaceGroup, groupNumber, cellParameter, atom_atomElement, atom_coordinate

    elif software.upper() == 'GULP':
        from RL_OptimizeStructure0 import CoordinateTransformation as CoorTrans
        atom_coordinate = {}
        atom_atomElement = {}
        groupNumber = int(GetInformation(filename, "_symmetry_Int_Tables_number\s*(\S*)", 1))
        spaceGroup = CoorTrans.Groupnum2Groupname(groupNumber)
        a = float(GetInformation(filename, "_cell_length_a\s+(\S*)", 1))
        b = float(GetInformation(filename, "_cell_length_b\s+(\S*)", 1))
        c = float(GetInformation(filename, "_cell_length_c\s+(\S*)", 1))
        A = float(GetInformation(filename, "_cell_angle_alpha\s+(\S*)", 1))
        B = float(GetInformation(filename, "_cell_angle_beta\s+(\S*)", 1))
        C = float(GetInformation(filename, "_cell_angle_gamma\s+(\S*)", 1))
        cellParameter = [a, b, c, A, B, C]
        AtomInformations = GetInformations(filename, "(\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+)", 1)

        element_num = {}
        for AtomInformation in AtomInformations:
            Atom = AtomInformation.split()
            AtomElement = re.match('(\w+)(\d+)', Atom[0]).group(1)
            if AtomElement not in element_num:
                element_num[AtomElement] = 1
            else:
                element_num[AtomElement] = element_num[AtomElement] + 1
            AtomName = AtomElement + str(element_num[AtomElement])
            AtomCoordinate = [float(Atom[1]), float(Atom[2]), float(Atom[3])]
            atom_atomElement[AtomName] = AtomElement
            atom_coordinate[AtomName] = AtomCoordinate
        return spaceGroup, groupNumber, cellParameter, atom_atomElement, atom_coordinate


if __name__ == '__main__':
    # ReadCif('cif/ABW.cif')
    pass