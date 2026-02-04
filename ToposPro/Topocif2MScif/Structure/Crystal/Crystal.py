# python Crystal V1.0
# by wangjiaze on 2022-May-17

import sys
sys.path.append(r'..\..\Structure')
import Structure.CoordinateTransformation as CoorTrans

class Crystal:
    def __init__(self, name, groupNumber, cellParameter, symmetryEquivPosAsXyzs, atoms, bonds = []):
        self.name = name
        self.groupNumber = groupNumber
        self.spaceGroup = CoorTrans.Groupnum2Groupname(self.groupNumber)
        self.crystalSystem = CoorTrans.Groupnum2CrystalSystem(self.groupNumber)
        self.cellParameter = cellParameter

        if symmetryEquivPosAsXyzs:
            self.symmetryEquivPosAsXyzs = symmetryEquivPosAsXyzs
        else:
            self.symmetryEquivPosAsXyzs = CoorTrans.GetSymmetryEquivPosAsXyz(self.spaceGroup)

        self.a = cellParameter[0]
        self.b = cellParameter[1]
        self.c = cellParameter[2]
        self.alpha = cellParameter[3]
        self.beta = cellParameter[4]
        self.gamma = cellParameter[5]

        self.atoms = atoms
        self.uniqueAtoms = atoms
        self.bonds = bonds


if __name__ == '__main__':
    print()
    print("####################")
    print("#       Crystal V1.0")
    print("#        2022-May-17")
    print("#       by wangjiaze")
    print("####################")
    print()
