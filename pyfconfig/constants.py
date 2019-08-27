"""
Common constants found in the kernel header file (if.h), and netlink\
documentation (man(7) netlink).
"""
import os

officialFlags = {
    "UP": 1 << 0,
    "BROADCAST": 1 << 1,
    "DEBUG": 1 << 2,
    "LOOPBACK": 1 << 3,
    "POINTOPOINT": 1 << 4,
    "NOTRAILERS": 1 << 5,
    "RUNNING": 1 << 6,
    "NOARP": 1 << 7,
    "PROMISC": 1 << 8,
    "ALLMULTI": 1 << 9,
    "MASTER": 1 << 10,
    "SLAVE": 1 << 11,
    "MULTICAST": 1 << 12,
    "PORTSEL": 1 << 13,
    "AUTOMEDIA": 1 << 14,
    "DYNAMIC": 1 << 15,
    "LOWER_UP": 1 << 16,
    "DORMANT": 1 << 17,
    "ECHO": 1 << 18
}

sysPath = "/sys/class/net/"

RTAMessages = {
    "RTA_DST": "dest",
    "RTA_SRC": "src",
    "RTA_OIF": "outInterface",
    "RTA_GATEWAY": "gateway",
    "RTA_PRIORITY": "priority",
    "RTA_TABLE": "table",
    "RTA_PREFSRC": "prefSrc",
    "RTA_METRICS": "metrics",
    "RTA_MULTIPATH": "multipath",
    "RTA_PROTOINFO": "protoInfo",
    "RTA_FLOW": "flow",
    "RTA_CACHEINFO": "cacheInfo"
}

IS_ROOT = os.geteuid() == 0
