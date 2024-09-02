import socket
import struct

# Define UDP host and port
udp_host = ''
udp_port = 2828

# Create a UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Bind the socket to the host and port
    s.bind((udp_host, udp_port))
    print(f"Listening for UDP packets on port {udp_port}...")

    # Listen for incoming data
    while True:
        # Receive data from the socket
        data, addr = s.recvfrom(1024)  # Buffer size is 1024 bytes
        # Unpack the received data assuming it's double precision floating point numbers
        unpacked_data = struct.unpack('!' + 'd' * (len(data) // struct.calcsize('d')), data)
        # Print the received data
        print("Received data:", unpacked_data)
