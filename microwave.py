from serial import Serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Change `COM3` to the serial port that your sensor is connected to
ser = Serial('COM3', 115200)

# Initialize plot
fig, ax = plt.subplots()
line1, = ax.plot([], [], label="Respiration")
line2, = ax.plot([], [], label="Heartbeat")
ax.set_xlabel("Time (samples)")
ax.set_ylabel("Value")
ax.legend()

respiration_curve_values = []
heartbeat_curve_values = []
respiration_history = []
heartbeat_history = []
counter = 0

# Adjust this value to change the maximum number of samples displayed on the plot
max_history_length = 100 


def animate(i):
    global respiration_curve_values, heartbeat_curve_values
    data = ser.read(1)
    if data == b'\x53':  # Check for 'S' byte
        data = ser.read(1)
        if data == b'\x59':  # Check for 'Y' byte
            data = ser.read(1)
            if data == b'\x54':  # Check for 'T' byte
                data = ser.read(1)
                if data == b'\x43':  # Check for 'C' byte
                    print("Getting new packet...")

                    # Read the remaining header bytes
                    length = int.from_bytes(ser.read(1), byteorder='little')
                    mode = int.from_bytes(ser.read(1), byteorder='little')
                    time = int.from_bytes(ser.read(2), byteorder='little')
                    num_tlv = int.from_bytes(ser.read(1), byteorder='little')
                    work_con = int.from_bytes(ser.read(1), byteorder='little')
                    speed = int.from_bytes(ser.read(1), byteorder='little') / 10
                    distance = int.from_bytes(ser.read(1), byteorder='little') / 10
                    angle = int.from_bytes(ser.read(1), byteorder='little') / 10
                    normal_int = int.from_bytes(ser.read(1), byteorder='little')
                    reserved = ser.read(1)

                    # Print header information
                    print(f"Length: {length} bytes")
                    print(f"Mode: {mode}")
                    print(f"Time: {time} minutes")
                    print(f"Number of TLVs: {num_tlv}")
                    print(f"Working condition: {work_con}")
                    print(f"Speed: {speed} m/s")
                    print(f"Distance: {distance} m")
                    print(f"Angle: {angle}°")
                    if normal_int == 1:
                        print("Breathing Normal")
                    else:
                        print("Breating Abnormal")

                    
                    # Process TLV data
                    for _ in range(num_tlv):
                        tlv_id = int.from_bytes(ser.read(1), byteorder='little')
                        distance = int.from_bytes(ser.read(1), byteorder='little') / 10  # Convert to meters
                        direction = int.from_bytes(ser.read(1), byteorder='little')
                        current_state = int.from_bytes(ser.read(1), byteorder='little')
                        respiration_rate = int.from_bytes(ser.read(1), byteorder='little')
                        heartbeat_rate = int.from_bytes(ser.read(1), byteorder='little')
                        respiration_curve = ser.read(20)
                        heartbeat_curve = ser.read(20)

                        # Print TLV information
                        print(f"--- TLV {tlv_id} ---")
                        print(f"Distance: {distance} m")
                        print(f"Direction: {direction}°")
                        print(f"Current state: {current_state}")
                        print(f"Respiration rate: {respiration_rate}")
                        print(f"Heartbeat rate: {heartbeat_rate}")
                        respiration_curve_values = list(respiration_curve)  # Convert bytes to list of integers
                        heartbeat_curve_values = list(heartbeat_curve)
                        for value in respiration_curve_values:
                            respiration_history.append(value)
                            if len(respiration_history) > max_history_length:
                                respiration_history.pop(0)
                        for value in heartbeat_curve_values:
                            heartbeat_history.append(value)
                            if len(heartbeat_history) > max_history_length:
                                heartbeat_history.pop(0)
    
    
    line1.set_data(range(len(respiration_history)), respiration_history)
    line2.set_data(range(len(heartbeat_history)), heartbeat_history)
    

    ax.relim()
    ax.autoscale_view()
    return line1, line2


ani = animation.FuncAnimation(fig, animate, interval=100, blit=True)

plt.show()
