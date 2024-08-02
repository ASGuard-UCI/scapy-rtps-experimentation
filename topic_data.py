import time

from scapy.all import RawVal, send
from scapy.contrib.rtps import RTPS
from scapy.contrib.rtps.rtps import (
    DataPacket,
    GUIDPrefixPacket,
    ProtocolVersionPacket,
    RTPSMessage,
    RTPSSubMessage_DATA,
    RTPSSubMessage_INFO_DST,
    RTPSSubMessage_INFO_TS,
    VendorIdPacket,
)
from scapy.layers.inet import IP, UDP

from common import APP_ID, HOST_ID, INSTANCE_ID, LISTENER_IP


def send_topic_data(ros2_node_ip):
    rtps_packet = RTPS(
        # Using 2.3 for protocol version since ROS 2
        protocolVersion=ProtocolVersionPacket(major=2, minor=3),
        # Vendor is eProsima - Fast-RTPS "01.15"
        vendorId=VendorIdPacket(vendor_id=RawVal("\x01\x0F")),
        # Taken directly from Wireshark packet. How are these values generated?
        guidPrefix=GUIDPrefixPacket(
            hostId=HOST_ID,
            appId=APP_ID,
            instanceId=INSTANCE_ID,
        ),
        magic=b"RTPS",
    ) / RTPSMessage(
        submessages=[
            RTPSSubMessage_INFO_DST(
                submessageFlags=0x01,
                octetsToNextHeader=12,
                guidPrefix=GUIDPrefixPacket(
                    hostId=HOST_ID,
                    appId=APP_ID,
                    instanceId=INSTANCE_ID,
                ),
            ),
            RTPSSubMessage_INFO_TS(
                submessageFlags=0x01,
                octetsToNextHeader=8,
                ts_seconds=int(time.time()),
                ts_fraction=653661355,
            ),
            RTPSSubMessage_DATA(
                submessageFlags=0x05,
                octetsToNextHeader=128,
                octetsToInlineQoS=16,
                readerEntityIdKey=0x000002,
                readerEntityIdKind=0x04,
                writerEntityIdKey=0x000001,
                writerEntityIdKind=0x03,
                writerSeqNumHi=0,
                writerSeqNumLow=3,
                data=DataPacket(
                    encapsulationKind=0x0001,
                    serializedData=b"\x01\x0f\x4e\x32\x50\x13\xc8\x8d\x00\x00\x00\x00\x00\x00\x01\xc1\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x2f\x00\x00\x00\x06\x00\x00\x00\x64\x75\x6d\x6d\x79\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x0f\x4e\x32\x50\x13\xc8\x8d\x00\x00\x00\x00\x00\x00\x03\x03\x00\x00\x00\x00\x00\x00\x00\x00\x01\x0f\x4e\x32\x50\x13\xc8\x8d\x00\x00\x00\x00\x00\x00\x04\x03\x00\x00\x00\x00\x00\x00\x00\x00",
                ),
            ),
        ]
    )

    udp_packet = UDP(sport=33653, dport=7400)
    ip_packet = IP(dst=ros2_node_ip)

    packet = ip_packet / udp_packet / rtps_packet
    send(packet)


if __name__ == "__main__":
    send_topic_data(LISTENER_IP)
