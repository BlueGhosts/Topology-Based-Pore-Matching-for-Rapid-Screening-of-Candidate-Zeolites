# AdoFile V1.0
# V1.0 by wangjiaze on 2022-May-16

import re

class AdoFile():
    def __init__(self, filepath):

        self.fileName = filepath.split('\\')[-1].split('/')[-1].split('.')[0]

        file = open(filepath)

        self.content = file.read()
        self.lines = self.content.split('\n')

        self.name = self.lines[1].strip().split(':')[-1]
        self.atomNames = self.GetAtoms()
        self.nodesNumber = len(self.atomNames)
        self.TD10 = self.GetTD10()
        self.transitivity = self.GetTransitivity()
        self.essentialRings = self.GetEssentialRings()
        self.ringsInFramework = self.GetRingsFromEssentialRings(self.essentialRings)
        self.tiling = self.GetTiling()
        self.tilings = self.GetTilings()

        self.atom_csq = self.GetAtom_Csq(self.content)
        self.atom_csqByFramework = self.GetAtom_CsqByFramework()
        self.TD10sByFramework = self.GetTD10ByFramework()
        self.csqs = list(self.atom_csq.values())

        self.NTname = self.GetNTname()



    def GetAtoms(self):
        Atoms = re.findall('\n----------------------\n(.*):', self.content)
        return Atoms

    def GetTD10(self):
        match = re.search('TD10=(\d+)', self.content)
        if match:
            TD10 = match.group(1)
            return TD10
        else:
            return False

    def GetTiling(self):
        tiling = re.search('Tiling: (.+) =', self.content)
        if tiling:
            tiling = tiling.group(1)
        else:
            tiling = False
        return tiling

    def GetTilings(self):
        if self.tiling:
            tilings = re.findall('\[.*?\]', self.tiling)
        else:
            tilings = False
        return tilings

    def GetTransitivity(self):
        Transitivity = False
        for i in range(len(self.lines)):
            line = self.lines[i]
            if 'All proper tilings' in line:
                i = i + 5
                line = self.lines[i]
                Transitivity = line.split('|')[2].strip()
                break
        return Transitivity

    def isNT(self):
        isNaturalTiling = False
        for i in range(len(self.lines)):
            line = self.lines[i]
            if 'All proper tilings' in line:
                i = i + 5
                line = self.lines[i]
                if 'NT' in line.split('|')[0]:
                    isNaturalTiling = True
                break
        return isNaturalTiling

    def GetNTname(self):
        NTname = 'N/A'
        for i in range(len(self.lines)):
            line = self.lines[i]
            if 'All proper tilings' in line:
                i = i + 5
                line = self.lines[i]
                if 'NT' in line.split('|')[0]:
                    NTname = "%s-%s"%(self.name, line.split('|')[0].strip())
                    if 'PPT' in NTname:
                        NTname = NTname.split('/NT')[0]
                break
        return NTname

    def GetEssentialRings(self):
        EssentialRings = False
        for i in range(len(self.lines)):
            line = self.lines[i]
            if 'All proper tilings' in line:
                i = i + 5
                line = self.lines[i]
                EssentialRings = line.split('|')[1].strip()
                break
        return EssentialRings

    def GetRingsFromEssentialRings(self, EssentialRings):
        if EssentialRings == False:
            AllRings = ['False']
        else:
            AllRings = []
            rings = re.findall('\d+', EssentialRings)
            # print(rings)
            for ring in rings:
                if ring not in AllRings:
                    AllRings.append(ring)
        return AllRings

    def GetAtom_CsqByFramework(self):
        atom_csqs = []
        informations = self.content.split('TD')[:-1]
        for information in informations:
            atom_csq = self.GetAtom_Csq(information.split('Coordination sequences')[-1])
            atom_csqs.append(atom_csq)
        return atom_csqs

    def GetTD10ByFramework(self):
        TD10s = re.findall('TD10=(\d+)', self.content)
        return TD10s

    def GetAtom_Csq(self, content):
        atom_csq = {}
        csqInformations = re.findall('.+:.+\nNum.+\nCum.+', content)
        for csqInformation in csqInformations:
            lines = csqInformation.split('\n')
            atomName = lines[0].split(':')[0]
            csq = [ int(csqNumber) for csqNumber in lines[1].split()[1:] ]
            atom_csq[atomName] = csq
        return atom_csq


if __name__ == '__main__':
    print()
    print("####################")
    print("        AdoFile V1.0")
    print("         2022-May-16")
    print("        by wangjiaze")
    print("####################")
    print()

    # adoFilepath = r'AET-PPT 1.ado'
    adoFilepath = r'example2.ado'
    AdoFile(adoFilepath)
