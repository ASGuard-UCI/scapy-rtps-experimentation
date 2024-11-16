#!/usr/bin/bash

HOME_DIR="/home/fayzah/scapy-rtps-experimentation"
export $(cat $HOME_DIR/.env) && $HOME_DIR/.venv/bin/python3 $HOME_DIR/amplification_vulnerability.py