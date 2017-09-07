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

##### Examples:

**Interface g0/1 with IPv4 address using CIDR or dotted decimal notation:**

```
csint.py g0/1 -4 172.16.0.1/24
csint.py g0/1 -4 172.16.0.1 255.255.255.0
```

Will generate:

```
interface g0/1
 ip address 172.16.0.1 255.255.255.240
 no shutdown
```

**Interface lo1 with IPv6 address:**

```
csint.py lo1 -6 2001:db8:cafe:a::1/64 -l fe80::1
```

Will generate:

```
interface lo1
 ipv6 address 2001:db8:cafe:a::1/64
 ipv6 address fe80::1 link-local
 no shutdown
```
