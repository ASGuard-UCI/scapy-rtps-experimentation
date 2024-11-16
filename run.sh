#!/bin/bash/

$HOME_DIR="/home/fayzah/scapy-rtps-experimentation"
sudo zmap -p 7400 -r 1 0.0.0.0/0 | export $(cat $HOME_DIR/.env) && python3 $HOME_DIR/amplification_vulnerability.py