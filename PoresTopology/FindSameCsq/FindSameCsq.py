# FindSameCsq V1.0
# by wangjiaze on 2025-Mar-03

import os
import sys
import re
sys.path.append(r'../../lib')
sys.path.append(r'../../ToposPro')
# sys.path.append(r'D:\Work\Programs\software\ToposPro')

import ExtractInformation
from AdoFile.AdoFile import AdoFile
from CoordinationSequence.CoordinationSequence import CoordinationSequence as Csq


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


def FindSameCsq(targetAdopath, checkAdoDirpath, outCsvpath, csqlength = 10):
    targetAdo = AdoFileDimension(targetAdopath)
    targetcsq = GetPoreCsq(targetAdo, csqlength, unique = False)
    print(targetcsq)  
    
    # targetAdo = AdoFile(targetAdopath)
    # targetAtom_csq = targetAdo.atom_csqByFramework
    # # targetcsq = Csq(targetAdo.csqs, unique = False)
    # targetcsq = Csq([ csq[:csqlength] for csq in targetAdo.csqs], unique = False)
    # # print(targetcsq)
    # print(targetAdo.name, targetcsq)
    sameAdoNames = []
    for adoFilepath in ExtractInformation.GetFilenames(checkAdoDirpath, 'ado'):
        ado = AdoFileDimension(adoFilepath)
        print(f"Calculating {ado.name}", end = '\r')
        csqs = GetPoreCsq(ado, csqlength, unique = False)
        # print(csqs)
        if targetcsq == csqs:
            sameAdoNames.append(ado.name)
    print("Calculate Done!      ")
            
    print("Same Number:", len(sameAdoNames))
    # with open(outCsvpath, 'w') as file:
    #     file.write('name\n')
    #     for sameAdoName in sameAdoNames:
    #         file.write(f"{sameAdoName}\n")
            
    # print(sameAdoNames)
    
    return sameAdoNames

def main_IZA():
    # CHA, LTA
    
    # name = "AEL"
    # filename = "%s-PPT 1"%name
    
    # targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\%s\Ado_Manual\%s_6.ado'%(name, filename)
    # # checkAdoDirpath = r'P:\Project\PoreTopology\02_ABC6\02_Process\03_PoreTopology\01_#Ado\02_2-16_layers_NT'
    # checkAdoDirpath_Deem = r'P:\Project\PoreTopology\03_Deem\02_Process\03_PoreTopology\01_#Ado\02_Deem-NT'
    # outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\%s\=%s_6_Deem-NT.csv'%(name, name)
    # sameAdoNames = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    
    
    name = "AFI"
    filename = "%s-PPT 1"%name
    
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\%s\Ado_Manual\%s_6.ado'%(name, filename)
    # checkAdoDirpath = r'P:\Project\PoreTopology\02_ABC6\02_Process\03_PoreTopology\01_#Ado\02_2-16_layers_NT'
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology_Manual\01_Ado\100_6-rings-Manual_Ado-NT'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\%s\=%s_6_IZA_6-NT.csv'%(name, name)
    sameAdoNames_6 = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_6:
            file.write(f"{sameAdoName}\n")
    
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\%s\Ado_Manual\%s_8.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology_Manual\01_Ado\200_8-rings-Manual_Ado-NT'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\%s\=%s_8_IZA_8-NT.csv'%(name, name)
    sameAdoNames_8 = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_8:
            if sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
            
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\%s\Ado_Manual\%s_10.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology_Manual\01_Ado\300_10-rings-Manual_Ado-NT'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\%s\=%s_10_IZA_10-NT.csv'%(name, name)
    sameAdoNames_10 = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_10:
            if sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
    
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\%s\Ado_Manual\%s_12.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology_Manual\01_Ado\400_12-rings-Manual_Ado-NT'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\%s\=%s_12_IZA_12-NT.csv'%(name, name)
    sameAdoNames_12 = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_12:
            if sameAdoName in sameAdoNames_10 and sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
    
    # checkAdoDirpath_ABC6 = r'P:\Project\PoreTopology\03_Deem\02_Process\03_PoreTopology\01_#Ado\02_Deem-NT'
    # outCsvpath = r'P:\Project\PoreTopology\03_IndustryZEO\=CHA(LTA)_6_Deem-NT.csv'
    # sameAdoNames = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    
    pass


def main_Deem():
    # CHA, LTA
    
    # name = "AEL"
    # filename = "%s-PPT 1"%name
    
    # name = "CHA"
    # filename = "%s-PPT 1"%name
    # with open(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_Deem-NT.csv'%(name, name), 'r') as file:
    #     lines = file.readlines()
    #     sameAdoNames_6 = [line.strip().split('/')[0] for line in lines[1:]]
    # print("Same Number 6:", len(sameAdoNames_6))
    # print(sameAdoNames_6)



    ###    
    name = "FAU"
    filename = "%s-PPT 1"%name
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_6.ado'%(name, filename)
    # checkAdoDirpath = r'P:\Project\PoreTopology\02_ABC6\02_Process\03_PoreTopology\01_#Ado\02_2-16_layers_NT'
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\03_Deem\02_Process\03_PoreTopology\01_#Ado\02_Deem-NT'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_Deem-NT.csv'%(name, name)
    sameAdoNames_6 = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_Deem-NT-250529.csv'%(name, name), 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_6:
            if sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
    print("Same Number 6:", len(sameAdoNames_6))
    # print(sameAdoNames_6)
    # return
    

    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_8.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\21_Deem\02_Process\01_#Ado\%s\202_PoreTopology-4.2-8r-NT'%name
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_8_Deem_8-NT-250529.csv'%(name, name)
    sameAdoNames_8_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_8 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_8_ori:
            # sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_8.append(sameAdoName)
    # print(sameAdoNames_8_ori)
    print("Same Number 8:", len(sameAdoNames_8))
            
            
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_10.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\21_Deem\02_Process\01_#Ado\%s\302_PoreTopology-5.0-10r-NT'%name
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_10_Deem_10-NT-250529.csv'%(name, name)
    sameAdoNames_10_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_10 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_10_ori:
            # sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_10.append(sameAdoName)
    print("Same Number 10:", len(sameAdoNames_10))
    
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_12.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\21_Deem\02_Process\01_#Ado\%s\401_PoreTopology-5.9-12r-NT'%name
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_12_Deem_12-NT-250529.csv'%(name, name)
    sameAdoNames_12_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_12 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_12_ori:
            # sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_10 and sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_12.append(sameAdoName)
    print("Same Number 12:", len(sameAdoNames_12))
    
    
def main_Deem_AEL_Straight():
    name = "AEL"
    filename = "%s-PPT 1"%name
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_Deem-NT_Straight.csv'%(name, name), 'r') as file:
        lines = file.readlines()
        sameAdoNames_6 = [line.strip().split(',')[0] for line in lines[1:]]
    print("Same Number 6:", len(sameAdoNames_6))

    
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\02_#Cif\AEL\203_PoreTopology-4.2-8r-NT-MS-ANGLE-Straight.csv', 'r') as file:
        lines = file.readlines()
        sameAdoNames_8_Straight = [line.strip().split(',')[0] for line in lines[1:]]
    
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_8.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\01_#Ado\%s\202_PoreTopology-4.2-8r-NT'%name
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_8_Deem_8-NT.csv'%(name, name)
    sameAdoNames_8_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_8 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_8_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_6 and sameAdoName in sameAdoNames_8_Straight:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_8.append(sameAdoName)
 
    # print(sameAdoNames_8)
    # input()
    # print(sameAdoNames_8_ori)
    # input()
    # print(sameAdoNames_8_Straight)
    print("Same Number 8:", len(sameAdoNames_8))
    

         
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\02_#Cif\AEL\303_PoreTopology-5.0-10r-NT-MS-ANGLE-Straight.csv', 'r') as file:
        lines = file.readlines()
        sameAdoNames_10_Straight = [line.strip().split(',')[0] for line in lines[1:]]
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_10.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\01_#Ado\%s\302_PoreTopology-5.0-10r-NT'%name
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_10_Deem_10-NT.csv'%(name, name)
    sameAdoNames_10_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_10 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_10_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_6 and sameAdoName in sameAdoNames_8:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_10.append(sameAdoName)
 
    print("Same Number 10:", len(sameAdoNames_10))
    
    
    
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\02_#Cif\AEL\403_PoreTopology-5.9-12r-NT-MS-ANGLE-Straight.csv', 'r') as file:
        lines = file.readlines()
        sameAdoNames_12_Straight = [line.strip().split(',')[0] for line in lines[1:]]

    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_12.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\01_#Ado\%s\401_PoreTopology-5.9-12r-NT'%name
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_12_Deem_12-NT.csv'%(name, name)
    sameAdoNames_12_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_12 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_12_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_10 and sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_12.append(sameAdoName)
    print("Same Number 12:", len(sameAdoNames_12))


def main_Deem_AFI_Straight():
    name = "AFI"
    filename = "%s-PPT 1"%name
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_Deem-NT_Straight.csv'%(name, name), 'r') as file:
        lines = file.readlines()
        sameAdoNames_6 = [line.strip().split(',')[0] for line in lines[1:]]
    print("Same Number 6:", len(sameAdoNames_6))

    
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\02_#Cif\AEL\203_PoreTopology-4.2-8r-NT-MS-ANGLE-Straight.csv', 'r') as file:
        lines = file.readlines()
        sameAdoNames_8_Straight = [line.strip().split(',')[0] for line in lines[1:]]
    
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_8.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\01_#Ado\AEL\202_PoreTopology-4.2-8r-NT'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_8_Deem_8-NT.csv'%(name, name)
    sameAdoNames_8_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_8 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_8_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_6 and sameAdoName in sameAdoNames_8_Straight:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_8.append(sameAdoName)
 
    # print(sameAdoNames_8)
    # input()
    # print(sameAdoNames_8_ori)
    # input()
    # print(sameAdoNames_8_Straight)
    print("Same Number 8:", len(sameAdoNames_8))
    

         
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\02_#Cif\AEL\303_PoreTopology-5.0-10r-NT-MS-ANGLE-Straight.csv', 'r') as file:
        lines = file.readlines()
        sameAdoNames_10_Straight = [line.strip().split(',')[0] for line in lines[1:]]
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_10.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\01_#Ado\AEL\302_PoreTopology-5.0-10r-NT'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_10_Deem_10-NT.csv'%(name, name)
    sameAdoNames_10_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_10 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_10_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_6 and sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_10_Straight:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_10.append(sameAdoName)
 
    print("Same Number 10:", len(sameAdoNames_10))
    
    
    
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\02_#Cif\AEL\403_PoreTopology-5.9-12r-NT-MS-ANGLE-Straight.csv', 'r') as file:
        lines = file.readlines()
        sameAdoNames_12_Straight = [line.strip().split(',')[0] for line in lines[1:]]

    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_12.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\01_#Ado\AEL\401_PoreTopology-5.9-12r-NT'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_12_Deem_12-NT.csv'%(name, name)
    sameAdoNames_12_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_12 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_12_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_10 and sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_12.append(sameAdoName)
    print("Same Number 12:", len(sameAdoNames_12))
    
    
def main_Deem_AEL():
    name = "AEL"
    filename = "%s-PPT 1"%name
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_Deem-NT_Straight.csv'%(name, name), 'r') as file:
        lines = file.readlines()
        sameAdoNames_6 = [line.strip().split(',')[0] for line in lines[1:]]
    print("Same Number 6:", len(sameAdoNames_6))

    
    # name = "AFI"
    # filename = "%s-PPT 1"%name
    
    # name = "CHA"
    # filename = "%s-PPT 1"%name
    # targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_6.ado'%(name, filename)
    # # checkAdoDirpath = r'P:\Project\PoreTopology\02_ABC6\02_Process\03_PoreTopology\01_#Ado\02_2-16_layers_NT'
    # checkAdoDirpath_Deem = r'P:\Project\PoreTopology\03_Deem\02_Process\03_PoreTopology\01_#Ado\02_Deem-NT'
    # outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\%s\=%s_6_Deem-NT.csv'%(name, name)
    # sameAdoNames_6 = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_Deem-NT_all_250527.csv'%(name, name), 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_6:
            if sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                

    print("Same Number 6:", len(sameAdoNames_6))
    print(sameAdoNames_6)



    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_8.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\21_Deem\02_Process\01_#Ado\%s\202_PoreTopology-4.2-8r-NT'%name
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_8_Deem_8-NT_Straight_250527.csv'%(name, name)
    sameAdoNames_8_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_8 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_8_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_8.append(sameAdoName)
 
    print("Same Number 8:", len(sameAdoNames_8))
            
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_10.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\21_Deem\02_Process\01_#Ado\%s\302_PoreTopology-5.0-10r-NT'%name
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_10_Deem_10-NT_all_250527.csv'%(name, name)
    sameAdoNames_10_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_10 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_10_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_10.append(sameAdoName)
    print("Same Number 10:", len(sameAdoNames_10))
    
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_12.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\21_Deem\02_Process\01_#Ado\%s\401_PoreTopology-5.9-12r-NT'%name
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_12_Deem_12-NT_all_250527.csv'%(name, name)
    sameAdoNames_12_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_12 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_12_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_10 and sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_12.append(sameAdoName)
    print("Same Number 12:", len(sameAdoNames_12))
    
   
def main_Deem_AFI():
    name = "AEL"
    filename = "%s-PPT 1"%name
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_Deem-NT_Straight.csv'%(name, name), 'r') as file:
        lines = file.readlines()
        sameAdoNames_6 = [line.strip().split(',')[0] for line in lines[1:]]
    print("Same Number 6:", len(sameAdoNames_6))


    # name = "AFI"
    # filename = "%s-PPT 1"%name

    # name = "CHA"
    # filename = "%s-PPT 1"%name
    # targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_6.ado'%(name, filename)
    # # checkAdoDirpath = r'P:\Project\PoreTopology\02_ABC6\02_Process\03_PoreTopology\01_#Ado\02_2-16_layers_NT'
    # checkAdoDirpath_Deem = r'P:\Project\PoreTopology\03_Deem\02_Process\03_PoreTopology\01_#Ado\02_Deem-NT'
    # outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\%s\=%s_6_Deem-NT.csv'%(name, name)
    # sameAdoNames_6 = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    
    name = "AFI"
    filename = "%s-PPT 1"%name

    with open(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_Deem-NT_all_250527.csv'%(name, name), 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_6:
            if sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                

    print("Same Number 6:", len(sameAdoNames_6))
    print(sameAdoNames_6)



    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_8.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\21_Deem\02_Process\01_#Ado\%s\202_PoreTopology-4.2-8r-NT'%"AEL"
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_8_Deem_8-NT_Straight_250527.csv'%(name, name)
    sameAdoNames_8_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_8 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_8_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_8.append(sameAdoName)

    print("Same Number 8:", len(sameAdoNames_8))
            
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_10.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\21_Deem\02_Process\01_#Ado\%s\302_PoreTopology-5.0-10r-NT'%"AEL"
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_10_Deem_10-NT_all_250527.csv'%(name, name)
    sameAdoNames_10_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_10 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_10_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_10.append(sameAdoName)
    print("Same Number 10:", len(sameAdoNames_10))

    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_12.ado'%(name, filename)
    checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\21_Deem\02_Process\01_#Ado\%s\401_PoreTopology-5.9-12r-NT'%"AEL"
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_12_Deem_12-NT_all_250527.csv'%(name, name)
    sameAdoNames_12_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_12 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_12_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_10 and sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_12.append(sameAdoName)
    print("Same Number 12:", len(sameAdoNames_12))
    
     
def main_ABC6():
    # CHA, LTA
    
    # name = "AEL"
    # filename = "%s-PPT 1"%name
    name = "MOR"
    filename = "%s-PPT 1"%name
    # with open(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_Deem-NT.csv'%(name, name), 'r') as file:
    #     lines = file.readlines()
    #     sameAdoNames_6 = [line.strip().split('/')[0] for line in lines[1:]]
    # print("Same Number 6:", len(sameAdoNames_6))
    
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_6.ado'%(name, filename)
    # checkAdoDirpath = r'P:\Project\PoreTopology\02_ABC6\02_Process\03_PoreTopology\01_#Ado\02_2-16_layers_NT'
    checkAdoDirpath_ABC6 = r'P:\Project\PoreTopology\02_ABC6\6-rings-3.3\02_Process\03_PoreTopology\01_#Ado\02_2-16_layers_NT'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_ABC6_6-NT.csv'%(name, name)
    sameAdoNames_6 = FindSameCsq(targetAdopath_6, checkAdoDirpath_ABC6, outCsvpath)
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_6:
            file.write(f"{sameAdoName}\n")


    
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_8.ado'%(name, filename)
    checkAdoDirpath_ABC6 = r'P:\Project\PoreTopology\02_ABC6\8-rings-4.2\02_Process\01_#Ado'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_8_ABC6_8-NT.csv'%(name, name)
    sameAdoNames_8_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_ABC6, outCsvpath)
    sameAdoNames_8 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_8_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_8.append(sameAdoName)
 
    print("Same Number 8:", len(sameAdoNames_8))
            
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_10.ado'%(name, filename)
    checkAdoDirpath_ABC6 = r'P:\Project\PoreTopology\02_ABC6\10-rings-5.0\02_Process\01_#Ado'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_10_ABC6_10-NT.csv'%(name, name)
    sameAdoNames_10_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_ABC6, outCsvpath)
    sameAdoNames_10 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_10_ori:
            sameAdoName = sameAdoName.split('/')[0]
            if sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_10.append(sameAdoName)
    print("Same Number 10:", len(sameAdoNames_10))
    
    # targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_12.ado'%(name, filename)
    # checkAdoDirpath_Deem = r'P:\Project\PoreTopology\04_IndustryZEO\02_Deem\02_Process\01_#Ado\%s\401_PoreTopology-5.9-12r-NT'%name
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_12_ABC6_12-NT.csv'%(name, name)
    # sameAdoNames_12_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_Deem, outCsvpath)
    sameAdoNames_12 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        # for sameAdoName in sameAdoNames_12_ori:
        #     sameAdoName = sameAdoName.split('/')[0]
        #     if sameAdoName in sameAdoNames_10 and sameAdoName in sameAdoNames_8 and sameAdoName in sameAdoNames_6:
        #         file.write(f"{sameAdoName}\n")
        #         sameAdoNames_12.append(sameAdoName)
    print("Same Number 12:", len(sameAdoNames_12))
 
 
def main_ABC6_AEL():
    
    name = "AFI"
    filename = "%s-PPT 1"%name
    with open(r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_Deem-NT_Straight.csv'%(name, name), 'r') as file:
        lines = file.readlines()
        sameAdoNames_6_Straight = [line.strip().split(',')[0] for line in lines[1:]]

    
    targetAdopath_6 = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\Ado_Manual\%s_6.ado'%(name, filename)
    # checkAdoDirpath = r'P:\Project\PoreTopology\02_ABC6\02_Process\03_PoreTopology\01_#Ado\02_2-16_layers_NT'
    checkAdoDirpath_ABC6 = r'P:\Project\PoreTopology\02_ABC6\6-rings-3.3\02_Process\03_PoreTopology\01_#Ado\02_2-16_layers_NT'
    outCsvpath = r'P:\Project\PoreTopology\04_IndustryZEO\01_IZA-7\%s\=%s_6_ABC6_6-NT_Straight.csv'%(name, name)
    sameAdoNames_6_ori = FindSameCsq(targetAdopath_6, checkAdoDirpath_ABC6, outCsvpath)
    sameAdoNames_6 = []
    with open(outCsvpath, 'w') as file:
        file.write('name\n')
        for sameAdoName in sameAdoNames_6_ori:
            if sameAdoName in sameAdoNames_6_Straight:
                file.write(f"{sameAdoName}\n")
                sameAdoNames_6.append(sameAdoName)
            # file.write(f"{sameAdoName}\n")
    print("Same Number 6:", len(sameAdoNames_6))



def FindPicIZA():
    def FindSameCsqIZA(targetAdopath, checkAdopath, csqlength = 10):
        targetAdo = AdoFileDimension(targetAdopath)
        checkAdo = AdoFileDimension(checkAdopath)
        targetcsq = GetPoreCsq(targetAdo, csqlength, unique = False)
        checkcsq = GetPoreCsq(checkAdo, csqlength, unique = False)
        
        if targetcsq == checkcsq:
            return True
        else:
            return False

    
    sixpath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology_Manual\01_Ado\100_6-rings-Manual_Ado-NT'
    eightpath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology_Manual\01_Ado\200_8-rings-Manual_Ado-NT'
    tenpath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology_Manual\01_Ado\300_10-rings-Manual_Ado-NT'
    twelvepath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology_Manual\01_Ado\400_12-rings-Manual_Ado-NT'
    
    filepaths = ExtractInformation.GetFilenames(sixpath, 'ado')
    
    for filepath in filepaths:
        filename = ExtractInformation.GetFilename(filepath)
        sixAdopath = "%s/%s.ado"%(sixpath, filename)
        eightAdopath = "%s/%s.ado"%(eightpath, filename)
        tenAdopath = "%s/%s.ado"%(tenpath, filename)
        twelveAdopath = "%s/%s.ado"%(twelvepath, filename)
        

        if not (os.path.exists(eightAdopath) and os.path.exists(tenAdopath) and os.path.exists(twelveAdopath)):
            print("File %s doesn't exists in all directories."%filename)
        
        if not(FindSameCsqIZA(sixAdopath, eightAdopath)) and not(FindSameCsqIZA(eightAdopath, tenAdopath)) and not(FindSameCsqIZA(tenAdopath, twelveAdopath)):
            print("File %s is not the same."%filename)
            
            print(GetPoreCsq(AdoFileDimension(sixAdopath), 10, unique = False))
            print(GetPoreCsq(AdoFileDimension(eightAdopath), 10, unique = False))
            print(GetPoreCsq(AdoFileDimension(tenAdopath), 10, unique = False))
            print(GetPoreCsq(AdoFileDimension(twelveAdopath), 10, unique = False))
            
        # print(not(FindSameCsqIZA(sixAdopath, eightAdopath)))

if __name__ == '__main__':
    print()
    print("########################################")
    print("#              FindSameCsq V1.0")
    print("#                            2022-May-19")
    print("#                           by wangjiaze")
    print("########################################")
    print()

    main_Deem()
    # main_Deem_AEL()
    # main_Deem_AFI()
    # main_ABC6_AEL()
    # FindPicIZA()
