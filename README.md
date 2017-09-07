Cisco IOS Configuration Generator
=================================

This project consists of a collection of python tools that can be used for auto-generation of configuration files used on Cisco IOS devices, that could be incorporated in scripts for automating configuration of multiple devices.

Utilities include:

- `csint.py`: interface configuration tool

### csint.py

```
usage: csint.py [-h] [-d DESC] [-4 IPV4] [-6 IPV6] [-l LLOCAL] [-m NETMASK]
                [-s] [-x]
                interface
```

**Generator utility for Cisco IOS interface configuration**

```
positional arguments:
  interface             Interface

optional arguments:
  -h, --help            show this help message and exit
  -d DESC, --desc DESC  Description
  -4 IPV4, --ipv4 IPV4  IPv4 address/CIDR
  -6 IPV6, --ipv6 IPV6  IPv6 address/CIDR
  -l LLOCAL, --llocal LLOCAL
                        IPv6 link-local address
  -m NETMASK, --netmask NETMASK
                        Add dotted decimal IPv4 netmask
  -s, --shutdown        Shutdown interface (default: no shutdown)
  -x, --exit            Add exit to end of interface configuration
```
