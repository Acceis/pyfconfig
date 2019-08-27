"""
This module serves basic layer 2 management for network interfaces.
"""
from pyfconfig.exceptions import *
from pyfconfig.constants import *
from pyfconfig.methods import *
import os


class Interface:
    """
    Layer 2 interface representation.
    """

    def __init__(self, name):
        """
        Constructs a new Interface object.

        :param name: The name of the interface. The interface with this name\
must exist (eg : "eth0").
        """
        if interfaceExists(name):
            self._name = name
        else:
            raise AttributeError("Invalid interface name.")

    def __str__(self):
        return self._name

    def __repr__(self):
        return f"pyfconfig.Interface({self._name})"

    # Manage sysfs toggleable flags
    def up(self):
        """
        Sets this interface up.
        """
        newFlags = hex(self.raw_flags + officialFlags["UP"])
        self.__writeFlags(newFlags)

    def down(self):
        """
        Sets this interface down
        """
        newFlags = hex(self.raw_flags - officialFlags["UP"])
        self.__writeFlags(newFlags)

    def toggleDebug(self):
        """
        Toggles the DEBUG flag of this interface
        """
        self.__toggleFlag("DEBUG")

    def toggleNoTrailers(self):
        """
        Toggles the NOTRAILERS flag of this interface.
        """
        self.__toggleFlag("NOTRAILERS")

    def toggleNoARP(self):
        """
        Toggles the NOARP flag of this interface.
        """
        self.__toggleFlag("NOARP")

    def togglePromisc(self):
        """
        Toggles the PROMISC flag of this interface.
        """
        self.__toggleFlag("PROMISC")

    def toggleAllMulti(self):
        """
        Toggles the ALLMULTI flag of this interface.
        """
        self.__toggleFlag("ALLMULTI")

    def toggleMulticast(self):
        """
        Toggles the MULTICAST flag of this interface.
        """
        self.__toggleFlag("MULTICAST")

    def togglePortSel(self):
        """
        Toggles the PORTSEL flag of this interface.
        """
        self.__toggleFlag("PORTSEL")

    def toggleAutoMedia(self):
        """
        Toggles the AUTOMEDIA flag of this interface.
        """
        self.__toggleFlag("AUTOMEDIA")

    def toggleDynamic(self):
        """
        Toggles the DYNAMIC flag of this interface.
        """
        self.__toggleFlag("DYNAMIC")

    def __toggleFlag(self, flag):
        if getattr(self, flag):
            newFlags = hex(self.raw_flags - officialFlags[flag])
        else:
            newFlags = hex(self.raw_flags + officialFlags[flag])
        self.__writeFlags(newFlags)

    def __writeFlags(self, newFlags):
        if IS_ROOT:
            fd = open(f"{sysPath}{self._name}/flags", "w")
            fd.write(f"{newFlags}\n")
            fd.close
        else:
            raise NotRootException()

    @property
    def operstate(self):
        """
        Returns the operative state of the interface
        """
        operstatefd = open(f"{sysPath}{self._name}/operstate", "r")
        operstate = operstatefd.readline().rstrip("\n")
        operstatefd.close()
        return operstate

    @property
    def address(self):
        """
        Returns the MAC address of the interface
        """
        address = open(f"{sysPath}{self._name}/address", "r").readline()
        return address.rstrip("\n")

    @property
    def name(self):
        """
        Returns the name of the interface
        """
        return self._name

    @property
    def carrier(self):
        """
        Returns the carrier state (physical link presence) of the interface
        """
        carrier = False
        try:
            carrierfd = open(f"{sysPath}{self._name}/carrier", "r")
            carrier = carrierfd.readline(1)
            carrierfd.close
            carrier = True if carrier == "1" else False
        except OSError:
            # The file "carrier" is locked by the kernel when the interface
            # is physically down. The read() call would then fail, thus this
            # try/except block
            carrier = False
        return carrier

    @property
    def wired(self):
        """
        Returns a boolean to get the type of interface.
        Returns True if the interface is a wired one, false otherwise.
        """
        return "wireless" not in os.listdir(f"{sysPath}{self._name}/")

    @property
    def wireless(self):
        """
        Returns a boolean to get the type of interface.
        Returns True if the interface is a wireless one, false oterwise.
        """
        return "wireless" in os.listdir(f"{sysPath}{self._name}/")

    """
    Getters and setters for flags
    """
    @property
    def flags(self):
        """
        Returns the interface's flags as a parsed python set.
        Example : {"UP", "RUNNING"}
        """
        fsFlags = open(f"{sysPath}{self._name}/flags", "r").readline()
        return parseFlags(int(fsFlags.rstrip("\n"), 16))

    @property
    def raw_flags(self):
        """
        Returns the interface's flags as an integer.
        """
        fsFlags = open(f"{sysPath}{self._name}/flags", "r").readline()
        return int(fsFlags.rstrip("\n"), 16)

    @property
    def UP(self):
        """
        Returns the value of the flag UP.
        """
        return "UP" in self.flags

    @property
    def BROADCAST(self):
        """
        Returns the value of the flag BROADCAST.
        """
        return "BROADCAST" in self.flags

    @property
    def DEBUG(self):
        """
        Returns the value of the flag DEBUG.
        """
        return "DEBUG" in self.flags

    @property
    def LOOPBACK(self):
        """
        Returns the value of the flag LOOPBACK.
        """
        return "LOOPBACK" in self.flags

    @property
    def POINTOPOINT(self):
        """
        Returns the value of the flag POINTOPOINT.
        """
        return "POINTOPOINT" in self.flags

    @property
    def NOTRAILERS(self):
        """
        Returns the value of the flag NOTRAILERS.
        """
        return "NOTRAILERS" in self.flags

    @property
    def RUNNING(self):
        """
        Returns the value of the flag RUNNING.
        """
        return "RUNNING" in self.flags

    @property
    def NOARP(self):
        """
        Returns the value of the flag NOARP.
        """
        return "NOARP" in self.flags

    @property
    def PROMISC(self):
        """
        Returns the value of the flag PROMISC.
        """
        return "PROMISC" in self.flags

    @property
    def ALLMULTI(self):
        """
        Returns the value of the flag ALLMULTI.
        """
        return "ALLMULTI" in self.flags

    @property
    def MASTER(self):
        """
        Returns the value of the flag MASTER.
        """
        return "MASTER" in self.flags

    @property
    def SLAVE(self):
        """
        Returns the value of the flag SLAVE.
        """
        return "SLAVE" in self.flags

    @property
    def MULTICAST(self):
        """
        Returns the value of the flag MULTICAST.
        """
        return "MULTICAST" in self.flags

    @property
    def PORTSEL(self):
        """
        Returns the value of the flag PORTSEL.
        """
        return "PORTSEL" in self.flags

    @property
    def AUTOMEDIA(self):
        """
        Returns the value of the flag AUTOMEDIA.
        """
        return "AUTOMEDIA" in self.flags

    @property
    def DYNAMIC(self):
        """
        Returns the value of the flag DYNAMIC.
        """
        return "DYNAMIC" in self.flags


def getInterfaces(loopback=False):
    """
    Returns the list of the current network interfaces.

    :param loopback: States wether loopback interfaces must be returned\
 as well (default : False).
    """
    global sysPath
    returnList = []
    for name in os.listdir(sysPath):
        intf = Interface(name)
        if intf.LOOPBACK and loopback or not intf.LOOPBACK:
            returnList.append(intf)
    return returnList
