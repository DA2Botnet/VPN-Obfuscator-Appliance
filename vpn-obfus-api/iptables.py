# Controls the iptables in the linux system
# For use to setup routing for vpn obfuscator
#
# Opens ports and routes traffic through to vpn
#
# Part of the DA2 system of appliances
# Written by Joseph Telaak
#
# Example Run:
# init()
# allow_tunneling()
# allow_vpn(1, 1194, "VPN")
# wrapup()
#

import os

# Flushes iptables
def flush():
    os.system("iptables -t nat -F")
    os.systen("iptables -t mangle -F")
    os.system("iptables -F")
    os.system("iptables -X")

# Block all
def initial_blocking():
    os.system("iptables -P OUTPUT DROP")
    os.system("iptables -P INPUT DROP")
    os.system("iptables -P FORWARDS DROP")

# Allow Localhost
def allow_localhost():
    os.system("iptables -A INPUT -i lo ACCEPT")
    os.system("iptables -A OUTPUT -o lo ACCEPT")

# Make sure the host can communicate with dhcp
def enable_dhcp():
    os.system("iptables -A OUTPUT -d 255.255.255.255 -j ACCEPT")
    os.system("iptables -A INPUT -d 255.255.255.255 -j ACCEPT")

# Allows established sessions to receive traffic
def allow_established_sesions():
    os.system("iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT")

# Performs the generic initialization tasks
# i.e. flush, initial_blocking, allow_localhost, enable_dhcp, allow_established_sessions
def init():
    flush()
    initial_blocking()
    allow_localhost()
    allow_established_sesions()

# Allow Tunneling
def allow_tunneling():
    os.system("iptables -A INPUT -i tun+ -j ACCEPT")
    os.system("iptables -A FORWARD -i tun+ -j ACCEPT")
    os.system("iptables -A FORWARD -o tun+ -j ACCEPT")
    os.system("iptables -t nat -A POSTROUTING -o tun+ -j MASQUERADE")
    os.system("iptables -A OUTPUT -o tun+ -j ACCEPT")

# Default VPN port
default_vpn_port = 1194

# Allow a vpn connection
def allow_vpn(number, port, comment):
    # TODO Check port validity

    os.system("iptables -I OUTPUT " + str(number) + " -p udp --destination-port " + str(port) + " -m comment --comment \"" + comment + "\" -j ACCEPT")

# Block all
def final_blocking():
    os.system("iptables -A OUTPUT -j DROP")
    os.system("iptables -A INPUT -j DROP")
    os.system("iptables -A FORWARD -j DROP")

# Log dropped packets
def enable_logging():
    os.system("iptables -N logging")
    os.system("iptables -A INPUT -j logging")
    os.system("iptables -A OUTPUT -j logging")
    os.system("iptables -A logging -m limit --limit 2/min -j LOG --log-prefix \"IPTables general: \" --log-level 7")
    os.system("iptables -A logging -j DROP")

# Wraps up the setup
# Does final_blocking and enable_logging
def wrapup():
    final_blocking()
    enable_logging()