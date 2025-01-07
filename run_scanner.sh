#!/usr/bin/bash

HOME_DIR="/home/fayzah/scapy-rtps-experimentation"

zmap -p 11311 0.0.0.0/0 | $HOME_DIR/.venv/bin/python3 $HOME_DIR/amplification_vulnerability.py