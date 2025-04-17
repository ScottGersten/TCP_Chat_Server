import threading
import socket
import datetime

# Class to represent the server
class Server:
    # Use the local host, 1024 bytes per buffer, and default values for 
    # the server name and termination message
    def __init__(self, host="127.0.0.1", buffer_size=1024, server_name = "SERVER",
                 exit_msg="/kill", logfile="chat_log.log"):
        
        # Get the TCP Port number from the user
        port = self.get_port()

        # Create a TCP socket for the server using local host and the chosen TCP port
        # Set the server to listen for client connections
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

        # Create empty lists to hold the client objects and their alliases
        self.clients = []
        self.nicknames = []

        # Set class constants
        self.BUFFER_SIZE = buffer_size
        self.SERVER_NAME = server_name
        self.NICK_NAME_MESSAGE = "***NICK_NAME***"
        self.NICK_NAME_TAKEN = "***TAKEN***"
        self.NICK_NAME_ACCEPTED = "***ACCEPTED***"
        self.EXIT_MESSAGE = exit_msg
        self.LOGFILE = logfile

        # Clear the chat log
        open(self.LOGFILE, "w").close()

        # Show the server is listening for clients
        print("The server is listening...")

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
                print("Enter an integer")

    # Allow the server to send messages and terminate
    # Operates in its own thread
    def server_write(self):
        # Loop until shutdown
        while True:
            # Get the message
            message = input("")

            # Message is calling for termination of server
            if message == self.EXIT_MESSAGE:
                # Only close server if all clients are disconnected
                if not self.clients:
                    print("Closing the server.")
                    self.server.close()
                    timestamp = datetime.datetime.now().strftime("%D %T")
                    self.broadcast(f"[{timestamp}] {self.SERVER_NAME}: The server is shutting down.".encode("ascii"))
                    break
                else:
                    print("There are still clients connected, cannot shutdown.")

            # Broadcast all other messages to clients
            else:
                timestamp = datetime.datetime.now().strftime("%D %T")
                message = f"[{timestamp}] {self.SERVER_NAME}: {message}".encode("ascii")
                self.broadcast(message)
            
    
    # Send a message to all connected clients
    def broadcast(self, msg):
        # Send to all clients
        for client in self.clients:
            client.send(msg)

        # Show message on server side
        print(msg.decode("ascii"))

        # Save messages to chat log
        with open(self.LOGFILE, "a") as file:
            print(msg.decode("ascii"), file=file)

    # Handle messages received from a client
    # Separate thread for each client connected
    def handle(self, client):
        # Loop until client shuts down
        while True:
            try:
                # Get message from a client
                message = client.recv(self.BUFFER_SIZE)
                decoded_message = message.decode("ascii")

                # See if the client is attempting to disconnect
                if decoded_message == self.EXIT_MESSAGE:
                    # Remove the client
                    raise Exception("Client requested disconnect.")
                # Send message to all clients
                # Use timestamps to show date and time
                timestamp = datetime.datetime.now().strftime("%D %T")
                message = f"[{timestamp}] {decoded_message}".encode("ascii")
                self.broadcast(message)

            # Close the client in case of an error
            except Exception as excp:
                # Show exception
                print(f"{excp}")

                # Find the client in list of clients and find its alias
                index = self.clients.index(client)
                nickname = self.nicknames[index]

                # Remove the client and its alias from the lists
                # close the client
                self.clients.remove(client)
                self.nicknames.remove(nickname)
                client.close()

                # Send a message detailing which client disconnected
                timestamp = datetime.datetime.now().strftime("%D %T")
                self.broadcast(f"[{timestamp}] {self.SERVER_NAME}: {nickname} left the chat.".encode("ascii"))
                print(f"{nickname} has disconnected.")
                break
    
    # Wait for connections from clients
    # Operates in its own thread
    def receive(self):
        # Loop until server shuts down
        while True:
            try:
                # Accept the client connection on the same TCP port
                client, address = self.server.accept()
                print(f"Connection found on {str(address)}.")

                # Ask the client to set an alias
                client.send(self.NICK_NAME_MESSAGE.encode("ascii"))
                nickname = client.recv(self.BUFFER_SIZE).decode("ascii")

                # If alias already exists, terminate connection with client
                if nickname == self.SERVER_NAME or nickname in self.nicknames:
                    client.send(self.NICK_NAME_TAKEN.encode("ascii"))
                    client.close()
                    continue

                # If alias checks out, allow client to begin writing
                client.send(self.NICK_NAME_ACCEPTED.encode("ascii"))   
                self.nicknames.append(nickname)
                self.clients.append(client)

                # Show client's nickname server side
                # Give the client a welcome message
                print(f"nickname of the client is {nickname}")
                client.send(f"Welcome, you are connected to the server. \"{self.EXIT_MESSAGE}\" to exit.\n".encode("ascii"))

                # Broadcast the new client joining to all clients
                timestamp = datetime.datetime.now().strftime("%D %T")
                self.broadcast(f"[{timestamp}] {self.SERVER_NAME}: {nickname} has joined the chat.".encode("ascii"))

                # Open a new thread for each client that connects
                # which handles each client's messages in its own thread
                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
            
            # When the server closes it will attempt to look for connections on
            # a now closed port, close this thread when that occurs
            except OSError:
                break
    
    # Send messages from the server, and receive connections at the same time
    # by having a thread for each
    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.server_write)
        write_thread.start()

# Instantiate server class and start threads
if __name__ == "__main__":
    server = Server()
    server.run()