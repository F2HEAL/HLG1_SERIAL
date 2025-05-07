# SPDX-License-Identifier:  AGPL-3.0-or-later
#

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
argp.add_argument("-b", "--baud", default=230400, type=int, help="default: 230400")
args = argp.parse_args()

start_time = time.time()

hlg = HLG1(args.serial_device, args.baud)


hlg.get_timing_input()
hlg.set_timing_input(1)
hlg.get_timing_input()

print()
print("Program ran in", (time.time() - start_time), "seconds")
