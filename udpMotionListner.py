import socket
import time  # Import the time module

# Set the IP address and port to bind the UDP socket
host = "0.0.0.0"  # Listen on all available interfaces
port = 2390

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Add a delay before binding to the port
time.sleep(2)

# Bind the socket to the address and port
udp_socket.bind((host, port))

print(f"Listening for UDP messages on port {port}")

while True:
    try:
        # Receive data from the socket
        data, addr = udp_socket.recvfrom(1024)

        # Convert the received data to string
        message = data.decode("utf-8")

        # Print debug information
        print(f"Received message: {message} from {addr}")

        # Check if motion is detected
        if message == "1023":
            print("Movement Detected")
            udp_socket.sendto("Movement Detected\n".encode("utf-8"), addr)  # Send the response with a newline

    except Exception as e:
        # Print the exception for debugging
        print(f"Error: {e}")

