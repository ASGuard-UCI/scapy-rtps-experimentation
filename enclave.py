from scapy.all import send
from scapy.contrib.rtps import RTPS
from scapy.contrib.rtps.pid_types import (
    PID_DEFAULT_UNICAST_LOCATOR,
    PID_METATRAFFIC_UNICAST_LOCATOR,
    PID_PARTICIPANT_GUID,
    PID_PROTOCOL_VERSION,
    PID_UNKNOWN,
    PID_VENDOR_ID,
    GUIDPacket,
    LocatorPacket,
)
from scapy.contrib.rtps.rtps import (
    DataPacket,
    GUIDPrefixPacket,
    ParameterListPacket,
    ProtocolVersionPacket,
    RTPSMessage,
    RTPSSubMessage_DATA,
    RTPSSubMessage_INFO_TS,
    VendorIdPacket,
)
from scapy.layers.inet import IP, UDP

from common import COLLECTOR_IP, LISTENER_IP


def enclave():
    rtps_packet = RTPS(
        protocolVersion=ProtocolVersionPacket(major=2, minor=3),
        vendorId=VendorIdPacket(vendor_id=271),
        guidPrefix=GUIDPrefixPacket(hostId=17799417, appId=3560560027, instanceId=0),
        magic=b"RTPS",
    ) / RTPSMessage(
        submessages=[
            RTPSSubMessage_INFO_TS(
                submessageId=9,
                submessageFlags=1,
                octetsToNextHeader=8,
                ts_seconds=1722809856,
                ts_fraction=92346737,
            ),
            RTPSSubMessage_DATA(
                submessageId=21,
                submessageFlags=5,
                octetsToNextHeader=244,
                extraFlags=0,
                octetsToInlineQoS=16,
                readerEntityIdKey=256,
                readerEntityIdKind=199,
                writerEntityIdKey=256,
                writerEntityIdKind=194,
                writerSeqNumHi=0,
                writerSeqNumLow=1,
                data=DataPacket(
                    encapsulationKind=3,
                    encapsulationOptions=0,
                    parameterList=ParameterListPacket(
                        parameterValues=[
                            PID_PROTOCOL_VERSION(
                                parameterId=21,
                                parameterLength=4,
                                protocolVersion=ProtocolVersionPacket(major=2, minor=3),
                                padding=b"\x00\x00",
                            ),
                            PID_VENDOR_ID(
                                parameterId=22,
                                parameterLength=4,
                                vendorId=VendorIdPacket(vendor_id=271),
                                padding=b"\x00\x00",
                            ),
                            PID_PARTICIPANT_GUID(
                                parameterId=80,
                                parameterLength=16,
                                guid=GUIDPacket(
                                    hostId=17799417,
                                    appId=3560560027,
                                    instanceId=0,
                                    entityId=449,
                                ),
                            ),
                            PID_METATRAFFIC_UNICAST_LOCATOR(
                                parameterId=50,
                                parameterLength=24,
                                locator=LocatorPacket(
                                    locatorKind=1, port=7410, address=LISTENER_IP
                                ),
                            ),
                            PID_DEFAULT_UNICAST_LOCATOR(
                                parameterId=49,
                                parameterLength=24,
                                locator=LocatorPacket(
                                    locatorKind=16, port=7411, address=LISTENER_IP
                                ),
                            ),
                            PID_UNKNOWN(
                                parameterId=38997,
                                parameterLength=249,
                                parameterData=b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x001\x00\x18\x00\x01\x00\x00\x00\xf3\x1c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xa84\x81\x02\x00\x08\x00\x14\x00\x00\x00\x00\x00\x00\x00X\x00\x04\x00?\x0c\x0f\x00b\x00\x08\x00\x02\x00\x00\x00/\x00\x00\x00,\x00\x10\x00\x0b\x00\x00\x00enclave=/;\x00\x00Y\x00(\x00\x01\x00\x00\x00\x11\x00\x00\x00PARTICIPANT_TYPE\x00\x00\x00\x00\x07\x00\x00\x00SIMPLE\x00\x00\x01\x00\x00\x00",
                            ),
                        ]
                    ),
                ),
            ),
        ]
    )

    udp_packet = UDP(sport=33653, dport=7400)
    ip_packet = IP(dst=COLLECTOR_IP)

    packet = ip_packet / udp_packet / rtps_packet
    send(packet)
