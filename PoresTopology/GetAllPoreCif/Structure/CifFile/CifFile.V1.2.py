# CifFile V1.1
# CifFile V1.2 by wangjiaze on 2025-Mar-02 optimize GetAtoms
# CifFile V1.1 by wangjiaze on 2025-Feb-26  (dont return01) atomCoordinate = [float(atomInformation[3]), float(atomInformation[4]), float(atomInformation[5])] 
# CifFile V1.0 by wangjiaze on 2022-May-24

import re
import sys
sys.path.append(r'..\..\Structure')
import Structure.CoordinateTransformation as CoorTrans
from Structure.Atom.Atom import Atom
from Structure.Bond.Bond import Bond
#from Crystal.Crystal import Crystal

RETAIN = 6

def Rename(name):
    if '_' not in name:
        name = name + '_2'
    else:
        order = int(name.split('_')[-1]) + 1
        name = name.split('_')[0] + '_' + str(order)
    return name

class CifFile():
    def __init__(self, filepath, software = 'MaterialsStudio'):
        self.fileName = filepath.split('\\')[-1].split('/')[-1].split('.')[0]

        file = open(filepath)

        self.software = software
        self.content = file.read()
        self.lines = self.content.split('\n')

        self.name = self.GetName()
        self.groupNumber = self.GetGroupNumber()
        self.spaceGroup = self.GetSpaceGroup()
        self.cellParameter = self.GetCellParameter()
        self.symmetryEquivPosAsXyzs = self.GetSymmetryEquivPosAsXyzs()

        self.atoms = self.GetAtoms()
        self.atomName_atom = {}
        for atom in self.atoms:
            self.atomName_atom[atom.name] = atom
        self.bonds = self.GetBonds()

    def GetName(self):
        name = self.lines[0].split('_')[-1]
        return name

    def GetGroupNumber(self):
        groupNumber = int(re.search("_symmetry_Int_Tables_number\s*(\S*)", self.content).group(1))
        return groupNumber

    def GetSpaceGroup(self):
        if self.software == 'MaterialsStudio' or self.software == 'MS':
            spaceGroup = re.search("_symmetry_space_group_name_H-M\s*(\S*)", self.content).group(1).replace('\'', '')
        elif self.software == 'GULP':
            spaceGroup = CoorTrans.Groupnum2Groupname(self.GetGroupNumber())
        elif self.software == 'ToposPro' or self.software == 'Topos':
            spaceGroup = CoorTrans.Groupnum2Groupname(self.GetGroupNumber())
        else:
            spaceGroup = False
        return spaceGroup

    def GetCellParameter(self):
        a = float(re.search("_cell_length_a\s+(\S*)", self.content).group(1))
        b = float(re.search("_cell_length_b\s+(\S*)", self.content).group(1))
        c = float(re.search("_cell_length_c\s+(\S*)", self.content).group(1))
        A = float(re.search("_cell_angle_alpha\s+(\S*)", self.content).group(1))
        B = float(re.search("_cell_angle_beta\s+(\S*)", self.content).group(1))
        C = float(re.search("_cell_angle_gamma\s+(\S*)", self.content).group(1))
        cellParameter = [a, b, c, A, B, C]
        return cellParameter

    def GetSymmetryEquivPosAsXyzs(self):
        symmetryEquivPosAsXyzs = []
        if self.software == 'MaterialsStudio' or self.software == 'MS':
            information = self.content.split("_symmetry_equiv_pos_as_xyz")[-1].split('_cell_length_a')[0]
            for line in information.split('\n')[1: -1]:
                symmetryEquivPosAsXyzs.append(line.strip())

        elif self.software == 'ToposPro' or self.software == 'Topos':
            information = self.content.split("_symmetry_equiv_pos_as_xyz")[-1].split('loop_')[0]
            for line in information.split('\n')[1: -1]:
                symmetryEquivPosAsXyzs.append(line.strip().split()[-1])
        return symmetryEquivPosAsXyzs

    def GetAtoms(self):
        def Return01(Coordinate):
            x = Coordinate[0]
            y = Coordinate[1]
            z = Coordinate[2]
            while (x < 0):
                x = x + 1
            while (x >= 1):
                x = x - 1

            while (y < 0):
                y = y + 1
            while (y >= 1):
                y = y - 1

            while (z < 0):
                z = z + 1
            while (z >= 1):
                z = z - 1
            
  
            if abs(x - 1/3) <= 0.0001:
                x = 1/3
            elif abs(x - 2/3) <= 0.0001:
                x = 2/3
                
            if abs(y - 1/3) <= 0.0001:
                y = 1/3
            elif abs(y - 2/3) <= 0.0001:
                y = 2/3

            if abs(z - 1/3) <= 0.0001:
                z = 1/3
            elif abs(z - 2/3) <= 0.0001:
                z = 2/3  
                
            x = round(x, RETAIN)
            y = round(y, RETAIN)
            z = round(z, RETAIN)
            return [x, y, z]

        if self.software == 'MaterialsStudio' or self.software == 'MS':
            atoms = []
            atomNames = []
            atomInformations = []
            if '_geom_bond_atom_site_label_1' in self.content:
                lines = self.content.split('_geom_bond_atom_site_label_1')[0].split('_atom_site_label')[-1].split('\n')
            else:
                lines = self.lines.split('_atom_site_label')[-1].split('\n')
                
            for line in lines:
                match = re.search('(\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+)', line)
                if match:
                    atomInformations.append(match.group(1))
            for atomInformation in atomInformations:
                atomInformation = atomInformation.split()

                atomName = atomInformation[0]
                while atomName in atomNames:
                    atomName = Rename(atomName)

                atomElement = atomInformation[1]
                atomCoordinate = Return01([float(atomInformation[2]), float(atomInformation[3]), float(atomInformation[4])])
                atom = Atom(atomName, atomElement, atomCoordinate, self.cellParameter)
                atomNames.append(atomName)
                atoms.append(atom)

        elif self.software == 'GULP':
            atoms = []
            atomInformations = []
            element_num = {}
            for line in self.lines:
                match = re.search('(\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+)', line)
                if match:
                    atomInformations.append(match.group(1))
            for atomInformation in atomInformations:
                atomInformation = atomInformation.split()
                atomElement = re.match('(\w+)(\d+)', atomInformation[0]).group(1)
                if atomElement not in element_num:
                    element_num[atomElement] = 1
                else:
                    element_num[atomElement] = element_num[atomElement] + 1
                atomName = atomElement + str(element_num[atomElement])
                atomCoordinate = Return01([float(atomInformation[1]), float(atomInformation[2]), float(atomInformation[3])])
                atom = Atom(atomName, atomElement, atomCoordinate, self.cellParameter)
                atoms.append(atom)

        elif self.software == 'ToposPro' or self.software == 'Topos':
            atoms = []
            atomNames = []
            atomInformations = []
            
            if '_topos_bond_atom_site_label_1' in self.content:
                lines = self.content.split('_topos_bond_atom_site_label_1')[0].split('atom_site_label')[-1].split('\n')
            else:
                lines = self.lines.split('atom_site_label')[-1].split('\n')
                
            for line in lines:
                match = re.search('(\S+\s+\S+\s+\d+\s+[\d|.]+\s+[\d|.]+\s+[\d|.]+)', line)
                if match:
                    atomInformations.append(match.group(1))
            for atomInformation in atomInformations:
                atomInformation = atomInformation.split()
                atomName = atomInformation[0]
                while atomName in atomNames:
                    atomName = RenameAtom(atomName)
                atomElement = atomInformation[1]
                atomMultiplicity = int(atomInformation[2])
                #atomCoordinate = Return01([float(atomInformation[3]), float(atomInformation[4]), float(atomInformation[5])])
                atomCoordinate = [float(atomInformation[3]), float(atomInformation[4]), float(atomInformation[5])]
                atom = Atom(atomName, atomElement, atomCoordinate, self.cellParameter)
                atom.multiplicity = atomMultiplicity
                atomNames.append(atomName)
                atoms.append(atom)

        else:
            atoms = False
        return atoms

    def GetBonds(self):
        bonds = []
        if (self.software == 'MaterialsStudio' or self.software == 'MS') and '_ccdc_geom_bond_type' in self.content:
            bondNames = []
            bondInformations = []
            for line in self.content.split('_ccdc_geom_bond_type')[-1].split('\n'):
                match = re.search('\S+\s+\S+\s+[\d|\.]+\s+\S+\s+\S+', line)
                if match:
                    bondInformations.append(match.group(0))

            for bondInformation in bondInformations:
                bondInformation = bondInformation.split()

                atom1 = self.atomName_atom[bondInformation[0]]
                atom2 = self.atomName_atom[bondInformation[1]]
                distance = float(bondInformation[2])
                type = bondInformation[4]

                bondName = "%s-%s" %(atom1.name, atom2.name)
                while bondName in bondNames:
                    bondName = Rename(bondName)
                bondNames.append(bondName)

                setSymmetry = []
                if bondInformation[3] == '.':
                    setSymmetry = [1, 5, 5, 5]
                elif '_' in bondInformation[3]:
                    set = bondInformation[3].split('_')
                    setSymmetry = [int(set[0]), int(set[1][0]), int(set[1][1]), int(set[1][2])]
                else:
                    setSymmetry = [int(bondInformation[3]), 5, 5, 5]

                bond = Bond(bondName, atom1, atom2, type, distance, setSymmetry)
                bonds.append(bond)

        elif (self.software == 'ToposPro' or self.software == 'Topos') and '_topos_bond_multiplicity' in self.content:
            bondNames = []
            bondInformations = []
            for line in self.content.split('_topos_bond_multiplicity')[-1].split('#End')[0].split('\n'):
                match = re.search('(\S+\s+\S+\s+[\d|_|\-]+\s+[\d|_|\-]+\s+[\d|.]+\s+[\d|.]+\s+\S+\s+\d+)', line)
                if match:
                    bondInformations.append(match.group(1))

            for bondInformation in bondInformations:
                bondInformation = bondInformation.split()

                atom1 = self.atomName_atom[bondInformation[0]]
                atom2 = self.atomName_atom[bondInformation[1]]
                siteSymmetry1 = [int(i) for i in bondInformation[2].split('_')]
                siteSymmetry2 = [int(i) for i in bondInformation[3].split('_')]
                distance = float(bondInformation[4])
                voronoiSolidangle = bondInformation[5]
                bondMultiplicity = int(bondInformation[7])

                type = bondInformation[6]
                if type != 'V':
                    continue
                else:
                    type = 'S'

                bondName = "%s-%s" %(atom1.name, atom2.name)
                while bondName in bondNames:
                    bondName = Rename(bondName)
                bondNames.append(bondName)

                setSymmetry = []
                setSymmetry.append(siteSymmetry2[0] - siteSymmetry1[0] + 1)
                setSymmetry.append(siteSymmetry2[1] - siteSymmetry1[1] + 5)
                setSymmetry.append(siteSymmetry2[2] - siteSymmetry1[2] + 5)
                setSymmetry.append(siteSymmetry2[3] - siteSymmetry1[3] + 5)

                bond = Bond(bondName, atom1, atom2, type, distance, setSymmetry)
                bond.voronoiSolidangle = voronoiSolidangle
                bond.multiplicity = bondMultiplicity
                bonds.append(bond)
        return bonds

    def cif2Crystal(self):
        from Structure.Crystal.Crystal import Crystal
        crystal = Crystal(self.name, self.groupNumber, self.cellParameter, self.symmetryEquivPosAsXyzs, self.atoms, self.bonds)
        return crystal


if __name__ == '__main__':
    print()
    print("####################")
    print("#       CifFile V1.0")
    print("#        2022-May-24")
    print("#       by wangjiaze")
    print("####################")
    print()


    # adoFilepath = r'example.ado'
    # adoFilepath = r'example2.ado'

    # cifFilepath = r'AFR-PPT1.cif'
    # # cif = CifFile(cifFilepath, 'ToposPro')
    # cifFilepath = r'AFR-PPT1-MS.cif'
    # cif = CifFile(cifFilepath, 'MS')
