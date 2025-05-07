

# HL-G1 Laser Marker Control Scripts

## 🚀 Quick Start Guide

## 1\. First-Time Setup

`pip install pyserial`

## 2\. Configuration Script

`python set_buffer_ready_and_offset_zero.py [-d PORT] [-b BAUDRATE]`

Example:

`python set_buffer_ready_and_offset_zero.py -d COM4 -b 115200`

## 3\. Measurement Trigger

`python start_measurement_by_serial_trigger.py`

## 4\. Data Collection

`python readout_buffer_over_serial.py output_data.txt`

## 🔧 Script Reference

| Script | Purpose | Key Parameters |
| :---- | :---- | :---- |
| `set_buffer_ready...` | Configures buffer | `-d` Serial port `-b` Baud rate |
| `start_measurement...` | Starts acquisition | None |
| `readout_buffer...` | Saves measurements | `output_file` (required) |

## 🛠️ Troubleshooting

*`# Check available ports:`*  
`python -m serial.tools.list_ports`

## 📊 Expected Output

`2023-07-15 14:30:45 INFO     Buffer status: 3`  
`2023-07-15 14:30:46 INFO     Saved 1500 measurements`

