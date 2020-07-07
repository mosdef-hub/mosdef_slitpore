import os
import sys
import mbuild
import foyer
import unyt as u
import mosdef_cassandra as mc
import numpy as np

sys.path.append("../../../")

from mosdef_cassandra.utils.tempdir import temporary_cd
from mosdef_slitpore.utils.cassandra import spce_water, load_final_frame

# Filter some warnings -- to cleanup output for this demo
from warnings import filterwarnings

filterwarnings("ignore", category=UserWarning)
from parmed.exceptions import OpenMMWarning
filterwarnings("ignore", category=OpenMMWarning)


def main():
    # Create a water molecule with the spce geometry
    water = spce_water()
    ff = foyer.Forcefield("../../ffxml/pore-spce.xml")
    water_typed = ff.apply(water)

    # Define conditions
    temperature = 298.0 * u.K
    # Define a range of (shifted) chemical potentials
    mus_adsorbate = np.arange(-48, -36, 3) * u.Unit("kJ/mol")

    # Define custom_args that are the same for all pure phase simulations
    custom_args = {
        "cutoff_style": "cut",
        "charge_style": "ewald",
        "rcut_min": 0.5 * u.angstrom,
        "vdw_cutoff": 9.0 * u.angstrom,
        "charge_cutoff": 9.0 * u.angstrom,
        "prop_freq": 10,
        "angle_style": ["fixed"],
    }
    
    # First run a simulation of NPT SPC/E water near
    # ambient pressure to get equilibrated liquid box
    print(f"\nRun simulation: T = {temperature}\n")
    dirname = f"pure_liq_T_{temperature:0.1f}".replace(
        " ", "_"
    ).replace(
        "/", "-"
    )
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    else:
        pass
    with temporary_cd(dirname):

        boxl = 2.0  # nm
        nwater = 264
        species_list = [water_typed]
        box_list = [mbuild.Box([boxl, boxl, boxl])]
        mols_to_add = [[nwater]]
        system = mc.System(
            box_list, species_list, mols_to_add=mols_to_add
        )
        moveset = mc.MoveSet("npt", species_list)
        moveset.prob_regrow = 0.0
        moveset.prob_translate = 0.499
        moveset.prob_rotate = 0.499
        moveset.prob_volume = 0.002

        mc.run(
            system=system,
            moveset=moveset,
            run_type="equil",
            run_length=500000,
            temperature=temperature,
            pressure=1.0 * u.bar,
            run_name="equil-npt",
            **custom_args,
        )
        
        equilibrated_box = load_final_frame("equil-npt.out.xyz")

    # Next run GCMC at each chemical potential
    for mu_adsorbate in mus_adsorbate:
        print(
            f"\nRun simulation: T = {temperature}, mu = {mu_adsorbate}\n"
        )
        dirname = f"pure_liq_T_{temperature:0.1f}_mu_{mu_adsorbate:.1f}".replace(
            " ", "_"
        ).replace(
            "/", "-"
        )
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        else:
            pass
        with temporary_cd(dirname):

            box_list = [equilibrated_box]
            mols_in_boxes = [[nwater]]
            system = mc.System(
                box_list, species_list, mols_in_boxes=mols_in_boxes
            )
            moveset = mc.MoveSet("gcmc", species_list)
            moveset.prob_regrow = 0.0
            moveset.prob_translate = 0.3
            moveset.prob_rotate = 0.3
            moveset.prob_insert = 0.2

            mc.run(
                system=system,
                moveset=moveset,
                run_type="equil",
                run_length=500000,
                temperature=temperature,
                run_name="equil",
                chemical_potentials=[mu_adsorbate],
                **custom_args,
            )

            mc.restart(
                system=system,
                moveset=moveset,
                run_type="prod",
                run_length=5500000,
                temperature=temperature,
                run_name="prod",
                restart_name="equil",
                chemical_potentials=[mu_adsorbate],
                **custom_args,
            )

if __name__ == "__main__":
    main()
