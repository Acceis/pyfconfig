# Pyfconfig

Pyfconfig is a simple package to manipulate your network interfaces under Linux.
It uses the */sys* filesystem to interact with your interfaces and the *pyroute2* package to implement the IP part (retrieving addresses and routes).

The entire package manages both IPv4 and IPv6 indinstinctly.

Every IP/network address uses the standard library [ipaddress](https://docs.python.org/3/library/ipaddress.html).

This module works for python 3.5+ and requires the following dependency : `pyroute2`.

## What can I do with it ?

### Retrieve your current interfaces :
```python
from pyfconfig import *

# Retrieve everything
interfaces = getInterfaces()
print(interfaces)
# [pyfconfig.Interface(eth0), pyfconfig.Interface(wlan0)]

# Retrieve a single interface
eth0 = IpInterface("eth0")
eth0
# pyfconfig.IpInterface(eth0)
```

### Access basic data
```python
from pyfconfig import *
eth0 = IpInterface("eth0")

# Retrieve the MAC address
print(eth0.address)
# 12:34:ab:cd:ff:43

# Get flags
print(eth0.flags)
# {'MULTICAST', 'BROADCAST', 'UP'}

# Or a single flag
print(eth0.UP)
# True

# Get the interface type
print(eth0.wired)
# True
print(eth0.wireless)
# False

# Get routing information for a single interface
print(eth0.routes)
# [{"gateway": IPv4Address('10.10.10.254'), 'outInterface': pyfconfig.IpInterface(eth0), 'dest': IPv4Network('0.0.0.0/0')}]

# or for the entire system
print(getRoutes())
""" [
        {
            "gateway": IPv4Address('10.10.10.254'),
            'outInterface': pyfconfig.IpInterface(eth0),
            'dest': IPv4Network('0.0.0.0/0')},
        {
            'table': 255,
            'dest': IPv4Network('0.0.0.0/0'),
            'prefSrc': '127.0.0.1', 
            'outInterface': pyfconfig.IpInterface(lo)
        }
    ]
"""

# Get IP addresses
print(eth0.ipAddresses)
# [IPv4Interface('10.10.10.42/24')]
```

### Configure your interfaces
```python
from pyfconfig import *
eth0 = IpInterface("eth0")

# Set the interface up and down
eth0.up()
eth0.down()

# Toggle some random flag
eth0.togglePromisc()

# Add and remove IP addresses
eth0.addIpAddress("10.10.10.42/24")
eth0.delIpAddress("10.10.10.42.24")
```

## Installation

Download the latest release and install it with pip :
```bash
pip install --user ./pyfconfig-0.1.1.tar.gz
```
