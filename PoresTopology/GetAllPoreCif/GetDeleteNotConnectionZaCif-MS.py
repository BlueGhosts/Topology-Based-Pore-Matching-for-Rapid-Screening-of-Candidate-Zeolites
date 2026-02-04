# python GetDeleteNotConnectionZaCif V1.0
# by wangjiaze on 2024-Feb-24

import os
import sys
sys.path.append(r'..\..\ToposPro')

from AdoFile.AdoFile import AdoFile
from Structure.CifFile.CifFile import CifFile
from WriteCif import WriteCif

def GetAdoInformation(adoFile):
    ado = AdoFile(adoFile)
    name = ado.fileName
    try:
        # print('\r  ' + name, end='')
        TD10s = ado.TD10sByFramework
        csqByFrameworks = ado.atom_csqByFramework
        return name, TD10s, csqByFrameworks
    except:
        return name, False, [['False']]
    
def GetDeleteNotConnectionZaCif(adoPath, cifPath, outCifPath):
    adoFiles = []
    cifFiles = []
    for filename in os.listdir(adoPath):
        if filename.endswith(".ado"):
            adoFiles.append(os.path.join(adoPath, filename))
            cifFiles.append(os.path.join(cifPath, filename.replace('.ado', '.cif').replace(' ', '')))
            
            
    for adoFile in adoFiles[:]:
        name, TD10s, csqByFrameworks = GetAdoInformation(adoFile)
        cifPath = cifFiles[adoFiles.index(adoFile)]
        # print(cifPath)
        cifFile = CifFile(cifPath, software='MS')
        atoms = cifFile.atoms.copy()

        print(f'Processing {name} {cifFile.name}')
        if len(TD10s) == 0:
            poreAtoms = [atom for atom in atoms if atom.element == 'O']
            poreAtoms += [atom for atom in atoms if atom.element == 'Si']
            # poreBonds = [bond for bond in cifFile.bonds if bond.atom1.element == 'O' or bond.atom2.element == 'O']
            # poreBonds += [bond for bond in cifFile.bonds if bond.atom1.element == 'Si' or bond.atom2.element == 'Si']

        if len(TD10s) > 0:
            poreAtoms = [atom for atom in atoms if atom.element == 'O']
            poreAtoms += [atom for atom in atoms if atom.element == 'Si']      
            for order in range(len(TD10s)):
                poreAtoms += [atom for atom in atoms if atom.name in csqByFrameworks[order].keys()]

                # poreBonds = [bond for bond in cifFile.bonds if bond.atom1.element == 'O' or bond.atom2.element == 'O']
                # poreBonds += [bond for bond in cifFile.bonds if bond.atom1.element == 'Si' or bond.atom2.element == 'Si']
                # poreBonds += [bond for bond in cifFile.bonds if bond.atom1.name in csqByFrameworks[order].keys() or bond.atom2.name in csqByFrameworks[order].keys()]  
        # print(f'poreAtoms: {atoms}')
        # print(cifFile.symmetryEquivPosAsXyzs)
        cifFile.atoms = poreAtoms
        crystal = cifFile.cif2Crystal()


        outCifFilepath = f'{outCifPath}/{name}.cif'
        WriteCif(crystal, outCifFilepath)
        # break
    pass


if __name__ == "__main__":
    print("############################")
    print("#        Get_TD10_Csq V1.1 #")
    print("#              2024-Dec-04 #")
    print("#             by wangjiaze #")
    print("############################")
    print()

    # adoPath = r'TestAdo'
    # cifPath = r'TestCif'
    # outCifPath = r'Test_out'
    
    # adoPath = r'P:\Project\PoreTopology\02_ABC6\02_Process\03_PoreTopology\01_#Ado\02_2-16_layers_NT'
    # cifPath = r'P:\Project\PoreTopology\02_ABC6\02_Process\03_PoreTopology\02_#Cif\03_2-16_layers-NT-2MS'
    # outCifPath = r'P:\Project\PoreTopology\02_ABC6\02_Process\03_PoreTopology\02_#Cif\04_2-16_layers-NT-2MS-DNC'


    import sys
    if len(sys.argv) > 1:
        adoPath = sys.argv[1]
        cifPath = sys.argv[2]
        outCifPath = sys.argv[3]
        GetDeleteNotConnectionZaCif(adoPath, cifPath, outCifPath)
    else:

        adoPath = input('Input Ado Files Folder Path:\n')
        cifPath = input('Input Cif Files Folder Path\n')
        outCifPath = input('Output Cif Files Folder Path\n')

        GetDeleteNotConnectionZaCif(adoPath, cifPath, outCifPath)
        input('Press any key to Finish.')


