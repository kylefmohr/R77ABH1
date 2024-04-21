## Interfacing with R77ABH1 77GHz Radar Sensor for Respiration and Heartbeat

This repo is meant to be a guide for anybody with the R77ABH1 Sensor that need to know how to interface with it. In searching the web, I have only been able to locate the Chinese language datasheet for this sensor. I ran that through Google Translate, and after a few hours of trial and error, I was able to get the sensor to work. 

There are 20 pins on the sensor, but we will only need three of them to read the data. I am using a USB to Serial adapter to connect to the sensor, but any microcontroller with a UART should work as well. 

The connection is simple:
| Computer      | Sensor |
| ----------- | ----------- |
| RX      | MD       |
| 5v   | 5v        |
| GND | GND       |

If you'd like to get going quickly, you can use the Python script in this repo to read the data from the sensor. Install the requirements in requirements.txt, change the serial port in the script to the one you are using, and run the script. If all goes well, after 30 seconds or so, you should see a live updating graph that looks something like this: ![matplotlib graph](https://github.com/kylefmohr/R77ABH1/assets/6644803/a4075c51-d842-45b7-bb57-10a294e8fcf0)

And the console output looks like this: 


```
Getting new packet...
Length: 65 bytes
Mode: 4
Time: 45 minutes
Number of TLVs: 1
Working condition: 1
Speed: 0.5 m/s
Distance: 0.0 m
Angle: 0.0°
Breathing Normal
--- TLV 1 ---
Distance: 0.6 m
Direction: 0°
Current state: 1
Respiration rate: 15
Heartbeat rate: 90
```

All data is in little endian format. 

It will output data at 115200 baud. The data packet is as follows:
| Packet | Size (bytes) | Description |
| ------ | ---- | ----------- |
| Beginning Identifier | 4 | This value will always be 0x53 0x59 0x54 0x43, meant to identify the start of the packet |
| Packet Length | 1 | The length of the packet, including the beginning identifier and the checksum |
| Mode | 1 | The mode of the sensor. 0x00 is Standby, 0x01 is Forward Wide-Area Detection Mode, 0x02 is Back Detection Mode, 0x03 is Forward Narrow Area Mode, and 0x04 is Forward Tracking Mode. I don't know how to change the mode, it is always 0x04 in my experience |
| Time | 2 | The time in minutes since the sensor was turned on |
| Number of TLV | 1 | The number of TLV packets in the data (I think this corresponds to the number of targets detected) |
| Working Condition | 1 | 0x01 is normal, 0x02 is standby, 0x03 is abnormal |
| Speed | 1 | The speed of the target, in units of 0.1m/s |
| Distance | 1 | The distance of the target, in units of 0.1m |
| Angle | 1 | The angle of the target, in units of 0.1 degrees |
| Current State | 1 | 0x01 is normal, 0x02 is abnormal |
| Reserved | 1 | Just discard this byte | 
| TLV Frame Number | 1 | The frame number of the TLV packet, starting at 0x01 |
| Target Distance | 1 | The distance of the target in this TLV packet, in units of 0.1m |
| Target Direction | 1 | The direction of the target in this TLV packet, in units of 0.1 degrees |
| Target State | 1 | 0x01 is normal, 0x02 is abnormal |
| Respiratory Rate | 1 | The respiratory rate of the target, in breaths per minute |
| Heart Rate | 1 | The heart rate of the target, in beats per minute |
| Respiration Curve | 20 | 20 bytes of data that shows a short history of the respiration rate |
| Heartbeat Curve | 20 | 20 bytes of data that shows a short history of the heartbeat rate |
| ----- | --- |(If there are multiple targets, there will be more data here, starting with the TLV Frame Number) |
| Checksum | 1 | CRC16 checksum of the packet |
| End Identifier | 2 | This value will always be 0xEE 0xEE, meant to identify the end of the packet |
