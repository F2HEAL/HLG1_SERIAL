# SPDX-License-Identifier:  AGPL-3.0-or-later
# Set New Zero Offset
# Set Trigger to start buffering


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

hlg.set_offset(0)

# read the abs. measurement and deduct it from the Offset to set abs. Zero here 
hlg.get_measurement()
hlg.get_offset()
hlg.set_offset(-hlg.get_measurement())
hlg.get_offset()
hlg.get_measurement()


hlg.get_buffering_operation()
hlg.set_buffering_operation(start=False)
hlg.get_buffering_operation()

hlg.set_buffering_rate(1)

hlg.get_buffer_rate()

hlg.get_sampling_cycle()

hlg.set_buffering_mode(triggered=True)

hlg.set_zero_set(1)
hlg.set_zero_set(0)


hlg.set_accumulated_amount(3000)
hlg.set_trigger_point(300)
hlg.set_trigger_delay(0)

# trigger by 
# +00000 At timing input ON
# +00001 At or higher than threshold
# +00002 Lower than threshold 
# +00003 At an alarm occurred
# +00004 At an alarm released
hlg.set_trigger_conditions(0)
#hlg.set_trigger_threshold(125)
hlg.get_trigger_conditions()

hlg.set_buffering_operation(start=True)
hlg.get_buffering_operation()
hlg.get_buffering_status()

# reset alarm
hlg.get_timing_input()
hlg.set_timing_input(0)
hlg.get_timing_input()

print()
print("Program ran in", (time.time() - start_time), "seconds")
