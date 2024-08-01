from scapy.all import RawVal, send
from scapy.contrib.rtps import RTPS
from scapy.contrib.rtps.rtps import (
    GUIDPrefixPacket,
    ProtocolVersionPacket,
    RTPSMessage,
    RTPSSubMessage_ACKNACK,
    RTPSSubMessage_INFO_DST,
    VendorIdPacket,
)
from scapy.layers.inet import IP, UDP

from common import APP_ID, HOST_ID, INSTANCE_ID, LISTENER_IP


def main():
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
            RTPSSubMessage_ACKNACK(
                # Some ACKNACK packets have the "final flag" set. What does
                # this mean? The value of this flag affects the number in
                # octetsToNextHeader.
                # As with the HEARTBEAT packets, DDS seems to be testing
                # whether the publishing/subscribing capabilities work
                # via the reader and writer entities.
                submessageFlags=0x01,
                octetsToNextHeader=24,
                reader_id=b"\x00\x02\x00\xc7",
                writer_id=b"\x00\x02\x00\xc2",
                readerSNState=b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
                count=2 << 24,
            ),
        ]
    )

    udp_packet = UDP(sport=33653, dport=7400)
    ip_packet = IP(dst=LISTENER_IP)

    packet = ip_packet / udp_packet / rtps_packet
    send(packet)


if __name__ == "__main__":
    main()
