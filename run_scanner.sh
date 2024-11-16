#!/usr/bin/bash

HOME_DIR="/home/fayzah/scapy-rtps-experimentation"

export $(cat $HOME_DIR/.env)
zmap -p 11311 -r 1 0.0.0.0/0 | $HOME_DIR/.venv/bin/python3 $HOME_DIR/amplification_vulnerability.py