from scapy.all import RawVal, send
from scapy.contrib.rtps import RTPS
from scapy.contrib.rtps.rtps import (
    GUIDPrefixPacket,
    ProtocolVersionPacket,
    RTPSMessage,
    RTPSSubMessage_HEARTBEAT,
    RTPSSubMessage_INFO_DST,
    VendorIdPacket,
)
from scapy.layers.inet import IP, UDP

from common import APP_ID, HOST_ID, INSTANCE_ID, LISTENER_IP


def send_heartbeat(ros2_node_ip):
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
            RTPSSubMessage_HEARTBEAT(
                submessageFlags=0x01,
                octetsToNextHeader=28,
                # Seems like DDS will send HEARTBEAT packets of different
                # READER and WRITER types (i.e. PUBLICATIONS_READER,
                # SUBSCRIPTIONS_READER, and PARTICIPANT_MESSAGE_READER)
                # Discovery process uses HEARTBEAT
                reader_id=b"\x00\x00\x03\xc7",
                writer_id=b"\x00\x00\x03\xc2",
                firstAvailableSeqNum=1,
                lastSeqNum=9,
                count=1,
            ),
        ]
    )

    udp_packet = UDP(sport=33653, dport=7400)
    ip_packet = IP(dst=ros2_node_ip)

    packet = ip_packet / udp_packet / rtps_packet
    send(packet)


if __name__ == "__main__":
    send_heartbeat(LISTENER_IP)
