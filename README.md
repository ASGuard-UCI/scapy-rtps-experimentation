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

9. To replicate the amplification vulnerability discussed by the TrendMicro
   researchers, run `python3 amplify.py` while having the listener node running.
   This should cause the listener node to start sending ACKNACK and HEARTBEAT
   packets to the IP address associated with the variable `HONEYPOT_IP` in
   `common.py`.

## Further Developments

While this allows us to obtain the IP address of a ROS 2 node, we still need to
to obtain information about its name and the topic(s) it publishes or is
subscribed to. To do this, one of the possible methods we are looking into is
to replicate the initial packet interaction between the talker and listener
nodes. During this interaction, the nodes will send their names to each other.

Specifically, the honeypot should respond with an ACKNACK packet if it receives
an ACKNACK packet from a ROS 2 node. The code for sending this packet is
available in `acknack.py`. Similarly. it should respond with a HEARTBEAT packet
if it receives a HEARTBEAT packet instead. The code for this packet can be
found in `heartbeat.py`. Lastly, after this series of packets, the honeypot
should send a packet containing its name, which would then cause the listener
node to respond with a packet containing its name. The code for this can be
found in `topic_data.py`.
