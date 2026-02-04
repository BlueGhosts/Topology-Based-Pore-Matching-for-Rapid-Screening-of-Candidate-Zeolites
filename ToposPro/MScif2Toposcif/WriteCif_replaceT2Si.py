# python WriteCif V1.0
# WriteCif V1.3 software = "ToposPro" _symmetry_equiv_pos_as_xyz by wangjiaze on 2025-Feb-25
# WriteCif V1.1 software = "ToposPro" by wangjiaze on 2025-Feb-23
# WriteCif V1.0 by wangjiaze on 2022-May-17
import os
import sys
import Structure.CoordinateTransformation as CoorTrans


def WriteCif(crystal, outFilepath, software = 'MaterialsStudio'):
    file = open(outFilepath, 'w')
    form = "{0:<35}\t{1:<20}\n"
    
    file.write('data_%s\n'%(crystal.name))
    
    if software == 'MaterialsStudio' or software.upper() == "MS":
        file.write(form.format('_audit_creation_method','Write2Cif_MS'))
    elif software == 'ToposPro' or software == 'Topos':
        file.write(form.format('_audit_creation_method','Write2Cif_ToposPro'))
        
    file.write(form.format('_symmetry_space_group_name_H-M', crystal.spaceGroup))
    file.write(form.format('_symmetry_Int_Tables_number', str(crystal.groupNumber)))
    file.write(form.format('_symmetry_cell_setting', crystal.crystalSystem))
    file.write(form.format('_cell_length_a', crystal.a))
    file.write(form.format('_cell_length_b', crystal.b))
    file.write(form.format('_cell_length_c', crystal.c))
    file.write(form.format('_cell_angle_alpha', crystal.alpha))
    file.write(form.format('_cell_angle_beta', crystal.beta))
    file.write(form.format('_cell_angle_gamma', crystal.gamma))

    if software == 'MaterialsStudio' or software.upper() == "MS":
        file.write('loop_\n')
        file.write('_symmetry_equiv_pos_as_xyz\n')
        for symmetryEquivPosAsXyz in crystal.symmetryEquivPosAsXyzs:
            file.write(symmetryEquivPosAsXyz + '\n')
    elif software == 'ToposPro' or software == 'Topos':
        file.write('loop_\n')
        file.write('_symmetry_equiv_pos_site_id\n')
        file.write('_symmetry_equiv_pos_as_xyz\n')
        order = 1
        for symmetryEquivPosAsXyz in crystal.symmetryEquivPosAsXyzs:
            file.write("%s %s\n"%(order ,symmetryEquivPosAsXyz))
            order += 1

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
        if atomElement == 'Lr':
            atomElement = 'ZA'
        file.write(formAtom.format(atom.name.replace("T", "Si"), atomElement, coordinate[0], coordinate[1], coordinate[2]))

    if software == 'MaterialsStudio' or software.upper() == "MS":
        formBond = "{0:<5}\t{1:<5}\t{2:<10}\t{3:<5}\t{4:<3}\n"
        file.write('loop_\n')
        file.write('_geom_bond_atom_site_label_1\n')
        file.write('_geom_bond_atom_site_label_2\n')
        file.write('_geom_bond_distance\n')
        file.write('_geom_bond_site_symmetry_2\n')
        file.write('_ccdc_geom_bond_type\n')
        for bond in crystal.bonds:
            setSymmetry = '%s_%s%s%s'%(bond.setSymmetry[0], bond.setSymmetry[1], bond.setSymmetry[2], bond.setSymmetry[3])
            file.write(formBond.format(bond.atom1.name.replace("T", "Si"), bond.atom2.name.replace("T", "Si"), bond.distance, setSymmetry, bond.type))
        file.close()
        
    elif software == 'ToposPro' or software == 'Topos':
        def GetUniqueBonds(bonds):
            uniqueBonds = []
            for bond in bonds:
                if bond not in uniqueBonds:
                    uniqueBonds.append(bond)
                # if bond not in uniqueBonds:
                #     uniqueBonds.append(bond)
                # else:
                #     setSymmetryBond1 = [abs(i) for i in bond.setSymmetry]
                #     setSymmetryBond2 = [abs(i) for i in uniqueBonds[uniqueBonds.index(bond)].setSymmetry]
                #     if (sum(setSymmetryBond1) < sum(setSymmetryBond2)):
                #         uniqueBonds[uniqueBonds.index(bond)] = bond
            return uniqueBonds
    
        formBond = "{0:<5}\t{1:<5}\t{2:<10}\t{3:<10}\t{4:<7}{5:<5}\n"
        file.write('loop_\n')
        file.write('_topos_bond_atom_site_label_1\n')
        file.write('_topos_bond_atom_site_label_2\n')
        file.write('_topos_bond_site_symmetry_1\n')
        file.write('_topos_bond_site_symmetry_2\n')
        file.write('_topos_bond_distance\n')
        file.write('_topos_bond_type\n')
        
        uniqueBonds = GetUniqueBonds(crystal.bonds)
        # uniqueBonds = crystal.bonds
        for bond in uniqueBonds:
            # print(bond.atom1.name, bond.atom2.name, bond.distance, bond.setSymmetry)
            
            setSymmetry = '%s_%s_%s_%s'%(bond.setSymmetry[0], bond.setSymmetry[1]-5, bond.setSymmetry[2]-5, bond.setSymmetry[3]-5)
            file.write(formBond.format(bond.atom1.name.replace("T", "Si"), bond.atom2.name.replace("T", "Si"), '1_0_0_0', setSymmetry, bond.distance, 'V'))
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



