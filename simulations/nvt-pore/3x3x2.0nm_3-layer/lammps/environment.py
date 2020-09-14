"""Configuration of the project enviroment.

The environments defined in this module can be auto-detected.
This helps to define environment specific behaviour in heterogenous
environments.
"""
import flow
#from flow.environment import get_environment
#from flow.environment import format_timedelta


#__all__ = ['get_environment']
__all__ = ['RahmanEnvironment']

class RahmanEnvironment(flow.environment.TorqueEnvironment):
    hostname_pattern = 'master.cl.vanderbilt.edu'
    template = 'rahman.vanderbilt.sh'
    cores_per_node = 16
