# -*- coding: utf-8 -*-
"""Set of common utils for MQTT protocol handling."""
#
#    Copyright (C) 2020 Samsung Electronics. All Rights Reserved.
#       Authors: Jakub Botwicz (Samsung R&D Poland),
#                Michał Radwański (Samsung R&D Poland)
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
from hexdump import dehex
from scapy.all import TCP
from scapy.contrib.mqtt import CONTROL_PACKET_TYPE, MQTT, MQTTConnack, RETURN_CODE

from .common_utils import print_verbose, show_verbose, tcp_sr1
from .protocol_tester import ProtocolTester

# MQTT message
# message type = CONNECT
# protocol name = MQTT
# protocol version = 3.1.1
# client ID = 1
MQTT_CONN_MQTT = "100d00044d5154540402003c000131"
MQTT_CONN_MQTT = "10a30100044d51545404c2003c00404c43466a527667787c7365637572656d6f64653d322c7369676e6d6574686f643d7368613235362c74696d657374616d703d313538323039303232303332367c0013566a376f3572467a62582675546a6e42374249004062393363333536663837333966303636366562303530353131326339326663393963376139646334323765353766643530373130393965343535663438613736"
MQTT_CONN_MQTT = "10880100044d51545404c0003c003e304b537835476e557c7365637572656d6f64653d342c7369676e6d6574686f643d736861312c74696d657374616d703d313536363434303733343234347c0012256368616e6e656c2526304b537835476e55002834623734376331316438323339313835343731636333666632636238353930343264383263366434"
MQTT_CONN_MQISDP = (
    "102400064d51497364700302003c000233000000000000000000000000000000000000000000"
)
MQTT_CONN_REJECT = (
    "102400064d51497364700302003c000200000000000000000000000000000000000000000000"
)


def mqtt_request(test_params, out_packet):
    """Sends MQTT request to broker and waiting for response."""
    try:
        for i in range(1 + test_params.nr_retries):
            in_data = tcp_sr1(test_params, out_packet)
            in_packet = MQTT(in_data)
            show_verbose(test_params, in_packet)
            if (
                in_packet[MQTT].type in CONTROL_PACKET_TYPE
                and CONTROL_PACKET_TYPE[in_packet[MQTT].type] == "CONNACK"
            ):
                print_verbose(
                    test_params,
                    "MQTT ping {}: in_packet[MQTTConnack].retcode: {}".format(
                        i + 1, RETURN_CODE[in_packet[MQTTConnack].retcode]
                    ),
                )
                return True
    except (socket.timeout, socket.error) as error:
        print_verbose(test_params, error)
    return False


class MQTTTester(ProtocolTester):
    """Tester of MQTT protocol"""

    def __init__(self):
        ProtocolTester.__init__(self)

    @staticmethod
    def protocol_short_name():
        """Provides short (abbreviated) name of protocol"""
        return "MQTT"

    @staticmethod
    def protocol_full_name():
        """Provides full (not abbreviated) name of protocol"""
        return "MQ Telemetry Transport"

    @staticmethod
    def default_port():
        """Provides default port used by implemented protocol"""
        return 1883

    @staticmethod
    def transport_protocol():
        """Provides Scapy class of transport protocol used by this tester (usually TCP or UDP)"""
        return TCP

    @staticmethod
    def request_parser():
        """Provides Scapy class implementing parsing of protocol requests"""
        return MQTT

    @staticmethod
    def response_parser():
        """Provides Scapy class implementing parsing of protocol responses"""
        return MQTT

    @staticmethod
    def implements_service_ping():
        """Returns True if this tester implements service_ping for this protocol"""
        return True

    @staticmethod
    def ping(test_params, show_result=False):
        """Checks MQTT service availability by sending ping packet and waiting for response."""
        # MQTT ping is using Connect message
        for packet_hex in [MQTT_CONN_MQTT, MQTT_CONN_MQISDP]:
            packet_data = dehex(packet_hex)
            out_packet = MQTT(packet_data)
            if mqtt_request(test_params, out_packet):
                return True
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
