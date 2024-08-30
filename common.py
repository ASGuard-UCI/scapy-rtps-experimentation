HOST_ID = 0x010F4E32
APP_ID = 0x0915C6E7
INSTANCE_ID = 0x00000000

METATRAFFIC_UNICAST_PORT = 7410
DEFAULT_UNICAST_PORT = 7411
COLLECTOR_IP = "3.19.252.184"

# UPDATE TO IP OF LISTENER NODE
LISTENER_IP = "3.14.203.13"

# Talker IP is         .128


"""
1. Set up both VMs
2. Start Listener VM
3. Run `ros2 run demo_nodes_cpp listener`
4. Run code in send_to_multicast.py in host machine
    The listener should start sending packets to the honeypot IP

TODO:
5. The honeypot should replicate the original ROS 2 communciation
    (ex. between the talker and listener) by responding appropriately
    to the packets that it receives:
    - When receiving an ACKNACK or a HEARTBEAT, it should respond with one
    of the same structure
6. Eventually, the honeypot should send the packet that contains the topic data
    /dummy. Afterwards, the listener should eventually respond with a packet
    containing its own node name.
7. Log node name in file and move to scanning the next IP.

"""
