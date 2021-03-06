# -*- coding: utf-8 -*-
"""Set of common utils for HTCPCP protocol handling."""
#
#    Copyright (C) 2020 Samsung Electronics. All Rights Reserved.
#       Author: Jakub Botwicz (Samsung R&D Poland)
#
#    This file is part of Cotopaxi.
#
#    Cotopaxi is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    Cotopaxi is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Cotopaxi.  If not, see <http://www.gnu.org/licenses/>.
#

import socket
from scapy.all import TCP
from scapy.layers.http import HTTPRequest, HTTPResponse

from .common_utils import print_verbose, tcp_sr1
from .protocol_tester import ProtocolTester

HTCPCP_BREW = (
    "BREW kafo://pot-0 HTCPCP/1.0\r\n" "Content-Type: message/coffeepot\r\n" "\r\n"
)


class HTCPCPTester(ProtocolTester):
    """Tester of HTCPCP protocol"""

    def __init__(self):
        ProtocolTester.__init__(self)

    @staticmethod
    def protocol_short_name():
        """Provides short (abbreviated) name of protocol"""
        return "HTCPCP"

    @staticmethod
    def protocol_full_name():
        """Provides full (not abbreviated) name of protocol"""
        return "Hyper Text Coffee Pot Control Protocol"

    @staticmethod
    def default_port():
        """Provides default port used by implemented protocol"""
        return 80

    @staticmethod
    def transport_protocol():
        """Provides Scapy class of transport protocol used by this tester (usually TCP or UDP)"""
        return TCP

    @staticmethod
    def request_parser():
        """Provides Scapy class implementing parsing of protocol requests"""
        return HTTPRequest

    @staticmethod
    def response_parser():
        """Provides Scapy class implementing parsing of protocol responses"""
        return HTTPResponse

    @staticmethod
    def implements_service_ping():
        """Returns True if this tester implements service_ping for this protocol"""
        return True

    @staticmethod
    def ping(test_params, show_result=False):
        """Checks HTCPCP service availability by sending BREW message and waiting for response."""

        try:
            for _ in range(1 + test_params.nr_retries):
                in_data = tcp_sr1(test_params, HTCPCP_BREW)
                if in_data:
                    print_verbose(
                        test_params,
                        "\n".join(["Received response:", 50 * "=", in_data, 50 * "="]),
                    )
                    if "HTCPCP/1.0" in in_data:
                        print_verbose(test_params, "HTCPCP BREW : SUCCESS")
                        return True
        except (socket.timeout, socket.error) as error:
            print_verbose(test_params, error)
        return False

    @staticmethod
    def implements_fingerprinting():
        """Returns True if this tester implements fingerprinting for this protocol"""
        return False

    @staticmethod
    def implements_resource_listing():
        """Returns True if this tester implements resource for this protocol"""
        return False

    @staticmethod
    def implements_server_fuzzing():
        """Returns True if this tester implements server fuzzing for this protocol"""
        return True

    @staticmethod
    def implements_client_fuzzing():
        """Returns True if this tester implements clients fuzzing for this protocol"""
        return True

    @staticmethod
    def implements_vulnerability_testing():
        """Returns True if this tester implements vulnerability testing for this protocol"""
        return True
