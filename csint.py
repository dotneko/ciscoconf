import argparse

# Define cs_Interface class
class cs_Interface:
    ident = ""
    desc = ""
    ipv4 = ""
    netmask = ""
    ipv6 = ""
    linklocal = ""
    no_shut = True

    def __init__(self, id):
        self.ident = id

    def __init__(self, id, ipv4addr):
        self.ident = id
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
        self.netmask = mask

    def add_desc(self, desc):
        self.desc = desc

    def no_shut(self, enable):
        self.no_shut = enable

    def output(self):
        out_str = "interface {}\n ip address {} {}\n".format(self.ident, self.ipv4, self.netmask)
        if self.desc != "":
            out_str += "description {}\n".format(self.desc)
        if self.no_shut:
            out_str += " no shutdown\n"
        else:
            out_str += " shutdown\n"
        return out_str

parser = argparse.ArgumentParser(description="Generator utility for Cisco IOS interface configuration")
parser.add_argument("interface", help="Interface")
parser.add_argument("ipv4_address", help="IPv4 address/CIDR")
parser.add_argument("-m", "--netmask", help="Add dotted decimal netmask", type=str)
parser.add_argument("-s", "--shutdown", help="Shutdown interface (default: no shutdown)", action="store_true")
parser.add_argument("--desc", help="Description")
args = parser.parse_args()

# Assign IP address to interface; converts CIDR to netmask
cs_int = cs_Interface(args.interface, args.ipv4_address)

# Use given netmask if flag -m | --netmask provided
if args.netmask:
    cs_int.add_mask(args.netmask)
if args.shutdown:
    cs_int.no_shut(False)
print(cs_int.output())

