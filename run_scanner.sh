#!/usr/bin/bash

HOME_DIR="$HOME/scapy-rtps-experimentation"

# This script requires usage of our ZMap fork located at ASGuard-UCI/zmap
# instead of the original ZMap.
zmap 0.0.0.0/0 | $HOME_DIR/.venv/bin/python3 $HOME_DIR/amplification_vulnerability.py