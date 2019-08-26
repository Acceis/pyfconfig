"""
Internal methods for code clarity.
"""
from pyfconfig.constants import *
import os


def parseFlags(flags):
    """
    Parses flags from hexadecimal to a readable set.
    Example : transforms the integer 0x1003 into the set {"UP", "RUNNING"}.
    """
    global officialFlags
    return {flag for flag, val in officialFlags.items() if flags & val}


def interfaceExists(name):
    """
    Returns wether an interface exists on the current system.
    """
    global sysPath
    return name and name in os.listdir(sysPath)


def flagsSetToHexString(flags):
    """
    Converts a set of flags to its hexadecimal representation, as a String.
    """
    return hex(sum([y for _, y in officialFlags.items() if _ in flags]))


def flagsHexStringToSet(flags):
    """
    See the method parseFlags(flags).
    """
    return parseFlags(flags)


def parseRTAMessage(msg):
    """
    Parses raw netlink messages to a simpler, cleaner dictionnary.
    """
    attrs = msg["attrs"]
    returnList = {}
    for key, val in attrs:
        if key in RTAMessages.keys():
            returnList[RTAMessages[key]] = val
    return returnList
