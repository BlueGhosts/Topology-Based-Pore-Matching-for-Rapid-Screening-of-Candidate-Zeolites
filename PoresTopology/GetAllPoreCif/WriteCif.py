# python WriteCif V1.0
# by wangjiaze on 2022-May-17
import os
import sys
sys.path.append(r'D:\Work\Programs\Normal')
import CoordinateTransformation as CoorTrans


def WriteCif(crystal, outFilepath):
    file = open(outFilepath, 'w')
    form = "{0:<35}\t{1:<20}\n"

    file.write('data_%s\n'%(crystal.name))
    file.write(form.format('_audit_creation_method','Write2Cif'))
    file.write(form.format('_symmetry_space_group_name_H-M', crystal.spaceGroup))
    file.write(form.format('_symmetry_Int_Tables_number', str(crystal.groupNumber)))
    file.write(form.format('_symmetry_cell_setting', crystal.crystalSystem))
    file.write(form.format('_cell_length_a', crystal.a))
    file.write(form.format('_cell_length_b', crystal.b))
    file.write(form.format('_cell_length_c', crystal.c))
    file.write(form.format('_cell_angle_alpha', crystal.alpha))
    file.write(form.format('_cell_angle_beta', crystal.beta))
    file.write(form.format('_cell_angle_gamma', crystal.gamma))

    file.write('loop_\n')
    file.write('_symmetry_equiv_pos_as_xyz\n')
    for symmetryEquivPosAsXyz in crystal.symmetryEquivPosAsXyzs:
        file.write(symmetryEquivPosAsXyz + '\n')

    formAtom = "{0:<10}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\n"
    file.write('loop_\n')
    file.write('_atom_site_label\n')
    file.write('_atom_site_type_symbol\n')
    file.write('_atom_site_fract_x\n')
    file.write('_atom_site_fract_y\n')
    file.write('_atom_site_fract_z\n')
    for atom in crystal.atoms:
        atomElement = atom.element
        coordinate = atom.coordinate
        file.write(formAtom.format(atom.name, atomElement, coordinate[0], coordinate[1], coordinate[2]))

    formBond = "{0:<5}\t{1:<5}\t{2:<10}\t{3:<5}\t{4:<3}\n"
    file.write('loop_\n')
    file.write('_geom_bond_atom_site_label_1\n')
    file.write('_geom_bond_atom_site_label_2\n')
    file.write('_geom_bond_distance\n')
    file.write('_geom_bond_site_symmetry_2\n')
    file.write('_ccdc_geom_bond_type\n')
    for bond in crystal.bonds:
        setSymmetry = '%s_%s%s%s'%(bond.setSymmetry[0], bond.setSymmetry[1], bond.setSymmetry[2], bond.setSymmetry[3])
        file.write(formBond.format(bond.atom1.name, bond.atom2.name, bond.distance, setSymmetry, bond.type))
    file.close()
    return os.path.abspath(outFilepath).replace('\\', '/')


if __name__ == "__main__":
    print("####################")
    print("#      WriteCif v1.0")
    print("#        2022-May-17")
    print("#       by wangjiaze")
    print("####################")
    print()

    import sys
    if len(sys.argv) > 1:
        crystal = sys.argv[1]
        outFilepath = sys.argv[2]
        WriteCif(crystal, outFilepath)

    '''
    import sys
    sys.path.append(r'D:\Work\Programs\Structure')
    from CifFile.CifFile import CifFile
    crystal = CifFile('AFR-PPT1.cif', software = 'ToposPro').cif2Crystal()
    outFilepath = 'outTest.cif'
    WriteCif(crystal, outFilepath)
    '''



