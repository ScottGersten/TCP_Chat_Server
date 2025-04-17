# Scott Gersten
# YL91135
# sgerste1@umbc.edu
# client.py

import socket
import threading

# Class to represent the client
class Client:
    # Use the local host, 1024 bytes per buffer, and default termination message
    def __init__(self, host="127.0.0.1", buff_size=1024, exit_msg = "/kill"):

        # Get the TCP port and alias from user
        port = self.get_port()
        self.nickname = self.get_nick_name()

        # Create a TCP socket for the client using local host and the chosen TCP port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Flag to show if connection to server is valid
        self.connected = True

        # Attempt to connect to server using local host and chosen TCP port
        try:
            self.client.connect((host, port))
        
        # If there are no clients on TCP port, close the client
        except OSError:
            # Flag stops the write thread from automatically starting
            self.connected = False
            print("No server found on TCP port, closing client.")

        # Set class constants
        self.BUFFER_SIZE = buff_size
        self.NICK_NAME_MESSAGE = "***NICK_NAME***"
        self.NICK_NAME_TAKEN = "***TAKEN***"
        self.NICK_NAME_ACCEPTED = "***ACCEPTED***"
        self.EXIT_MESSAGE = exit_msg

    # Get the alias from the user with error checking
    @staticmethod
    def get_nick_name():
        nickname = ""
        # Ensure alias is not just whitespace as it crashes server
        while not nickname.strip():
            nickname = input("Choose a nickname: ")
            if not nickname.strip():
                print("Cannot enter whitespace for name.")
        return nickname

    # Get the TCP port from the user with bounds and error checking
    @staticmethod
    def get_port():
        while True:
            port = input("Enter the port number [1025, 65535]: ")
            try:
                # Ensure port number is an int
                port = int(port)
                # Ensure port number is in [1025, 65535]
                if port >= 1025 and port <= 65535:
                    return port
                else:
                    print("Port must be in range [1025, 65535].")
            except:
                print("Enter an integer.")

    # Allows the client to receive messages from the server
    # Operates in its own thread
    def receive(self):
        # Loop until shutdown
        while True:
            try:
                # Wait for a message from the server
                message = self.client.recv(self.BUFFER_SIZE).decode("ascii")

                # Send alias if server requests nickname
                if message == self.NICK_NAME_MESSAGE:
                    self.client.send(self.nickname.encode("ascii"))

                # Terminate connection if server says nickname is in use
                elif message == self.NICK_NAME_TAKEN:
                    print("Nickname taken, terminating connection.")
                    self.client.send(self.EXIT_MESSAGE.encode("ascii"))
                    # Raise exception to terminate connection
                    raise Exception
                
                # Start the write thread if the server accepts the nickname
                elif message == self.NICK_NAME_ACCEPTED:
                    write_thread = threading.Thread(target=self.write)
                    write_thread.start()

                # Print any other message that is linked to certain behavior
                else:
                    print(message)

            # If write thread terminates the connection, catch exception to
            # close the receive thread gracefully
            except Exception:
                print("You have disconnected from the server.")
                self.client.close()
                break
    
    # Allows the client to send messages to the server
    # Operates in its own thread
    def write(self):
        # Loop until shutdown
        while True:
            # Get client's message from user
            message = input("")

            # Terminate client connection on request
            if message == self.EXIT_MESSAGE:
                self.client.send(self.EXIT_MESSAGE.encode("ascii"))
                self.client.close()
                break

            # Otherwise send message to the server
            else:
                self.client.send(f"{self.nickname}: {message}".encode("ascii"))


    # Start only the receive thread
    # Server certifying nickname will start write thread
    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

# Instantiate client class and start thread
# Only start thread if the TCP connection is valid
if __name__ == "__main__":
    client = Client()
    if client.connected:
        client.run()