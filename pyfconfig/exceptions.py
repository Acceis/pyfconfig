"""
Just a few exceptions for code clarity and easier debugging.
"""

from pyroute2.netlink.exceptions import NetlinkError


class AddressAlreadyExistsException(NetlinkError):
    """
    Exception to declare that an address cannot be added as it already exists.
    """

    def __init__(self):
        """
        The exception constructor
        """
        super().__init__(17, "This IP Address already exists.")


class AddressDoesntExistException(NetlinkError):
    """
    Exception to declare that an address cannot be removed as\
 it does not even exist.
    """

    def __init__(self):
        """
        The exception constructor
        """
        super().__init__(99, "This IP address does not exist.")


class NotRootException(Exception):
    """
    Exception to state that the library cannot operate as the user requests\
because of lack of proper rights
    """

    def __init__(self):
        """
        The exception constructor
        """
        super().__init__("Permission denied.")
