import os
from pkg_resources import resource_filename

def get_ff(filename):
    """Get path to a file in ffxml directory
    """
    file_path = resource_filename('mosdef_slitpore',
            os.path.join('ffxml', filename))

    return file_path
