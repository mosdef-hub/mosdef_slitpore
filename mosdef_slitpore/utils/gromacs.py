import os

def add_settles(top_file):
    """Add settles section in GROMACS top file
    """
    atom_dict = dict()
    i = 0
    with open(top_file, 'r') as f:
        for line in f:
            if len(line.split()) == 0:
                continue
            if 'GPH' == line.split()[0]:
                atom_dict['GPH'] = i
                i += 1
            elif 'o_spce' == line.split()[0]:
                atom_dict['o_spce'] = i
                i += 1
            elif 'h_spce' == line.split()[0]:
                atom_dict['h_spce'] = i
                i += 1
            if i >= 3:
                break

    with open(top_file, 'a') as f:
        f.write('\n')
        f.write('[ settles ]\n')
        f.write('; OW    funct   doh     dhh\n')
        f.write('{}    1    0.1    0.1633'.format(atom_dict['o_spce']-1))

def write_ndx():
    """ Write GROMACS ndx file
    """
    cmd = 'printf "q\n" | gmx make_ndx -f init.gro -o index.ndx'
    os.system(cmd)
