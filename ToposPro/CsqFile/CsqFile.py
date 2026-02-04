# CsqFile V1.0
# by wangjiaze on 2022-May-20

class CsqFile():
    def __init__(self, filepath):
        self.fileName = filepath.split('\\')[-1].split('/')[-1].split('.')[0]

        file = open(filepath)

        self.content = file.read()
        self.lines = self.content.split('\n')
        self.name = self.lines[1].strip().split(':')[-1]

        self.nodeNumber = int(self.lines[2].strip().split()[0])
        self.layerNumber = int(self.lines[2].strip().split()[1])

        self.atom_csq = self.GetAtom_csq()
        self.csqs = list(self.atom_csq.values())

    def GetAtom_csq(self):
        atom_csq = {}
        for line in self.lines[3:]:
            if not line:
                continue
            line = line.split()
            atom = line[0].strip()
            csq = [ int(i) for i in line[1:]]
            atom_csq[atom] = csq
        return atom_csq


if __name__ == '__main__':
    print()
    print("####################")
    print("#       CsqFile V1.0")
    print("#        2022-May-20")
    print("#       by wangjiaze")
    print("####################")
    print()

    csqFilepath = r'AWW.csq'
    # adoFilepath = r'example2.ado'
    CsqFile(csqFilepath)
