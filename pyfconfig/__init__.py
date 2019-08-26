"""
Pyfconfig is a simple and naive python library to interact with your\
 system's network interfaces under linux.
The layer 2 management is entirely based on the /sys filesystem. It allows\
interfaces management (setting state, flags, parameters etc).
The layer 3 management is based over the pyroute2 library which is a netlink\
sockets interface. This library allows to add and remove IP addresses to the\
various network interface you might have.
"""
from pyfconfig.Interface import Interface, getInterfaces
from pyfconfig.IpInterface import IpInterface, getRoutes

__all__ = ["Interface", "IpInterface", "getInterfaces", "getRoutes"]