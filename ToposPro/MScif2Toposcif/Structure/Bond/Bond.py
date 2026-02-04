# Bond V1.1
# Bond V1.1 by wangjiaze on 2025-Feb-27 Add Function __eq__
# Bond V1.0 by wangjiaze on 2022-May-17

class Bond:
    def __init__(self, name, atom1, atom2, type, distance, setSymmetry = []):
        self.name = name
        self.atom1 = atom1
        self.atom2 = atom2
        self.type = type
        self.distance = distance
        self.setSymmetry = setSymmetry

    def __eq__(self, other):
        if (abs(self.distance - other.distance) <= 0.002) and self.type == other.type:
            if (self.atom1.name == other.atom1.name and self.atom2.name == other.atom2.name) or \
            (self.atom1.name == other.atom2.name and self.atom2.name == other.atom1.name):  
                return True
        return False

if __name__ == '__main__':
    print()
    print("####################")
    print("#          Bond V1.1")
    print("#        2025-Feb-27")
    print("#       by wangjiaze")
    print("####################")
    print()

