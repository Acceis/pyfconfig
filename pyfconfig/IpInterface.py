"""
This module adds the layer 3 functionalities. It allows the creation of\
IP interface objects, with IP addresses and routes.
"""
from pyroute2.netlink.exceptions import NetlinkError
from socket import AF_INET, AF_INET6
from pyfconfig.Interface import Interface
from pyroute2 import IPRoute
from pyfconfig.exceptions import *
from pyfconfig.methods import *
import ipaddress


class IpInterface(Interface):
    """
    The base class for interacting with IP enabled interfaces.
    """

    def __init__(self, name):
        """
        Creates an IPInterface object.

        :param name: The name of the interface.
               This name must reflect an existing interface such as "eth0"\
 on most systems.
        """
        super().__init__(name)

    def __repr__(self):
        return f"pyfconfig.IpInterface({self._name})"

    @property
    def ipAddresses(self):
        """
        Returns the list of IP addresses assigned to this interface.
        The list contains addresses as defined by the standard library\
ipaddress. The addresses are represented as IPv4Interface\
 or IPv6Interface objects.
        """
        returnList = []
        addresses = ()
        with IPRoute() as ipr:
            addresses = ipr.get_addr(label=self._name)
            for address in addresses:
                theip = [x[1]
                         for x in address["attrs"] if x[0] == "IFA_ADDRESS"][0]
                theprefix = address["prefixlen"]
                if address["family"] == AF_INET:
                    returnList.append(
                        ipaddress.IPv4Interface(f"{theip}/{theprefix}"))
                elif address["family"] == AF_INET6:
                    returnList.append(
                        ipaddress.IPv6Interface(f"{theip}/{theprefix}"))
        return returnList

    def addIpAddress(self, address):
        """
        Adds an IP address to the current Interface.

        :param address: The string representing the IP address.
                  Example : "10.10.10.1/24", "10.10.10.1"
        """
        addr = ipaddress.ip_interface(address)
        with IPRoute() as ipr:
            index = ipr.link_lookup(ifname=self.name)[0]
            try:
                ipr.addr("add", index=index,
                         address=str(addr.ip), mask=addr.network.prefixlen)
            except NetlinkError as e:
                if e.code == 17:
                    raise AddressAlreadyExistsException()
                else:
                    raise e

    def delIpAddress(self, address):
        """
        Removes an IP address from the current Interface.

        :param address: The string representing the IP address to remove.
                        Example : "10.10.10.1/24", "10.10.10.1".
        """
        addr = ipaddress.ip_interface(address)
        with IPRoute() as ipr:
            index = ipr.link_lookup(ifname=self.name)
            try:
                ipr.addr("delete", index=index,
                         address=str(addr.ip), mask=addr.network.prefixlen)
            except NetlinkError as e:
                if e.code == 99:  # address already exists
                    raise AddressDoesntExistException()
                else:
                    raise e

    def flushIpAddresses(self):
        """
        Flushes IP addresses for the current interface.
        """
        with IPRoute() as ipr:
            ipr.flush_addr(label=self.name)

    @property
    def routes(self):
        """
        Returns the list of the routes having this interface as output.
        """
        routes = getRoutes()
        returnList = []
        for route in routes:
            if "outInterface" in route.keys()\
               and route["outInterface"].name == self.name:
                returnList.append(route)
        return returnList


def getRoutes(cacheInfo=False):
    """
    Returns a list of every route declared on the current system.

    :param cacheInfo: Boolean to indicate if statistical data about routes\
 must be returned if available.
    """
    returnList = []
    with IPRoute() as ipr:
        routes = ipr.get_routes()
        parsedRoutes = [parseRTAMessage(r) for r in routes]
        for route in parsedRoutes:
            if "dest" not in route.keys():
                route["dest"] = "0.0.0.0/0"
            route["dest"] = ipaddress.ip_network("0.0.0.0/0")
            if "src" in route.keys():
                route["src"] = ipaddress.ip_address(route["src"])
            if "gateway" in route.keys():
                route["gateway"] = ipaddress.ip_address(route["gateway"])
            if "outInterface" in route.keys():
                intf = ipr.get_links(route["outInterface"])[0]
                intf = intf.get_attr("IFLA_IFNAME")
                route["outInterface"] = IpInterface(intf)
            if "inInterface" in route.keys():
                intf = ipr.get_links(route["inInterface"])[0]
                intf = intf.get_attr("IFLA_IFNAME")
                route["inInterface"] = IpInterface(intf)
            if "cacheInfo" in route.keys() and cacheInfo is False:
                del route["cacheInfo"]
            returnList.append(route)
    return returnList
