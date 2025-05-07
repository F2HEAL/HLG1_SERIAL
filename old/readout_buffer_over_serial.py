# SPDX-License-Identifier:  AGPL-3.0-or-later
import argparse
import time
import logging


from HLG1 import HLG1

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

argp = argparse.ArgumentParser()
argp.add_argument("-d", "--serial_device", default="/dev/ttyUSB0", help="default: /dev/ttyUSB0")
argp.add_argument("-b", "--baud", default=115200, type=int, help="default: 115200")
argp.add_argument("output_file", help="destination file")
args = argp.parse_args()

start_time = time.time()

hlg = HLG1(args.serial_device, args.baud)

buf_stats = hlg.get_buffering_status()

if buf_stats != "3":
    print("ERROR: Buffer is not ready, being = ", buf_stats)
    print(hlg.get_trigger_conditions())
else :
    hlg.get_timing_input()
    hlg.set_timing_input(0)
    hlg.get_timing_input()
    output = hlg.read_data()

    with open(args.output_file, "w") as f:
        for i in output:
            f.write(f"{i}\n")

print("Program ran in", (time.time() - start_time), "seconds")
