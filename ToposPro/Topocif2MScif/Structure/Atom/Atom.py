# Atom V1.0
# by wangjiaze on 2022-May-17

class Atom:
    def __init__(self, name, element, coordinate, cellParameter, position = [5, 5 ,5]):
        self.name = name
        self.element = element
        self.cellParameter = cellParameter
        self.position = position
        self.coordinate = coordinate

        self.x = self.coordinate[0]
        self.y = self.coordinate[1]
        self.z = self.coordinate[2]

        self.wyc = '?'
        self.multiplicity = '?'
        self.bonds = []
        self.attachAtoms = []

    def AddBond(self, bond):
        self.bonds.append(bond)
        if bond.atom1 != self:
            self.attachAtoms.append(bond.atom1)
        else:
            self.attachAtoms.append(bond.atom2)

    def GiveWyc(self, wyc):
        self.wyc = wyc

    def GiveCoordinationSequence(self, coordinationSequence):
        self.coordinationSequence = coordinationSequence

    def GetBondAttachAtom(self, bond):
        if bond.atom1 != self:
            return bond.atom1
        else:
            return bond.atom2


if __name__ == '__main__':
    print()
    print("####################")
    print("#          Atom V1.0")
    print("#        2022-May-17")
    print("#       by wangjiaze")
    print("####################")
    print()

