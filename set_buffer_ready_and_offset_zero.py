# SPDX-License-Identifier: AGPL-3.0-or-later
"""
HL-G1 Buffer Configuration & Zero Offset Setup
Configures buffering parameters and sets absolute zero offset
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
argp = argparse.ArgumentParser(description="Configure HL-G1 buffer and zero offset")
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

# Zero offset configuration
hlg.set_offset(0)  # Reset offset
current_measure = hlg.get_measurement()  # Get absolute position
hlg.set_offset(-current_measure)  # Compensate offset
print(f"Zero offset set to: {hlg.get_offset()/10000:.4f}mm")

# Buffer configuration
hlg.set_buffering_operation(False)  # Stop buffering first
hlg.set_buffering_rate(1)  # 1 sample per trigger
hlg.set_buffering_mode(True)  # Triggered mode
hlg.set_zero_set(1)  # Enable zero set
hlg.set_zero_set(0)  # Disable after enabling (toggle)

# Trigger configuration
hlg.set_accumulated_amount(3000)  # Max buffer capacity
hlg.set_trigger_point(300)  # Trigger at 300 samples
hlg.set_trigger_delay(0)  # No delay
hlg.set_trigger_conditions(0)  # Trigger on timing input

# Start buffering
hlg.set_buffering_operation(True)
print(f"Buffer status: {hlg.get_buffering_status()}")

# Reset timing input
hlg.set_timing_input(0)  # Ensure clean state

print(f"\nConfiguration completed in {time.time() - start_time:.2f} seconds")