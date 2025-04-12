import threading
import socket

class Server:
    def __init__(self, host="127.0.0.1", port=55555, buffer_size=1024):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        self.buffer_size = buffer_size
        print("The server is listening")

    def broadcast(self, msg):
        for client in self.clients:
            client.send(msg)
    

    def handle(self, client):
        while True:
            try:
                message = client.recv(self.buffer_size)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                client.remove(self.clients)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f"{nickname} left the chat".encode("ascii"))
                self.nicknames.remove(nickname)
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            client.send("***NICK_NAME***".encode("ascii"))
            nickname = client.recv(self.buffer_size).decode("ascii")
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f"nickname of the client is {nickname}")
            client.send("Welcome, you are connected to the server. \"/kill\" to exit".encode("ascii"))
            self.broadcast(f"{nickname} has joined the chat".encode("ascii"))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

if __name__ == "__main__":
    server = Server()
    server.receive()