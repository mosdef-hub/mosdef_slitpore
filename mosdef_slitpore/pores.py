import mbuild as mb
from mbuild import recipes

def narrow_small_singlelayer():
    """Generate an empty pore with the following:

    Single layer graphene
    Lateral: 1.0 nm x 1.0 nm
    Width: 1.0 nm

    Arguments
    ---------
    None

    Returns
    -------
    mbuild.Compound
    """
    # Create pore system
    pore = recipes.GraphenePore(
        pore_width=1.0,
        pore_length=1.0,
        pore_depth=1.1,
        n_sheets=1,
        slit_pore_dim=2
    )

    # Translate to centered at 0,0,0 and make box larger in z
    pore.translate([0,0,1.0-pore.center[2]])
    pore.periodicity[2] = 2.0

    return pore

def narrow_large_singlelayer():
    """Generate an empty pore with the following:

    Single layer graphene
    Lateral: 3.0 nm x 3.0 nm
    Width: 1.0 nm

    Arguments
    ---------
    None

    Returns
    -------
    mbuild.Compound
    """
    # Create pore system
    pore = recipes.GraphenePore(
        pore_width=1.0,
        pore_length=3.0,
        pore_depth=3.0,
        n_sheets=1,
        slit_pore_dim=2
    )

    # Translate to centered at 0,0,0 and make box larger in z
    pore.translate([0,0,1.0-pore.center[2]])
    pore.periodicity[2] = 2.0

    return pore

def narrow_large_triplelayer():
    """Generate an empty pore with the following:

    Three graphene layers
    Lateral: 3.0 nm x 3.0 nm
    Width: 1.0 nm

    Arguments
    ---------
    None

    Returns
    -------
    mbuild.Compound
    """
    # Create pore system
    pore = recipes.GraphenePore(
        pore_width=1.0,
        pore_length=3.0,
        pore_depth=3.0,
        n_sheets=3,
        slit_pore_dim=2
    )

    # Translate to centered at 0,0,0 and make box larger in z
    pore.translate([0,0,2.7-pore.center[2]])
    pore.periodicity[2] = 5.4

    return pore


def wide_large_triplelayer():
    """Generate an empty pore with the following:

    Three graphene layers
    Lateral: 3.0 nm x 3.0 nm
    Width: 1.6 nm

    Arguments
    ---------
    None

    Returns
    -------
    mbuild.Compound
    """
    # Create pore system
    pore = recipes.GraphenePore(
        pore_width=1.6,
        pore_length=3.0,
        pore_depth=3.0,
        n_sheets=3,
        slit_pore_dim=2
    )
   
    # Translate to centered at 0,0,0 and make box larger in z
    pore.translate([0,0,3.0-pore.center[2]])
    pore.periodicity[2] = 6.0

    return pore

def graphene_surface():
    """Generate a graphene surface with the following:
    Three graphene layers
    Lateral: 4.0 nm x 4.0 nm
    Vacuum: 20 nm

    Arguments
    ---------
    None

    Returns
    -------
    mbuild.Compound
    """
    surface = recipes.GrapheneSurface(
            x_length=4.0,
            y_length=4.0,
            n_sheets=3,
            vacuum=20.0
            )
