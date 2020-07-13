import os
import sys
import mbuild
import foyer
import unyt as u
import mosdef_cassandra as mc
import numpy as np

from mosdef_cassandra.utils.tempdir import temporary_cd
from mosdef_slitpore.utils.cassandra import spce_water
from mosdef_slitpore.utils.utils import get_ff

# Filter some warnings -- to cleanup output for this demo
from warnings import filterwarnings

filterwarnings("ignore", category=UserWarning)
from parmed.exceptions import OpenMMWarning
filterwarnings("ignore", category=OpenMMWarning)


def main():
    # Create a water molecule with the spce geometry
    water = spce_water()
    ff = foyer.Forcefield(get_ff("pore-spce.xml"))
    water_typed = ff.apply(water)

    # Define conditions
    temperature = 298.0 * u.K
    # Define a range of (shifted) chemical potentials
    mus_adsorbate = np.arange(-60, -36, 3) * u.Unit("kJ/mol")

    # Define custom_args that are the same for all pure phase simulations
    custom_args = {
        "cutoff_style": "cut",
        "charge_style": "ewald",
        "rcut_min": 0.5 * u.angstrom,
        "vdw_cutoff": 9.0 * u.angstrom,
        "prop_freq": 10,
        "angle_style": ["fixed"],
    }

    for mu_adsorbate in mus_adsorbate:
        print(f"\nRun simulation: T = {temperature}, mu = {mu_adsorbate}\n")
        dirname = f"pure_vap_T_{temperature:0.1f}_mu_{mu_adsorbate:.1f}".replace(
            " ", "_"
        ).replace(
            "/", "-"
        )
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        else:
            pass
        with temporary_cd(dirname):
            # Box size depends on chemical potential
            # Prelim simulation shows mu' = -48 kJ/mol; p ~ 0.01 bar
            # Employ IG law to estimate remaining box sizes; target 40 waters
            mu_0 = -48 * u.kJ/u.mol
            p_0 = 0.01 * u.bar
            n_water_target = 40
            p_ig = p_0 * np.exp((mu_adsorbate-mu_0)/(u.kb * temperature))
            vol = n_water_target * u.kb * temperature / p_ig
            boxl = (vol**(1./3.)).to_value("nm")
            custom_args["charge_cutoff"] = 0.25 * boxl * u.nm

            species_list = [water_typed]
            box_list = [mbuild.Box([boxl, boxl, boxl])]
            system = mc.System(
                box_list, species_list,
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
                run_length=1000000,
                temperature=temperature,
                run_name="prod",
                restart_name="equil",
                chemical_potentials=[mu_adsorbate],
                **custom_args,
            )

if __name__ == "__main__":
    main()
