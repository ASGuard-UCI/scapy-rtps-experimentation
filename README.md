# `scapy` RTPS Experimentation

## Prerequisites

To experiment with RTPS for the purpose of our project, the following software
must be installed:

- **Python 3.10 or later**
- **Some virtual machine software:** while the code here has only been tested
  using VMWare Workstation Pro, it should also work on Workstation Player and
  even VirtualBox.

## Setup

1. Set up two virtual machines in a NAT network running Ubuntu 22.04. It is
   important that version 22.04 should be used because our project uses ROS 2
   Humble, which explicitly requires 22.04.

2. After going through the set up for each VM, set up ROS 2 Humble by following
   the instructions outlined in the [documentation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html).

   **Make sure to install `ros-humble-desktop` rather than `ros-humble-ros-base`
   as the talker/listener example programs will be needed later.**

   Ensure that after installation, that `ros2 run demo_nodes_cpp talker` can be
   run on one VM, `ros2 run demo_nodes_cpp listener` can be run on the other, and
   output appears on both terminals. Moving forward, the VM that is running the
   talker node will be denoted as the _talker VM_ and the VM running the listener
   node will be denoted as the _listener VM_.

3. On one of the virtual machines, install Wireshark. The Ubuntu package repository
   does not have the latest version of Wireshark installed, but there is an official
   PPA contains the newest version:

```shell
sudo add-apt-repository ppa:wireshark-dev/stable
sudo apt install wireshark
```

4. Now to see the network packets that are sent on the NAT network, run
   Wireshark, the talker node on the talker VM and the listener node on the
   listener VM. Set the packet filter in Wireshark to `rtps`, as ROS 2's
   middleware, the Data Distribution Service, uses the Real Time Publish Subscribe
   (RTPS) protocol underneath.

5. Clone this repository on your host machine.

6. Create a virtual environment by running `python3 -m venv [VENV_NAME]` and
   activate it by running `source [VENV_NAME]/bin/activate` on Unix-based
   machines or `.\[VENV_NAME]\Scripts\activate` on Windows machines.

7. Install the Python `scapy` package by running `pip install scapy`.

8. In `common.py`. update the value of `LISTENER_IP` to the IP address of the
   listener VM. This can be found by running `hostname -I` on the VM.

9. A server that uses a tool such as `tcpdump` should be set up so that it can
   receive the traffic that is triggered by the amplification vulnerability.
   Cloud computing platforms such as Amazon Web Services or Google Cloud
   Platform offer such servers. From this point forward, this server will be
   denoted as a **collector**.

10. Obtain the **public** IP address of the collector and update the
    `COLLECTOR_IP` to this IP. By doing this, the amplified packets will be
    sent to the collector.

11. To replicate the amplification vulnerability discussed by the TrendMicro
    researchers, run `python3 amplify.py` while having the listener node running.
    This should cause the listener node to start sending ACKNACK and HEARTBEAT
    packets to the collector. Make sure to have `tcpdump` running to capture
    the packets.

## Scanning the IPv4 Space

A [fork of ZMap](https://github.com/ASGuard-UCI/zmap/) has been created that
prunes the packet sending functionality so that only the IP generation remains
and output each IP address generated without any additional logging statements.
With this slimmer version of ZMap, it is possible to pipe its IP generation
output into this Python program so that RTPS packets can be sent to the desired
IPv4 subnets. For example:

```sh
zmap 1.2.3.4/32 | python amplification_vulnerability.py
```

Note that since this fork has been modified, it requires building from source.
Please refer to the
[INSTALL.md](https://github.com/ASGuard-UCI/zmap/blob/main/INSTALL.md) file to
build and install it.

## Further Developments

While this allows us to obtain the IP address of a ROS 2 node, we still need to
to obtain information about its name and the topic(s) it publishes or is
subscribed to. One way this might work is to do this is to replicate the initial
handshake process between the talker and listener nodes, using a Python
`systemctl` service on the collector to send packets back to the listener. This
way, we will be able to find out more about the ROS 2 system under investigation.
