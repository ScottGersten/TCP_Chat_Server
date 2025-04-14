import threading
import socket

class Server:
    def __init__(self, host="127.0.0.1", buffer_size=1024, 
                 nick_name_msg="***NICK_NAME***", exit_msg="/kill"):
        port = self.get_port()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        self.BUFFER_SIZE = buffer_size
        self.NICK_NAME_MESSAGE = nick_name_msg
        self.EXIT_MESSAGE = exit_msg
        print("The server is listening...")

    @staticmethod
    def get_port():
        while True:
            port = input("Enter the port number [1025, 65535]: ")
            try:
                port = int(port)
                if port >= 1025 and port <= 65535:
                    return port
                else:
                    print("Port must be in range [1025, 65535].")
            except:
                print("Enter an integer")

    def broadcast(self, msg):
        # decoded_msg = msg.decode("ascii")
        # decoded_msg += "\n"
        # msg = decoded_msg.encode("ascii")
        for client in self.clients:
            client.send(msg)

    def handle(self, client):
        while True:
            try:
                message = client.recv(self.BUFFER_SIZE)
                decoded_message = message.decode("ascii")
                if decoded_message == self.EXIT_MESSAGE:
                    raise Exception("Client requested disconnect.")
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                nickname = self.nicknames[index]
                #client.remove(self.clients)
                self.clients.remove(client)
                self.nicknames.remove(nickname)
                client.close()
                self.broadcast(f"{nickname} left the chat.".encode("ascii"))
                print(f"{nickname} has disconnected.")

                if not self.clients:
                    print("All clients have disconnected. Shutting down the server.")
                    self.server.close()

                break

    def receive(self):
        while True:
            try:
                client, address = self.server.accept()
                print(f"Connected with {str(address)}.")

                client.send(self.NICK_NAME_MESSAGE.encode("ascii"))
                nickname = client.recv(self.BUFFER_SIZE).decode("ascii")
                self.nicknames.append(nickname)
                self.clients.append(client)

                print(f"nickname of the client is {nickname}")
                client.send(f"Welcome, you are connected to the server. \"{self.EXIT_MESSAGE}\" to exit.\n".encode("ascii"))
                self.broadcast(f"{nickname} has joined the chat.".encode("ascii"))

                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
            except OSError:
                break

if __name__ == "__main__":
    server = Server()
    server.receive()