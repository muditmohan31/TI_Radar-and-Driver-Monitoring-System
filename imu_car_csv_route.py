import socket
import csv
import time
import keyboard

UDP_IP = "0.0.0.0"
UDP_PORT = 2828

# Field names for CSV headers
headers = [
    "timestamp", "accx", "accy", "accz", "gravaccx", "gravaccy", "gravaccz", "flag_mild_traffic", "flag_moderate_traffic", "flag_heavy_traffic"
]

# UDP setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

# CSV setup
csv_filename = "data.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

# Flags setup
flags = {
    "flag_mild_traffic": 0,
    "flag_moderate_traffic": 0,
    "flag_heavy_traffic": 0
}


# Function to toggle the flag state
def toggle_flag(fg):
    global flags
    flags[fg] = 1 if flags[fg] == 0 else 0


# Register key press and release event handlers
keyboard.on_press_key('a', lambda _: toggle_flag("flag_mild_traffic"))
keyboard.on_release_key('a', lambda _: toggle_flag("flag_mild_traffic"))
keyboard.on_press_key('s', lambda _: toggle_flag("flag_moderate_traffic"))
keyboard.on_release_key('s', lambda _: toggle_flag("flag_moderate_traffic"))
keyboard.on_press_key('d', lambda _: toggle_flag("flag_heavy_traffic"))
keyboard.on_release_key('d', lambda _: toggle_flag("flag_heavy_traffic"))

while True:
    try:
        lux, _ = sock.recvfrom(1024)
        lux_values = lux.decode().split(',')
        print(lux_values)
        # Make sure the received data has all the required fields
        if len(lux_values) == len(headers) - 4:  # Excluding timestamp and flags from the count
            timestamp = time.time()  # Get current timestamp
            lux_values.insert(0, str(timestamp))  # Insert timestamp at the beginning
            lux_values.extend(str(flags[flag]) for flag in flags)
            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(lux_values)
        else:
            print("Received incomplete data. Skipping.")
    except socket.error:
        pass

    # Check if 'q' key is pressed
    if keyboard.is_pressed('q'):
        break  # Break out of the loop if 'q' is pressed

