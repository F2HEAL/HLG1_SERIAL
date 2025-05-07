# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Panasonic HL-G1 Laser Marker Control Library
Provides serial communication interface for HL-G1 High-Function Type
"""

import serial
import logging
import sys

class HLG1:
    def __init__(self,
                 serial_device="/dev/ttyUSB0",
                 baud=230400,
                 id="01"):
        """
        Initialize HL-G1 connection
        Args:
            serial_device: Serial port (default: /dev/ttyUSB0)
            baud: Baud rate (default: 230400)
            id: Device ID (default: 01)
        """
        self.cmd_base = "%" + id + "#"
        try:
            self.serial = serial.Serial(serial_device, baud, timeout=1)
        except Exception as e:
            print(f"Failed to connect to device {serial_device}: {str(e)}")
            sys.exit(1)

        logging.info("Connected to " + self.serial.name)

    # --------------------------
    # Core Communication Methods
    # --------------------------
    def snd_cmd(self, cmd, sub_cmd="", sub_cmd_chr="+"):
        """Send formatted command to HL-G1"""
        cmd_full = self.cmd_base + cmd
        if sub_cmd:
            cmd_full += sub_cmd_chr + sub_cmd
        cmd_full += "**\r"
        logging.debug("Sending:" + cmd_full)
        self.serial.write(cmd_full.encode())

    def rcv_output(self):
        """Receive response from HL-G1 (until carriage return)"""
        x = " "
        result = bytes()
        while x != b"\r":
            x = self.serial.read(1)
            result += x
        logging.debug("Received:" + result.decode("ASCII"))
        return result

    def check_error(self, output):
        """Check for and log HL-G1 error codes"""
        if output[3:4] == b"!":
            error_code = output[4:6].decode("ASCII")
            logging.warning(f"Rcv Error {error_code} : ")
            # Error code explanations...
            return True
        return False

    # --------------------------
    # Basic Settings Commands
    # --------------------------
    def get_sampling_cycle(self):
        """Read sampling interval (200µs/500µs/1ms/2ms)"""
        self.snd_cmd("RSP")
        output = self.rcv_output()
        if self.check_error(output):
            return
        # ... implementation ...

    def get_shutter_time(self):
        """Read shutter time setting (Auto or fixed 00-31)"""
        self.snd_cmd("RFB")
        output = self.rcv_output()
        if self.check_error(output):
            return
        # ... implementation ...

    # --------------------------
    # Buffering Control Commands
    # --------------------------
    def get_buffering_mode(self):
        """Check buffering mode (Continuous/Trigger)"""
        self.snd_cmd("RBD")
        output = self.rcv_output()
        if self.check_error(output):
            return
        # ... implementation ...

    def set_buffering_mode(self, triggered=True):
        """Set buffering mode (False=Continuous, True=Trigger)"""
        cmd = "WBD"
        sub_cmd = "00001" if triggered else "00000"
        self.snd_cmd(cmd, sub_cmd)
        # ... implementation ...

    # --------------------------
    # Trigger Control Commands
    # --------------------------
    def get_trigger_conditions(self):
        """Read trigger condition (0-4)"""
        self.snd_cmd("RTR")
        output = self.rcv_output()
        if self.check_error(output):
            return
        # ... implementation ...

    def set_trigger_conditions(self, conditions):
        """Set trigger condition:
           0=Timing input, 1=Threshold exceeded, 3=Alarm occurred
        """
        self.snd_cmd("WTR", str(conditions).zfill(5))
        # ... implementation ...

    # --------------------------
    # Measurement Commands
    # --------------------------
    def get_measurement(self):
        """Read current displacement in mm (-950.0000 to +950.0000)"""
        self.snd_cmd("RMD")
        output = self.rcv_output()
        if self.check_error(output):
            return
        # ... implementation ...

    def read_data(self):
        """Read buffered measurement data (returns list of values)"""
        samples = self.get_last_datapoint()
        self.snd_cmd("RLA", str(1).zfill(5) + str(samples).zfill(5), "")
        # ... implementation ...

    # --------------------------
    # Alarm/Timing Commands
    # --------------------------
    def get_alarm_status(self):
        """Check alarm state (0=OFF, 1=ON)"""
        self.snd_cmd("ROA")
        output = self.rcv_output()
        if self.check_error(output):
            return
        # ... implementation ...

    def set_timing_input(self, set):
        """Enable/disable timing input (0=OFF, 1=ON)"""
        self.snd_cmd("WTI", str(set).zfill(5))
        # ... implementation ...

    # ... [remaining methods with similar comments] ...

# Special note for error handling
"""
Error Code Reference:
01 - Command error     02 - Address error
03 - Data error       04 - BCC error
11 - Communication    21 - Control flow
22 - Execution        31-33 - Buffering errors
"""
