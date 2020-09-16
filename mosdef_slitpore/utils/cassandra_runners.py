import mbuild
import foyer
import unyt as u
import mosdef_cassandra as mc
import numpy as np

from mosdef_slitpore.utils.utils import get_ff
from mosdef_slitpore.utils.cassandra_helpers import spce_water


def run_adsorption(
    empty_pore, pore_width, temperature, mu, nsteps, **custom_args,
    ):
    """Run adsorption simulation at the specified temperature
    and chemical potential

    Parameters
    ----------
    pore : mbuild.Compound
        empty pore system to simulate
    pore_width : u.unyt_quantity (length)
        width of pore for restricted insertions
    temperature: u.unyt_quantity (temperature)
        desired temperature
    mu : u.unyt_quantity (energy)
        desired chemical potential
    nsteps : int
        number of MC steps in simulation

    Returns
    -------
    None: runs simulation
    """
    # Load foyer ff
    ff = foyer.Forcefield(get_ff("pore-spce.xml"))

    # Apply ff
    typed_pore = ff.apply(pore)

    # Create a water molecule with the spce geometry
    typed_water = ff.apply(spce_water)

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

    # Specify the restricted insertion
    restricted_type = [[None, "slitpore"]]
    restricted_value = [[None, 0.5 * pore_width ]]
    moves.add_restricted_insertions(
        species_list, restricted_type, restricted_value
    )

    # Set thermodynamic properties
    thermo_props = [
        "energy_total",
        "nmols",
    ]

    default_args = {
        "run_name" : "gcmc",
        "cutoff_style": "cut",
        "charge_style": "ewald",
        "rcut_min": 0.5 * u.angstrom,
        "vdw_cutoff": 9.0 * u.angstrom,
        "charge_cutoff": 9.0 * u.angstrom,
        "properties": thermo_props,
        "angle_style": ["harmonic", "fixed"],
        "coord_freq": 100000,
    }

    custom_args = { **default_args, **custom_args}

    mc.run(
        system=system,
        moveset=moves,
        run_type="equilibration",
        run_length=nsteps,
        temperature=temperature,
        chemical_potentials=["none", mu],
        **custom_args,
    )


def run_desorption(
    filled_pore,
    pore_width,
    temperature,
    mu,
    nsteps_nvt,
    nsteps_gcmc,
    **custom_args,
):
    """Run desorption simulation at the specified temperature
    and chemical potential

    Parameters
    ----------
    filled_pore : porebuilder.GraphenePoreSolvent
        pore filled with water
    pore_width : u.unyt_quantity (length)
        width of pore for restricted insertions
    temperature: u.unyt_quantity (temperature)
        desired temperature
    mu : u.unyt_quantity (energy)
        desired chemical potential
    nsteps_nvt : int
        number of MC steps for NVT equilibration
    nsteps_gcmc : int
        number of MC steps for GCMC simulation

    Returns
    -------
    None: runs simulation
    """
    # Load foyer ff
    ff = foyer.Forcefield(get_ff("pore-spce.xml"))

    # Extract just the pore and apply ff
    empty_pore = filled_pore.children[0]
    typed_pore = ff.apply(empty_pore)

    # Create a water molecule with the spce geometry and apply ff
    typed_water = ff.apply(spce_water)

    # Determine the number of waters in the pore
    nwater = len([child for child in filled_pore.children])-1

    # Create box and species list
    box_list = [filled_pore]
    species_list = [typed_pore, typed_water]

    # Specify mols at start of the simulation
    mols_in_boxes = [[1, nwater]]

    # Create MC system
    system = mc.System(box_list, species_list, mols_in_boxes=mols_in_boxes)
    moves = mc.MoveSet("nvt", species_list)

    # Set move probabilities
    moves.prob_translate = 0.5
    moves.prob_rotate = 0.5
    moves.prob_regrow = 0.0

    # Set thermodynamic properties
    thermo_props = [
        "energy_total",
        "nmols",
    ]

    default_args = {
        "run_name" : "nvt",
        "cutoff_style": "cut",
        "charge_style": "ewald",
        "rcut_min": 0.5 * u.angstrom,
        "vdw_cutoff": 9.0 * u.angstrom,
        "charge_cutoff": 9.0 * u.angstrom,
        "properties": thermo_props,
        "angle_style": ["harmonic", "fixed"],
        "coord_freq": 100000,
        "prop_freq": 1000,
    }

    custom_args = { **default_args, **custom_args}

    # Run NVT equilibration
    mc.run(
        system=system,
        moveset=moves,
        run_type="equilibration",
        run_length=nsteps_eq,
        temperature=temperature,
        **custom_args,
    )

    # Create MC system
    equilibrated_box = load_final_frame("nvt.out.xyz")
    box_list = [equilibrated_box]
    system = mc.System(box_list, species_list, mols_in_boxes=mols_in_boxes)
    moves = mc.MoveSet("gcmc", species_list)

    # Set move probabilities
    moves.prob_translate = 0.25
    moves.prob_rotate = 0.25
    moves.prob_insert = 0.25
    moves.prob_regrow = 0.0

    # Specify the restricted insertion
    restricted_type = [[None, "slitpore"]]
    restricted_value = [[None, 0.5 * pore_width]]
    moves.add_restricted_insertions(
        species_list, restricted_type, restricted_value
    )

    # Run GCMC
    custom_args["run_name"] = "gcmc"
    mc.run(
        system=system,
        moveset=moves,
        run_type="equilibration",
        run_length=nsteps_prod,
        temperature=temperature,
        chemical_potentials=["none", mu],
        **custom_args,
    )


def run_nvt(filled_pore, temperature, nsteps_eq, nsteps_prod, **custom_args):
    """Run an NVT MC simulation at the specified temperature

    Parameters
    ----------
    filled_pore : porebuilder.GraphenePoreSolvent
        pore filled with water
    temperature: u.unyt_quantity (temperature)
        desired temperature
    nsteps_eq : int
        number of MC steps for NVT equilibration
    nsteps_prod : int
        number of MC steps for GCMC simulation

    Returns
    -------
    None: runs simulation
    """
    # Load foyer ff
    ff = foyer.Forcefield(get_ff("pore-spce.xml"))

    # Extract just the pore and apply ff
    empty_pore = filled_pore.children[0]
    typed_pore = ff.apply(empty_pore)

    # Create a water molecule with the spce geometry and apply ff
    typed_water = ff.apply(spce_water)

    # Determine the number of waters in the pore
    nwater = len([child for child in filled_pore.children])-1

    # Create box and species list
    box_list = [filled_pore]
    species_list = [typed_pore, typed_water]

    # Specify mols at start of the simulation
    mols_in_boxes = [[1, nwater]]

    # Create MC system
    system = mc.System(box_list, species_list, mols_in_boxes=mols_in_boxes)
    moves = mc.MoveSet("nvt", species_list)

    # Set move probabilities
    moves.prob_translate = 0.5
    moves.prob_rotate = 0.5
    moves.prob_regrow = 0.0

    # Set thermodynamic properties
    thermo_props = [
        "energy_total",
    ]

    default_args = {
        "run_name": "equil.nvt",
        "cutoff_style": "cut",
        "charge_style": "ewald",
        "rcut_min": 0.5 * u.angstrom,
        "vdw_cutoff": 9.0 * u.angstrom,
        "charge_cutoff": 9.0 * u.angstrom,
        "properties": thermo_props,
        "angle_style": ["harmonic", "fixed"],
        "coord_freq": 10000,
        "prop_freq": 1000,
    }

    custom_args = { **default_args, **custom_args}

    # Run NVT equilibration
    mc.run(
        system=system,
        moveset=moves,
        run_type="equilibration",
        run_length=nsteps_eq,
        temperature=temperature,
        **custom_args,
    )

    # Run production
    custom_args["run_name"] = "prod.nvt"
    custom_args["restart_name"] = "equil.nvt"
    mc.restart(
        system=system,
        moveset=moves,
        run_type="production",
        run_length=nsteps_prod,
        temperature=temperature,
        **custom_args,
    )

