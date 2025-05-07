# SPDX-License-Identifier: AGPL-3.0-or-later
"""
HL-G1 Buffer Data Readout Utility
Reads measurement data from HL-G1 buffer and saves to file when buffer is ready
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

# Set up command line arguments
argp = argparse.ArgumentParser(description="Read HL-G1 buffer data to file")
argp.add_argument("-d", "--serial_device", 
                 default="/dev/ttyUSB0", 
                 help="Serial port device (default: /dev/ttyUSB0)")
argp.add_argument("-b", "--baud", 
                 default=115200, 
                 type=int, 
                 help="Baud rate (default: 115200)")
argp.add_argument("output_file", 
                 help="Output file path for measurement data")
args = argp.parse_args()

start_time = time.time()

# Initialize HL-G1 connection
hlg = HLG1(args.serial_device, args.baud)

# Check buffer status
buf_stats = hlg.get_buffering_status()

if buf_stats != "3":
    print(f"ERROR: Buffer not ready (status: {buf_stats})")
    print(f"Current trigger conditions: {hlg.get_trigger_conditions()}")
else:
    # Reset timing input before readout
    hlg.get_timing_input()
    hlg.set_timing_input(0)  # Disable timing input
    hlg.get_timing_input()  # Verify
    
    # Read all buffered data
    output = hlg.read_data()
    
    # Save to file (one measurement per line)
    with open(args.output_file, "w") as f:
        for measurement in output:
            f.write(f"{measurement}\n")

print(f"Program completed in {time.time() - start_time:.2f} seconds")