# GetCsq&Bond&Angel V1.0
# by wangjiaze on 2025-Mar-03

import os
import sys
import re
sys.path.append(r'../../lib')
sys.path.append(r'../../ToposPro')
sys.path.append(r'P:\Project\Program\ToposPro')
sys.path.append(r'P:\Project\Program\ToposPro')

import ExtractInformation
from AdoFile.AdoFile import AdoFile
from CoordinationSequence.CoordinationSequence import CoordinationSequence as Csq
from CoordinationSequence.CoordinationSequence import AtomCoordinationSequence as AtomCsq
class Chain():
    def __init__(self, chainType, chainAtomNames, chainTD10, chain_atom_csq):
        self.types = chainType
        self.atomNames = chainAtomNames
        self.TD10 = chainTD10
        self.atom_csq = chain_atom_csq
        
class Plane():
    def __init__(self, planeType, planeAtomNames, planeTD10, plane_atom_csq):
        self.types = planeType
        self.atomNames = planeAtomNames
        self.TD10 = planeTD10
        self.atom_csq = plane_atom_csq
 
class Framework():
    def __init__(self, frameworkAtomNames, frameworkTD10, framework_atom_csq):
        self.type = [1, 1, 1]
        self.atomNames = frameworkAtomNames
        self.TD10 = frameworkTD10
        self.atom_csq = framework_atom_csq
 
class AdoFileDimension(AdoFile):
    def __init__(self, adoFilepath):
        super().__init__(adoFilepath)
        self.molecularComplexNumber = self.GetMolecularComplex()
        self.chains = self.GetChains()
        self.planes = self.GetPlanes()
        self.frameworks = self.GetFrameworks()
        self.dimensionType, self.dimensionType_str, self.dimensionNumber = self.CalculateDimension()
    
    def GetMolecularComplex(self):
        if 'molecular complex groups ZA' in self.content:
            molecularComplexNumber = len(re.findall('molecular complex groups ZA', self.content))
        else:
            molecularComplexNumber = 0
        return molecularComplexNumber
      
    def GetChains(self):
        # chains [ 1 0` 0] with ZA
        chains = [] 
        if 'chains' in self.content:
            chainsInformations = re.findall('chains.*?TD10.*?\n', self.content, re.DOTALL)
            for chainsInformation in chainsInformations:
                chainTypes = []
                chainTypeContents = re.findall('\[.*?\]', chainsInformation.split('\n')[0])
                for chainTypeContent in chainTypeContents:
                    chainTypeSearch = re.search('\[-?\s*(\d+)\s*(-?\d+)\s*(-?\d+)\]', chainTypeContent)
                    # print(chainTypeContent)
                    # print(chainTypeSearch.group(1), chainTypeSearch.group(2), chainTypeSearch.group(3))
                    chainType = [int(chainTypeSearch.group(1)), int(chainTypeSearch.group(2)), int(chainTypeSearch.group(3))]
                    chainTypes.append(chainType)
                    
                chainAtomNames = [ atom.replace(":", "") for atom in re.findall('ZA\d+:', chainsInformation)]
                chainTD10 = int(re.search('TD10=(\d+)', chainsInformation).group(1))
                
                chain_atom_csq = {}
                chain_atom_csq = {atom: atom_csq[atom] for atom_csq in self.atom_csqByFramework for atom in chainAtomNames if atom in atom_csq}
                chain = Chain(chainTypes, chainAtomNames, chainTD10, chain_atom_csq)
                # print(chainTypes, chainAtomNames, chainTD10)
                
                chains.append(chain)
        return chains
            
    def GetPlanes(self):
        # plane layers ( 1 0 0) with ZA
        planes = []
        if 'plane layers' in self.content:
            planesInformations = re.findall('plane layers.*?TD10.*?\n', self.content, re.DOTALL)
            for planesInformation in planesInformations:
                # print(planesInformation)
                planeTypes = []
                planeTypeContents = re.findall('\(.*?\)', planesInformation.split('\n')[0])
                for planeTypeContent in planeTypeContents:
                    planeTypeSearch = re.search('\(-?\s*(\d+)\s*(-?\d+)\s*(-?\d+)\)', planeTypeContent)
                    planeType = [int(planeTypeSearch.group(1)), int(planeTypeSearch.group(2)), int(planeTypeSearch.group(3))]
                    planeTypes.append(planeType)
                    
                planeAtomNames = [ atom.replace(":", "") for atom in re.findall('ZA\d+:', planesInformation)]
                planeTD10 = int(re.search('TD10=(\d+)', planesInformation).group(1))
                # plane_atom_csq = [ atom_csq for atom_csq in self.atom_csqByFramework for atom in planeAtomNames if atom in atom_csq]
                plane_atom_csq = {atom: atom_csq[atom] for atom_csq in self.atom_csqByFramework for atom in planeAtomNames if atom in atom_csq}
                # print(planeTypes, planeAtomNames, planeTD10)
                plane = Plane(planeTypes, planeAtomNames, planeTD10, plane_atom_csq)
                
                planes.append(plane)
        return planes
            
    def GetFrameworks(self):
        frameworks = []
        if '3D framework with ZA' in self.content:
            frameworksInformations = re.findall('3D framework with ZA.*?TD10.*?\n', self.content, re.DOTALL)
            for frameworksInformation in frameworksInformations:
                
                frameworkAtomNames = [ atom.replace(":", "") for atom in re.findall('ZA\d+:', frameworksInformation)]
                frameworkTD10 = int(re.search('TD10=(\d+)', frameworksInformation).group(1))
                # framework_atom_csq = [ atom_csq for atom_csq in self.atom_csqByFramework for atom in frameworkAtomNames if atom in atom_csq]
                framework_atom_csq = {atom: atom_csq[atom] for atom_csq in self.atom_csqByFramework for atom in frameworkAtomNames if atom in atom_csq}
                
                framework = Framework(frameworkAtomNames, frameworkTD10, framework_atom_csq)
                # print(framework.type, frameworkAtomNames, frameworkTD10)
                frameworks.append(framework)
        return frameworks

    def CalculateDimension(self):
        dimensionType = [0, 0, 0] 
        dimensionType_str = ["", "", ""]
        for chains in self.chains:
            # print(chains.types)
            for chainType in chains.types:
                dimensionType[0] += chainType[0]
                dimensionType[1] += chainType[1]
                dimensionType[2] += chainType[2]
            dimensionType_str[0] = '1D'

        for plane in self.planes:
            for planeType in plane.types:
                # print(planeType)
                vector = [1, 1, 1]
                if planeType[0] != 0:
                    vector[0] = 0
                if planeType[1] != 0:
                    vector[1] = 0
                if planeType[2] != 0:
                    vector[2] = 0        
                # print(vector)
                
                dimensionType[0] += vector[0]
                dimensionType[1] += vector[1]
                dimensionType[2] += vector[2]
            dimensionType_str[1] = '2D'
            
        for framework in self.frameworks:
            dimensionType[0] += framework.type[0]
            dimensionType[1] += framework.type[1]
            dimensionType[2] += framework.type[2]
            dimensionType_str[2] = '3D'    
        
        dimensionType = [1 if dimension != 0 else 0 for dimension in dimensionType]
        dimensionType_str = dimensionType_str[0] + dimensionType_str[1] + dimensionType_str[2]
        dimensionNumber = sum(dimensionType)
        return dimensionType, dimensionType_str, dimensionNumber
        
class Atom:
    def __init__(self, name, atom_xyz, atom_csq):
        self.uniqueName = name
        # self.index = atom_index
        # self.name = name + '_' + str(atom_index)
        self.xyz = atom_xyz
        self.x = atom_xyz[0]
        self.y = atom_xyz[1]
        self.z = atom_xyz[2]
        
        self.csq = atom_csq
    
    def rename(self, atom_index):
        self.index = atom_index
        self.name = self.uniqueName + '_' + str(atom_index)
        
    def __str__(self, *args, **kwds):
        return f"Atom Name: {self.name}, {self.csq}, Coordinates: {self.xyz}"
    
    def __eq__(self, other):
        if not isinstance(other, Atom):
            raise ValueError(f"Atoms can only be compared with other Atom objects, not {type(other)}")
        for i in range(3):
            if self.xyz[i] != other.xyz[i]:
                return False
        return True
    
    def __ne__(self, other):
        if not isinstance(other, Atom):
            raise ValueError(f"Atoms can only be compared with other Atom objects, not {type(other)}")
        
        for i in range(3):
            if self.xyz[i] != other.xyz[i]:
                return True 
        return False

class Bond:
    def __init__(self, name, atom1, atom2, bond_length):
        self.name = name
        self.atom1 = atom1
        self.atom2 = atom2
        self.bond_length = float(bond_length)
        
        self.csq = (atom1.csq, atom2.csq)

    def __str__(self, *args, **kwds):
        return f"Bond: {self.name} {self.atom1.name}-{self.atom2.name}, Length: {self.bond_length}"
    
    def __eq__(self, other):
        # print("Bond __eq__")
        if not isinstance(other, Bond):
            raise ValueError(f"Bonds can only be compared with other Bond objects, not {type(other)}")
        if (self.atom1 == other.atom1 and self.atom2 == other.atom2) or (self.atom1 == other.atom2 and self.atom2 == other.atom1):
            return True
        else:
            return False
        
    def __ne__(self, other):
        # print("Bond __ne__")
        if not isinstance(other, Bond):
            raise ValueError(f"Bonds can only be compared with other Bond objects, not {type(other)}")
        if (self.atom1 == other.atom1 and self.atom2 == other.atom2) or (self.atom1 == other.atom2 and self.atom2 == other.atom1):
            return False
        else:
            return True

class Angle:
    def __init__(self, name, atom1, atom2, atom3, angle_value):
        self.name = name
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom3 = atom3
        self.degree = float(angle_value)
        
        self.csq = (atom1.csq, atom2.csq, atom3.csq)

    def __str__(self, *args, **kwds):
        return f"Angle: {self.name} {self.atom1.name}\{self.atom2.name}/{self.atom3.name}, Value: {self.degree}"
    
    def __eq__(self, other):
        if not isinstance(other, Angle):
            raise ValueError(f"Angles can only be compared with other Angle objects, not {type(other)}")
        if self.atom2 != other.atom2:
            return False  
        if (self.atom1 == other.atom1 and self.atom3 == other.atom3) or (self.atom1 == other.atom3 and self.atom3 == other.atom1):
            return True
        else:
            return False
               
    def __ne__(self, other):
        if not isinstance(other, Angle):
            raise ValueError(f"Angles can only be compared with other Angle objects, not {type(other)}")
        if self.atom2 != other.atom2:
            return True
        if (self.atom1 == other.atom1 and self.atom3 == other.atom3) or (self.atom1 == other.atom3 and self.atom3 == other.atom1):
            return False
        else:
            return True 

    def equalbyCsq(self, other):
        if not isinstance(other, Angle):
            raise ValueError(f"Angles can only be compared with other Angle objects, not {type(other)}")
        if self.atom2 != other.atom2:
            return False
        if (self.atom1.csq == other.atom1.csq and self.atom3.csq == other.atom3.csq) or (self.atom1.csq == other.atom3.csq and self.atom3.csq == other.atom1.csq):
            return True
        else:
            return False
    

   
def CalculatePoreDimension(adoDirpath, outFilepath):
    adoFilepaths = ExtractInformation.GetFilenames(adoDirpath, 'ado')
    with open(outFilepath, 'w') as file:
        file.write('name,molecularComplexNumber,chain,chainAtoms,chainTD,chainAtom_csq,plane,planeAtoms,planeTD,planeAtom_csq,framework,frameworkAtoms,frameworkTD,frameworkAtom_csq,dimensionType_str,dimensionType,dimensionNumber\n')
        # file.write('name,molecularComplexNumber,chain,chainAtoms,chainTD,plane,planeAtoms,planeTD,framework,frameworkAtoms,frameworkTD,dimensionType_str,dimensionType,dimensionNumber\n')
        
        for adoFilepath in adoFilepaths:
            print(adoFilepath)
            ado = AdoFileDimension(adoFilepath)

            file.write(f"{ado.name},{ado.molecularComplexNumber},")
            file.write(f"{str([chain.types for chain in ado.chains]).replace(',', ';')},")
            file.write(f"{str([chain.atomNames for chain in ado.chains]).replace(',', ';')},")
            file.write(f"{str([chain.TD10 for chain in ado.chains]).replace(',', ';')},")
            file.write(f"{str([chain.atom_csq for chain in ado.chains]).replace(',', ';')},")
            
            file.write(f"{str([plane.types for plane in ado.planes]).replace(',', ';')},")
            file.write(f"{str([plane.atomNames for plane in ado.planes]).replace(',', ';')},")
            file.write(f"{str([plane.TD10 for plane in ado.planes]).replace(',', ';')},")
            file.write(f"{str([plane.atom_csq for plane in ado.planes]).replace(',', ';')},")
            
            file.write(f"{str([framework.type for framework in ado.frameworks]).replace(',', ';')},")      
            file.write(f"{str([framework.atomNames for framework in ado.frameworks]).replace(',', ';')},")
            file.write(f"{str([framework.TD10 for framework in ado.frameworks]).replace(',', ';')},")
            file.write(f"{str([framework.atom_csq for framework in ado.frameworks]).replace(',', ';')},")
            
            file.write(f"{str(ado.dimensionType_str).replace(',', ';')},{str(ado.dimensionType).replace(',', ';')},{ado.dimensionNumber}\n")
    return outFilepath


def GetPoreCsq(ado, csqlength = 10, unique = False):
    atomNames = []
    atom_csq = {}
    for chain in ado.chains:
        atomNames += chain.atomNames
        atom_csq.update(chain.atom_csq)
    for plane in ado.planes:
        atomNames += plane.atomNames
        atom_csq.update(plane.atom_csq)
    for framework in ado.frameworks:
        atomNames += framework.atomNames
        atom_csq.update(framework.atom_csq)
        
    csqs = atom_csq.values()
    csqs = Csq([ csq[:csqlength] for csq in csqs], unique = unique)
    return csqs


def GetCsq_Bond_Angle(txtfile, atom_csq):
    def get_or_create_atom(atomName, atomXYZ, atoms, csq):
        def FindAtom(atomOrigin, atoms):
            for atom in atoms:
                if atomOrigin == atom:
                    return atom
                
        atom = Atom(atomName, atomXYZ, csq)
        if atom not in atoms:
            atom.rename(len(atoms)+1)
            atoms.append(atom)
        else:
            atom = FindAtom(atom, atoms)
        return atom     
                   
    def DealAtomInformation(atomInformation):
        atomUniqueName = atomInformation.split('(')[0]
        # print(atomInformation.split('(')[1].split(')')[0].split(';')[2])
        x = float(atomInformation.split('(')[1].split(')')[0].split(';')[0])
        y = float(atomInformation.split('(')[1].split(')')[0].split(';')[1])
        z = float(atomInformation.split('(')[1].split(')')[0].split(';')[2])
        atomXYZ = [float(x), float(y), float(z)]
        return atomUniqueName, atomXYZ
       
    with open(txtfile, 'r') as f:
        lines = f.readlines()
    
    atoms = []
    bonds = []
    angles = []
    for line in lines:
        if line[:4] == "Bond"  and line.strip() != "Bond":
            bondName = line.split(',')[0]
            atom1Information = line.split(',')[1]
            atom2Information = line.split(',')[2]
            bond_length = line.split(',')[3].strip()
            
            atom1_uniqueName, atom1_xyz = DealAtomInformation(atom1Information)
            atom2_uniqueName, atom2_xyz = DealAtomInformation(atom2Information)

            if atom1_uniqueName not in atom_csq or atom2_uniqueName not in atom_csq:
                # print(f"Atom {atom1_uniqueName} or {atom2_uniqueName} not found in atom_csq.")
                continue
            
            atom1 = get_or_create_atom(atom1_uniqueName, atom1_xyz, atoms, atom_csq[atom1_uniqueName])
            atom2 = get_or_create_atom(atom2_uniqueName, atom2_xyz, atoms, atom_csq[atom2_uniqueName])
            
            bond = Bond(bondName, atom1, atom2, bond_length)
            bonds.append(bond)
            
        elif "Angle" in line and line.strip() != "Angle":   
            # print('AAA')
            angleName = line.split(',')[0]
            bond1Information = line.split(',')[1]
            atom2Information = line.split(',')[2]
            bond2Information = line.split(',')[3]
            angleDegree = line.split(',')[4].strip()
            
            atom1Information = "(".join(bond1Information.split('(')[1:]).split(')')[0]
            atom3Information = "(".join(bond2Information.split('(')[1:]).split(')')[0]
            
            atom1_uniqueName, atom1_xyz = DealAtomInformation(atom1Information)
            atom2_uniqueName, atom2_xyz = DealAtomInformation(atom2Information)
            atom3_uniqueName, atom3_xyz = DealAtomInformation(atom3Information)
    
            if atom1_uniqueName not in atom_csq or atom2_uniqueName not in atom_csq or atom3_uniqueName not in atom_csq:
                # print(f"Atom {atom1_uniqueName}, {atom2_uniqueName} or {atom3_uniqueName} not found in atom_csq.")
                continue

            atom1 = get_or_create_atom(atom1_uniqueName, atom1_xyz, atoms, atom_csq[atom1_uniqueName])
            atom2 = get_or_create_atom(atom2_uniqueName, atom2_xyz, atoms, atom_csq[atom2_uniqueName])
            atom3 = get_or_create_atom(atom3_uniqueName, atom3_xyz, atoms, atom_csq[atom3_uniqueName])


            angle = Angle(angleName, atom1, atom2, atom3, angleDegree)
            angles.append(angle)
    # print("Atoms:")
    # for atom in atoms:
    #     print(atom)
    
    # print("Bonds:")
    # for bond in bonds:
    #     print(bond)
    
    # print("Angles:")
    # for angle in angles:
    #     print(angle)
    return atoms, bonds, angles


def GetAtom_csq0(ado, csqlength = 10):
    atom_csq = {}
    for atom, csq in ado.atom_csq.items():
        atom_csq[atom] = AtomCsq(csq[:csqlength])
    return atom_csq

def GetAtom_csq(ado, csqlength = 10):
    atomNames = []
    atom_csq = {}
    for chain in ado.chains:
        atomNames += chain.atomNames
        atom_csq.update(chain.atom_csq)
    for plane in ado.planes:
        atomNames += plane.atomNames
        atom_csq.update(plane.atom_csq)
    for framework in ado.frameworks:
        atomNames += framework.atomNames
        atom_csq.update(framework.atom_csq)
        
        
    # atom_csq = {}
    for atom, csq in atom_csq.items():
        atom_csq[atom] = AtomCsq(csq[:csqlength])
    return atom_csq

def GetBondValue(bonds):
    bondCsq_values = {}
    for bond in bonds:
        if bond.csq not in bondCsq_values:
            bondCsq_values[bond.csq] = [bond.bond_length]
        elif bond.bond_length not in bondCsq_values[bond.csq]:
            bondCsq_values[bond.csq].append(bond.bond_length)

    # print(bondCsq_values)
    return bondCsq_values


def GetAngleValue(angles):
    angleCsq_values = {}
    for angle in angles:
        if angle.csq not in angleCsq_values:
            angleCsq_values[angle.csq] = [angle.degree]
        elif angle.degree not in angleCsq_values[angle.csq]:
            angleCsq_values[angle.csq].append(angle.degree)

    # print(angleCsq_values)        
    return angleCsq_values


def CompareRange(list1, list2, threshold = 0.1):
    value1_flag = {}
    for value1 in list1:
        value1_flag[value1] = False
    for value2 in list2:
        flag = False
        for value1 in list1:
            if ( abs(float(value1) - float(value2))/float(value1) ) <= threshold:
                value1_flag[value1] = True
                flag = True

        if not flag:
            # print(f"Value not found: {value2}")
            return False
 
    for value1, flag in value1_flag.items():
        if not flag:
            # print(f"Value not found: {value1}")
            return False        
    return True


def CompareByBond(bonds1, bonds2, threshold = 0.1):
    bond1Csq_values = GetBondValue(bonds1)
    bond2Csq_values = GetBondValue(bonds2)
    
    # print("Bond1Csq Values:", bond1Csq_values)
    # print("Bond2Csq Values:", bond2Csq_values)    
    for bond1 in bond1Csq_values:
        if bond1 not in bond2Csq_values and (bond1[1], bond1[0]) not in bond2Csq_values:
            # print(f"Bond found: {bond1.name} {bond1.bond_length}")
            # print(f"Bond not found: {bond1.name} {bond1.bond_length}")
            print(f"Bond not found 1")
            return "Bond not found 1"
            return False
        
    for bond2 in bond2Csq_values:
        if bond2 not in bond1Csq_values and (bond1[1], bond1[0]) not in bond1Csq_values:
            # print(f"Bond not found: {bond2.name} {bond2.bond_length}")
            print(f"Bond not found 2")
            return "Bond not found 2"
            return False

    bond1Csq_compareResult = {}
    for bond1, lengths1 in bond1Csq_values.items():
        if bond1 in bond2Csq_values:
            lengths2 = bond2Csq_values[bond1]
        elif (bond1[1], bond1[0]) in bond2Csq_values:
            lengths2 = bond2Csq_values[(bond1[1], bond1[0])]
        else:
            print(f"Bond not found in bond2Csq_values: {bond1}")
            # return False
        result = CompareRange(lengths1, lengths2, threshold)
        bond1Csq_compareResult[bond1] = result

    for bond1, result in bond1Csq_compareResult.items():
        if not result:
            # print(f"Bond length difference: {bond1.name} {bond1Csq_values[bond1]} - {bond2Csq_values[bond1]}")
            return False   
    # print(bond1Csq_compareResult) 
    return True                   
    
    
def CompareByAngle(angles1, angles2, threshold = 0.1):
    angle1Csq_values = GetAngleValue(angles1)
    angle2Csq_values = GetAngleValue(angles2)
    
    for angle1 in angle1Csq_values:
        if angle1 not in angle2Csq_values:
            # print(f"Angle not found: {angle1.name} {angle1.degree}")
            return False
        
    for angle2 in angle2Csq_values:
        if angle2 not in angle1Csq_values:
            # print(f"Angle not found: {angle2.name} {angle2.degree}")
            return False

    angle1Csq_compareResult = {}
    for angle1, degrees1 in angle1Csq_values.items():
        degrees2 = angle2Csq_values[angle1]
        result = CompareRange(degrees1, degrees2, threshold)
        angle1Csq_compareResult[angle1] = result

    for angle1, result in angle1Csq_compareResult.items():
        if not result:
            # print(f"Angle difference: {angle1.name} {angle1Csq_values[angle1]} - {angle2Csq_values[angle1]}")
            return False   
    # print(angle1Csq_compareResult) 
    return True

   
def main0():
    # targetAdo = AdoFileDimension('CHA-PPT 1_6.ado')
    targetAdo = AdoFileDimension(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\CHA\Ado_Manual\CHA-PPT 1_6.ado')
    
    
    targetcsq = GetPoreCsq(targetAdo, csqlength = 10, unique = False)
    # print(targetcsq)  
    # ado1 = AdoFile('CHA-PPT 1_6.ado')
    target_atom_csq = GetAtom_csq(targetAdo)
    target_atoms, target_bonds, target_angles = GetCsq_Bond_Angle(r'CHA-PPT 1_6.txt', target_atom_csq)
    
    
    ado = AdoFileDimension('AEI-PPT 1.ado')
    csq = GetPoreCsq(ado, csqlength = 10, unique = False)
    atom_csq = GetAtom_csq(ado)
    atoms, bonds, angles = GetCsq_Bond_Angle(r'AEI-PPT 1.txt', atom_csq)
    
    if targetcsq == csq:
        # print("The two csqs are equal")
        # CompareByBond(target_atoms, target_bonds, target_angles, atoms, bonds, angles, threshold = 0.3)
        # target_bonds = {'1': 1, '2': 2, '3': 3}
        
        bondResult = CompareByBond(target_bonds, bonds, threshold = 0.3)
        print({"bondResult": bondResult})   
        angleResult = CompareByAngle(target_angles, angles, threshold = 0.1)
        print({"angleResult": angleResult})
    else:
        print("The two csqs are not equal")
  
    
def main_IZA():
    # targetname = 
    # targetAdo = AdoFileDimension('CHA-PPT 1_6.ado')
    targetAdo = AdoFileDimension(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\AEL\Ado_Manual\AEL-PPT 1_6.ado')
    targetcsq = GetPoreCsq(targetAdo, csqlength = 10, unique = False)
    target_atom_csq = GetAtom_csq(targetAdo)
    # print(target_atom_csq)
    # P:\Project\PoreTopology\04_IndustryZEO\04_=MFI\01_IZA\101_3.3-6r\03_BondAngleTxT
    target_atoms, target_bonds, target_angles = GetCsq_Bond_Angle(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\AEL\txt_bondAngle\AEL-PPT 1_6.txt', target_atom_csq)

    
    # path = r'P:\Project\PoreTopology\04_IndustryZEO\05_MFI\01_IZA\301_5.0-10r'
    # path = r'P:\Project\PoreTopology\04_IndustryZEO\04_=MFI\02_ABC6\201_4.2-8r'
    
    path = r'P:\Project\PoreTopology\04_IndustryZEO\07_AEL\01_IZA\101_3.3-6r'
    # path = r'P:\Project\PoreTopology\04_IndustryZEO\07_AEL\03_Deem\201_4.2-8r'
    # path = r'P:\Project\PoreTopology\04_IndustryZEO\07_AEL\03_Deem\301_5.0-10r'
    # path = r'P:\Project\PoreTopology\04_IndustryZEO\07_AEL\03_Deem\401_5.9-12r'
    
    
    threshold = 0.15
    outfile = open("%s/same_%s-2.csv"%(path, threshold), 'w')
    outfile.write('name,csqCheck,bondCheck,angleCheck,allCheck\n')


    adopath = r'%s\01_Ado'% path
    txtpath = r'%s\03_BondAngleTxT'% path
    
    adoFilepaths = ExtractInformation.GetFilenames(adopath, 'ado')
    for adoFilepath in adoFilepaths:
        # print(adoFilepath)
        filename = ExtractInformation.GetFilename(adoFilepath)
        
        ado = AdoFileDimension(adoFilepath)
        csq = GetPoreCsq(ado, csqlength = 10, unique = False)
        atom_csq = GetAtom_csq(ado)
        txtFilepath = "%s\%s.txt"%(txtpath, filename.replace(' ', ''))
        # print(txtFilepath)
        # print(os.path.join(txtFilepath, filename.replace(' ', '') + '.txt'))
        atoms, bonds, angles = GetCsq_Bond_Angle(txtFilepath, atom_csq)
        # print(atom_csq)
        if targetcsq == csq:
            # print("The two csqs are equal")
            # CompareByBond(target_atoms, target_bonds, target_angles, atoms, bonds, angles, threshold = 0.3)
            # target_bonds = {'1': 1, '2': 2, '3': 3}
            
            bondResult = CompareByBond(target_bonds, bonds, threshold = threshold)
            # print({"bondResult": bondResult})   
            angleResult = CompareByAngle(target_angles, angles, threshold = threshold)
            # print({"angleResult": angleResult})
        else:
            # print("The two csqs are not equal")
            pass
        outfile.write('%s,%s,%s,%s,%s\n'%(filename, str(targetcsq == csq), str(bondResult), str(angleResult), str((targetcsq == csq) and bondResult and angleResult)))
        print('%s,%s,%s,%s,%s'%(filename, str(targetcsq == csq), str(bondResult), str(angleResult), str((targetcsq) == csq and bondResult and angleResult)))
        # break
                
        # break
        # outfile.write('name,csqCheck,bondCheck,angleCheck\n')
    
    
            
            
    
    # ado = AdoFileDimension('AEI-PPT 1.ado')
    # csq = GetPoreCsq(ado, csqlength = 10, unique = False)
    # atom_csq = GetAtom_csq(ado)
    # atoms, bonds, angles = GetCsq_Bond_Angle(r'AEI-PPT 1.txt', atom_csq)
    
    # if targetcsq == csq:
    #     # print("The two csqs are equal")
    #     # CompareByBond(target_atoms, target_bonds, target_angles, atoms, bonds, angles, threshold = 0.3)
    #     # target_bonds = {'1': 1, '2': 2, '3': 3}
        
    #     bondResult = CompareByBond(target_bonds, bonds, threshold = 0.3)
    #     print({"bondResult": bondResult})   
    #     angleResult = CompareByAngle(target_angles, angles, threshold = 0.1)
    #     print({"angleResult": angleResult})
    # else:
    #     print("The two csqs are not equal")
    
def main_AEL():
    def Compare180(angles1, angles2):
        for angle1 in angles1:
            if angle1.degree != 180:
                print(f"Angle not 180")
                return False
        for angle2 in angles2:
            if angle2.degree != 180:
                print(f"Angle not 180")
                return False
        return True
    

    # targetAdo = AdoFileDimension(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\AEL\Ado_Manual\AEL-PPT 1_10.ado')
    targetAdo = AdoFileDimension(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\AFI\Ado_Manual\AFI-PPT 1_10.ado')
    targetcsq = GetPoreCsq(targetAdo, csqlength = 10, unique = False)
    target_atom_csq = GetAtom_csq(targetAdo)
    # print(target_atom_csq)
    # P:\Project\PoreTopology\04_IndustryZEO\04_=MFI\01_IZA\101_3.3-6r\03_BondAngleTxT
    target_atoms, target_bonds, target_angles = GetCsq_Bond_Angle(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\AFI\txt_bondAngle\AFI-PPT 1_10.txt', target_atom_csq)
    # target_atoms, target_bonds, target_angles = GetCsq_Bond_Angle(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\AFI\txt_bondAngle\AFI-PPT 1_10.txt', target_atom_csq)

    # path = r'P:\Project\PoreTopology\04_IndustryZEO\05_MFI\01_IZA\301_5.0-10r'
    # path = r'P:\Project\PoreTopology\04_IndustryZEO\04_=MFI\02_ABC6\201_4.2-8r'
    
    # path = r'P:\Project\PoreTopology\04_IndustryZEO\08_AFI\03_Deem\101_3.3-6r'
    # path = r'P:\Project\PoreTopology\04_IndustryZEO\08_AFI\03_Deem\201_4.2-8r'
    path = r'P:\Project\PoreTopology\04_IndustryZEO\08_AFI\03_Deem\301_5.0-10r'
    # path = r'P:\Project\PoreTopology\04_IndustryZEO\08_AFI\03_Deem\401_5.9-12r'
    
    threshold = 0.15
    outfile = open("%s/same_%s-2.csv"%(path, threshold), 'w')
    outfile.write('name,csqCheck,bondCheck,angleCheck,allCheck\n')

    adopath = r'%s\01_Ado'% path
    txtpath = r'%s\03_BondAngleTxT'% path
    
    adoFilepaths = ExtractInformation.GetFilenames(adopath, 'ado')
    for adoFilepath in adoFilepaths:
        # print(adoFilepath)
        filename = ExtractInformation.GetFilename(adoFilepath)
        
        ado = AdoFileDimension(adoFilepath)
        csq = GetPoreCsq(ado, csqlength = 10, unique = False)
        atom_csq = GetAtom_csq(ado)
        txtFilepath = "%s\%s.txt"%(txtpath, filename.replace(' ', ''))
        atoms, bonds, angles = GetCsq_Bond_Angle(txtFilepath, atom_csq)
    
        if targetcsq == csq:
            bondResult = "NA"
            angleResult = Compare180(target_angles, angles)

        else:
            # print("The two csqs are not equal")
            bondResult = False
            angleResult = False
            pass
        outfile.write('%s,%s,%s,%s,%s\n'%(filename, str(targetcsq == csq), str(bondResult), str(angleResult), str((targetcsq == csq) and bondResult and angleResult)))
        print('%s,%s,%s,%s,%s'%(filename, str(targetcsq == csq), str(bondResult), str(angleResult), str((targetcsq) == csq and bondResult and angleResult)))
        # break


if __name__ == '__main__':
    print()
    print("########################################")
    print("#                 GetCsq&Bond&Angel V1.0")
    print("#                            2022-May-19")
    print("#                           by wangjiaze")
    print("########################################")
    print()

    # main_Deem_AFI()
    # main_ABC6_AEL()
    
    # main_IZA()
    main_AEL()
    
    