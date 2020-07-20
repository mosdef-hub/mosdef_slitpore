import mbuild
import foyer
import unyt as u
import mosdef_cassandra as mc
import numpy as np


def run_adsorption(pore, temperature, mu, nsteps):
    """Run adsorption simulation at the specified temperature
    and chemical potential

    Parameters
    ----------

    Returns
    -------

    """
    # Verify inputs

    # Apply ff
    ff = foyer.Forcefield('../../../ffxml/pore-spce.xml')
    typed_pore = ff.apply(pore)

    # Create a water molecule with the spce geometry
    water = spce_water()
    typed_water = ff.apply(water)

    # Create box and species list
    box_list = [pore]
    species_list = [typed_pore, typed_water]

    # Specify mols at start of the simulation
    mols_in_boxes = [[1, 0]]

    # Create MC system
    system = mc.System(box_list, species_list, mols_in_boxes=mols_in_boxes)
    moves = mc.MoveSet("gcmc", species_list)

    # Set move probabilities
    moves.prob_translate = 0.25
    moves.prob_rotate = 0.25
    moves.prob_insert = 0.25
    moves.prob_regrow = 0.0

    # Set thermodynamic properties
    thermo_props = [
        "energy_total",
        "pressure",
        "volume",
        "nmols",
        "mass_density",
    ]

    custom_args = {
        "cutoff_style" : "cut",
        "charge_style": "ewald",
        "rcut_min": 0.5 * u.angstrom,
        "vdw_cutoff": 9.0 * u.angstrom,
        "charge_cutoff" : 9.0 * u.angstrom,
        "properties": thermo_props,
        "angle_style" : ["harmonic", "fixed"],
        "run_name": "equil",
        "coord_freq": 50000,
    }

    # Specify the restricted insertion
    restricted_type = [[None, 'slitpore']]
    restricted_value = [[None, 0.8 * u.nm]]
    moves.add_restricted_insertions(species_list,
                                   restricted_type,
                                   restricted_value)

    mc.run(
        system=system,
   	    moveset=moves,
   	    run_type="equilibration",
   	    run_length=nsteps,
   	    temperature=temperature,
   	    chemical_potentials=["none", mu],
   	    **custom_args,
    )


def restart_adsorption(pore, temperature, mu, nsteps):
    """Run adsorption simulation at the specified temperature
    and chemical potential

    Parameters
    ----------

    Returns
    -------

    """
    # Verify inputs

    # Apply ff
    ff = foyer.Forcefield('../../../ffxml/pore-spce.xml')
    typed_pore = ff.apply(pore)

    # Create a water molecule with the spce geometry
    water = spce_water()
    typed_water = ff.apply(water)

    # Create box and species list
    box_list = [pore]
    species_list = [typed_pore, typed_water]

    # Specify mols at start of the simulation
    mols_in_boxes = [[1, 0]]

    # Create MC system
    system = mc.System(box_list, species_list, mols_in_boxes=mols_in_boxes)
    moves = mc.MoveSet("gcmc", species_list)

    # Set move probabilities
    moves.prob_translate = 0.25
    moves.prob_rotate = 0.25
    moves.prob_insert = 0.25
    moves.prob_regrow = 0.0

    # Set thermodynamic properties
    thermo_props = [
        "energy_total",
        "pressure",
        "volume",
        "nmols",
        "mass_density",
    ]

    custom_args = {
        "cutoff_style" : "cut",
        "charge_style": "ewald",
        "rcut_min": 0.5 * u.angstrom,
        "vdw_cutoff": 9.0 * u.angstrom,
        "charge_cutoff" : 9.0 * u.angstrom,
        "properties": thermo_props,
        "angle_style" : ["harmonic", "fixed"],
        "run_name": "equil",
        "coord_freq": 50000,
    }

    # Specify the restricted insertion
    restricted_type = [[None, 'slitpore']]
    restricted_value = [[None, 0.8 * u.nm]]
    moves.add_restricted_insertions(species_list,
                                   restricted_type,
                                   restricted_value)

    custom_args["run_name"] = "equil.rst"
    custom_args["restart_name"] = "equil"
    mc.restart(
        system=system,
   	    moveset=moves,
   	    run_type="equilibration",
   	    run_length=nsteps,
   	    temperature=temperature,
   	    chemical_potentials=["none", mu],
   	    **custom_args,
    )


def spce_water():
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
                natom_line = iline-1

    final_frame = data[natom_line+2:]
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

    box_matrix = np.asarray(data[-6:-3], dtype=np.float32)
    assert box_matrix.shape == (3,3)
    if np.count_nonzero(box_matrix - np.diag(np.diagonal(box_matrix))) > 0:
        raise ValueError("Only orthogonal boxes are currently supported")

    # If all is well load in the final frame
    frame = mbuild.load(fname + "-final.xyz")
    # mbuild.Compounds use nanometers!
    frame.periodicity = np.diagonal(box_matrix/10.0)

    return frame
