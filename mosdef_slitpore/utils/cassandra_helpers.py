import mbuild
import numpy as np


def create_spce_water():
    """Generate a single water molecule with the SPC/E geometry

    Paper DOI: 10.1021/j100308a038

    Arguments
    ---------
    None

    Returns
    -------
    mbuild.Compound
    """
    OH_bl = 0.1  # nm
    HOH_angle = 109.47  # degrees
    water = mbuild.Compound(name="water")
    O = mbuild.Compound(name="O", pos=[0.0, 0.0, 0.0])
    H1 = mbuild.Compound(name="H", pos=[OH_bl, 0.0, 0.0])
    H2 = mbuild.Compound(
        name="H",
        pos=[
            OH_bl * np.cos(np.radians(HOH_angle)),
            OH_bl * np.sin(np.radians(HOH_angle)),
            0.0,
        ],
    )
    water.add([O, H1, H2])
    water.add_bond([O, H1])
    water.add_bond([O, H2])

    return water


# Instantiate a single water into the namespace
spce_water = create_spce_water()


def load_final_frame(fname):
    """Return the final frame of a Cassandra .xyz file as an mbuild.Compound

    Assumes there is a .H file with the same name. E.g., if the .xyz file
    is 'equil.out.xyz', there should also be an 'equil.out.H' containing
    the box information.

    Arguments
    ---------
    fname : str
        path to of the xyz file
    """
    if not isinstance(fname, str):
        raise TypeError("'fname' must be a string")
    if fname[-4:] == ".xyz":
        fname = fname[:-4]

    data = []
    with open(fname + ".xyz") as f:
        for line in f:
            data.append(line.strip().split())

    for iline, line in enumerate(data):
        if len(line) > 0:
            if line[0] == "MC_STEP:":
                natom_line = iline - 1

    final_frame = data[natom_line + 2 :]
    natoms = int(data[natom_line][0])
    with open(fname + "-final.xyz", "w") as f:
        f.write(f"{natoms}\nAtoms\n")
        for coord in final_frame:
            f.write(
                "{}\t{}\t{}\t{}\n".format(
                    coord[0], coord[1], coord[2], coord[3],
                )
            )
    data = []
    with open(fname + ".H") as f:
        for line in f:
            data.append(line.strip().split())

    nspecies = int(data[-1][0])
    box_matrix = np.asarray(
        data[-(nspecies + 5) : -(nspecies + 2)], dtype=np.float32
    )
    assert box_matrix.shape == (3, 3)
    if np.count_nonzero(box_matrix - np.diag(np.diagonal(box_matrix))) > 0:
        raise ValueError("Only orthogonal boxes are currently supported")

    # If all is well load in the final frame
    frame = mbuild.load(fname + "-final.xyz")
    # mbuild.Compounds use nanometers!
    frame.periodicity = np.diagonal(box_matrix / 10.0)

    return frame


def check_simulation(filen, nsteps):
    """Check the energy file to determine if the simulation is complete

    Parameters
    ----------
    filen : string
        energy file name to check
    nsteps : int
        number of steps in simulation

    Returns
    -------
    complete : bool
        True if the simulation has reached nsteps, else false
    """
    try:
        with open(filen) as f:
            for line in f:
                pass
            last = line.strip().split()
    except OSError:
        return False

    if int(last[0]) == nsteps:
        return True
    else:
        return False


def mu_from_mu_cassandra(mu_shift, beta):
    q_rot = 43.45
    return mu_shift - (1./beta) * np.log(q_rot)


