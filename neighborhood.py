#! /usr/bin/env python
# vim: set fenc=utf8 ts=4 sw=4 et :
#
# Layer 2 network neighbourhood discovery tool
# written by Benedikt Waldvogel (mail at bwaldvogel.de)

# Copyright (c) 2013 Benedikt Waldvogel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from __future__ import absolute_import, division, print_function
import logging
import scapy.config
import scapy.layers.l2
import scapy.route
import socket
import math
import errno

def long2net(arg):
    if (arg <= 0 or arg >= 0xFFFFFFFF):
        raise ValueError("illegal netmask value", hex(arg))
    return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))


def to_CIDR_notation(bytes_network, bytes_netmask):
    network = scapy.utils.ltoa(bytes_network)
    netmask = long2net(bytes_netmask)
    net = "%s/%s" % (network, netmask)
    if netmask < 16:
        logger.warn("%s is too big. skipping" % net)
        return None

    return net


def get_subnet_sweep_params(include_loopback):
    for network, netmask, _, interface, address, _ in scapy.config.conf.route.routes:

        # skip loopback network and default gw
        if not include_loopback and (network == 0 or interface == 'lo' or
           address == '127.0.0.1' or address == '0.0.0.0'):
            continue

        if netmask <= 0 or netmask == 0xFFFFFFFF:
            continue

        net = to_CIDR_notation(network, netmask)

        if interface != scapy.config.conf.iface:
            # see http://trac.secdev.org/scapy/ticket/537
            print("skipping because scapy currently doesn't support arping on non-primary network interfaces")
            continue

        if net:
            return net
    return None
