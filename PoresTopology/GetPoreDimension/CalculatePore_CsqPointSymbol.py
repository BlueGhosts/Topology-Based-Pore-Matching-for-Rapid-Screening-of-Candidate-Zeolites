# CalculatePoreDimension V1.0
# by wangjiaze on 2025-Feb-21

import sys
sys.path.append(r'D:\Work\Programs\Normal')
sys.path.append(r'D:\Work\Programs\Software\ToposPro')
import re

import ExtractInformation
from AdoFile.AdoFile import AdoFile
  
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



if __name__ == '__main__':
    print()
    print("##############################")
    print("   CalculatePoreDimension V1.0")
    print("                   2025-Feb-21")
    print("                  by wangjiaze")
    print("##############################")
    print()

    # adoDirpath = r'TestAdo'
    # outFilepath = r'Test.csv'
    
    # adoDirpath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology\01_Ado\Intergrowths_NT'
    # outFilepath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology\01_Ado\Intergrowths_NT_PoreDimension.csv'   
     
    #adoDirpath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology\01_Ado\Table_NT'
    #outFilepath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology\01_Ado\Table_NT_PoreDimension_csq.csv'    
    if len(sys.argv) > 1:
        adoDirpath = sys.argv[1]
        outFilepath = sys.argv[2]
        CalculatePoreDimension(adoDirpath, outFilepath)
    else:
        adoDirpath = input('Input Ado Folder Path:\n')
        outFilepath = input('Output File Name:\n') + '.csv'
        CalculatePoreDimension(adoDirpath, outFilepath)
        input('Press any key to continue.')