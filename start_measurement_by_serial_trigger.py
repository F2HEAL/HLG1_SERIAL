# SPDX-License-Identifier: AGPL-3.0-or-later
"""
HL-G1 Measurement Trigger Utility
Activates timing input to start buffered measurements
"""

import argparse
import time
import logging
from HLG1 import HLG1

# Configure logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

# Command line arguments
argp = argparse.ArgumentParser(description="Trigger HL-G1 measurements")
argp.add_argument("-d", "--serial_device", 
                 default="/dev/ttyUSB0", 
                 help="Serial port device (default: /dev/ttyUSB0)")
argp.add_argument("-b", "--baud", 
                 default=230400, 
                 type=int, 
                 help="Baud rate (default: 230400)")
args = argp.parse_args()

start_time = time.time()

# Initialize connection
hlg = HLG1(args.serial_device, args.baud)

# Check current timing input state
current_state = hlg.get_timing_input()
print(f"Current timing input state: {current_state}")

# Activate timing trigger
hlg.set_timing_input(1)  # Enable timing input
print(f"New timing input state: {hlg.get_timing_input()}")

print(f"\nTrigger activated in {time.time() - start_time:.2f} seconds")