#!/usr/bin/python

# Copyright (c) 2017 Gavin Chan
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
import argparse
import textwrap

class cs_Config:
    hostname = ""
    domain = ""
    ipv6ur = True
    en_pass = "class"
    con_pass = "cisco"
    local_user = ""
    local_pass = "cisco"
    vty_login = "login"
    vty_trans = "none"
    exec_timeout = 5
    pktracer = False
    rsa_mod = 2048

    def __init__(self, hostname, con_pass, en_pass):
        self.hostname = hostname
        self.con_pass = con_pass
        self.en_pass = en_pass

    def conf_login(self, userpass):
        # Configure local login credentials
        self.local_user, self.local_pass = userpass.split(":")

        if self.local_user == "":
            # If only given password, e.g. ":password", use for telnet login
            self.vty_login = "login"
        else:
            self.vty_login = "login local"

    def conf_ipv6ur(self, enabled):
        self.ipv6ur = enabled

    def conf_domain(self, domain):
        self.domain = domain

    def conf_vty(self, transp):
        self.vty_trans = transp

    def conf_pktracer(self, ptmode):
        self.pktracer = ptmode

    def gen_vty(self):
        vty_conf = ""
        if self.vty_login == "login local":
            # Generate username/password for local login
            vty_conf += "username {} algorithm-type scrypt secret {}\n".format(self.local_user, self.local_pass)

            if "ssh" in self.vty_trans and self.domain:
                # Configure SSH if domain name exists

                if self.pktracer:
                    # Use Cisco packet tracer 7 syntax for key generation
                    vty_conf += "crypto key generate rsa\n{}".format(self.rsa_mod)
                else:
                    # Default: for Cisco devices
                    vty_conf += "crypto key generate rsa modulus {}".format(self.rsa_mod)
                vty_conf += "\nip ssh version 2\n"
        elif "ssh" in self.vty_trans:
            print("!! Error: SSH cannot be configured without credentials/domain name")

        # Generate basic vty configuration
        vty_conf += textwrap.dedent("""\
                line vty 0 15
                 logging synchronous
                 exec-timeout {}
                 transport input {}
                 """.format(self.exec_timeout, self.vty_trans))
        if self.vty_trans == "none":
            vty_conf += " no login"
        elif self.vty_trans == "telnet":
            if self.vty_login == "login":
                vty_conf += " password {}\n {}".format(self.local_pass, self.vty_login)
            else:
                vty_conf += " " + self.vty_login
        return vty_conf

    def output(self):
        # Generate output

        out_str = textwrap.dedent("""\
                hostname {}
                no ip domain-lookup
                service password-encryption
                banner motd #Unauthorized access prohibited#
                """.format(self.hostname))
        if self.domain:
            out_str += "ip domain-name {}\n".format(self.domain)
        if self.ipv6ur:
            out_str += "ipv6 unicast-routing\n"

        out_str += textwrap.dedent("""\
                enable algorithm-type scrypt secret {}
                line con 0
                 password {}
                 logging synchronous
                 login
                 exec-timeout {}
                line aux 0
                 no exec
                 """.format(self.en_pass, self.con_pass, self.exec_timeout))
        out_str += self.gen_vty()
        return out_str

# Main
parser = argparse.ArgumentParser(description="Generator utility for Cisco IOS device initial configuration")
parser.add_argument("hostname", help="Hostname")
parser.add_argument("console_pass", help="Console Password")
parser.add_argument("enable_pass", help="Enable Secret")
parser.add_argument("-d", "--domain", help="Domain Name")
parser.add_argument("-l", "--login", help="Login Credentials - username:password", type=str)
parser.add_argument("-t", "--telnet", help="Enable Telnet; use -l username:password", action="store_true")
parser.add_argument("-s", "--ssh", help="Enable SSH; use -l username:password", action="store_true")
parser.add_argument("-x6", "--noipv6", help="Disable IPv6 unicast-routing", action="store_true")
parser.add_argument("-K", "--packettracer", help="Packet Tracer syntax for key generation", action="store_true")
args = parser.parse_args()

cs_conf = cs_Config(args.hostname, args.console_pass, args.enable_pass)
if args.domain:
    cs_conf.conf_domain(args.domain)
if args.login:
    cs_conf.conf_login(args.login)
if args.packettracer:
    cs_conf.conf_pktracer(True)
if args.noipv6:
    cs_conf.conf_ipv6ur(False)
if args.telnet:
    if args.ssh and args.login:
        # Use both telnet and SSH
        cs_conf.conf_vty("telnet ssh")
    else:
        # Use telnet only
        cs_conf.conf_vty("telnet")
elif args.ssh:
    # Use SSH only
    cs_conf.conf_vty("ssh")

# Generate output

config = cs_conf.output()

print(config)
