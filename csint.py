import argparse

# Define cs_Interface class
class cs_Interface:
    ident = ""
    desc = ""
    encap = ""
    ipv4 = ""
    netmask = ""
    ipv6 = ""
    linklocal = ""
    no_shut = True
    sw_mode = ""
    vlan = ""

    def __init__(self, id):
        self.ident = id

    def add_ipv4(self, ipv4addr):
        if '/' in ipv4addr:
            self.ipv4, cidr = self.ip_cidr(ipv4addr)
            self.netmask = self.get_mask(cidr)
        else:
            # Use 255.255.255.255 for netmask by default
            self.ipv4 = ipv4addr
            self.netmask = "255.255.255.255"

    def ip_cidr(self, ipaddr):
        addr,cidr = ipaddr.split("/")
        return addr, cidr

    def get_mask(self, cidr):
        # Convert CIDR to dotted decimal netmmask
        # Input: numeric string
        # Output: Netmask in dotted decimal (string)

        try:
            num = int(cidr)
        except:
            print("Error")
            return "255.255.255.0"
        mask = ""
        if num >= 32 or num <= 0:
            mask = "255.255.255.255"
        else:
            quo = num // 8
            rem = num % 8
            for i in range(quo):
                mask += "255."
            dec = 256 - 2**(8-rem)
            mask += str(dec)
            if quo < 3:
                for i in range(3-quo):
                    mask += ".0"
        return mask

    def add_mask(self, mask):
        # Uses specified netmask for IPv4 address
        self.netmask = mask

    def add_desc(self, desc):
        # Adds description to interface
        self.desc = desc

    def conf_encap(self, encap):
        self.encap = encap

    def add_ipv6(self, ipv6):
        # Adds IPv6 address to interface
        self.ipv6 = ipv6

    def add_llocal(self, llocal):
        # Adds IPv6 link-local address to interface
        self.linklocal = llocal

    def conf_access(self):
        self.sw_mode = "access"

    def conf_native(self):
        self.sw_mode = "native"

    def conf_trunk(self):
        self.sw_mode = "trunk"

    def conf_vlan(self, vlan):
        self.vlan = vlan

    def no_shut(self, enable):
        # Sets port status (default enable=true)
        self.no_shut = enable

    def output(self):
        out_str = "interface {}\n".format(self.ident)
        if self.desc:
            out_str += " description {}\n".format(self.desc)
        if self.encap:
            out_str += " encapsulation {}".format(self.encap)
            if self.encap.lower() == "dot1q" and self.vlan:
                out_str += " {}\n".format(self.vlan)
            else:
                out_str += "\n"
        if self.ipv4:
            out_str += " ip address {} {}\n".format(self.ipv4, self.netmask)
        if self.ipv6:
            out_str += " ipv6 address {}\n".format(self.ipv6)
        if self.linklocal:
            out_str += " ipv6 address {} link-local\n".format(self.linklocal)
        if self.sw_mode == "trunk":
            out_str += " switchport mode trunk\n"
        elif self.sw_mode == "native":
            out_str += " switchport mode trunk\n"
            if self.vlan:
                out_str += " switchport trunk native vlan {}\n".format(self.vlan)
        elif self.sw_mode == "access":
            out_str += " switchport mode access\n"
            if self.vlan:
                out_str += " switchport access vlan {}\n".format(self.vlan)
        if self.no_shut:
            out_str += " no shutdown\n"
        else:
            out_str += " shutdown\n"
        return out_str

parser = argparse.ArgumentParser(description="Generator utility for Cisco IOS interface configuration")
parser.add_argument("interface", help="Interface")
parser.add_argument("-d", "--desc", help="Description")
parser.add_argument("-e", "--encap", help="Encapsulation mode; can use with -v", type=str)
parser.add_argument("-4", "--ipv4", help="IPv4 address/CIDR", type=str)
parser.add_argument("-6", "--ipv6", help="IPv6 address/CIDR", type=str)
parser.add_argument("-l", "--llocal", help="IPv6 link-local address", type=str)
parser.add_argument("-m", "--netmask", help="Specify IPv4 netmask instead of CIDR", type=str)
parser.add_argument("-sA", "--access", help="Switchport mode access; use with -v to specify VLAN", action="store_true")
parser.add_argument("-sN", "--native", help="Switchport mode trunk; use with -v to specify VLAN", action="store_true")
parser.add_argument("-sT", "--trunk", help="Switchport mode trunk", action="store_true")
parser.add_argument("-v", "--vlan", help="VLAN number; use with -a,-n,-e dot1q", type=str)
parser.add_argument("-X", "--shutdown", help="Shutdown interface (default: no shutdown)", action="store_true")
parser.add_argument("-x", "--exit", help="Add exit to end of interface configuration", action="store_true")
args = parser.parse_args()

cs_int = cs_Interface(args.interface)

if args.ipv4:
    # Create instance of interface +/- IPv4 address/CIDR
    cs_int.add_ipv4(args.ipv4)

    if args.netmask:
        # Use given netmask if specified
        cs_int.add_mask(args.netmask)
else:
    cs_int = cs_Interface(args.interface)

if args.desc:
    # Add description to interface
    cs_int.add_desc(args.desc)
if args.encap:
    cs_int.conf_encap(args.encap)
if args.ipv6:
    # Add IPv6 address
    cs_int.add_ipv6(args.ipv6)
if args.llocal:
    # Add IPv6 link-local address
    cs_int.add_llocal(args.llocal)

# Switchport modes and VLAN
if args.access:
    # Configure switchport mode access +/- VLAN
    cs_int.conf_access()
if args.native:
    # Configure switchport mode trunk native +/- VLAN
    cs_int.conf_native()
if args.trunk:
    # Configure switchport mode trunk
    cs_int.conf_trunk()
if args.vlan:
    # Configure switchport mode access vlan
    cs_int.conf_vlan(args.vlan)
if args.shutdown:
    # Explicitly shutdown port
    cs_int.no_shut(False)

# Generate output

config = cs_int.output()
if args.exit:
    config += " exit\n"

print(config)
