import threading
import socket
import datetime

class Server:
    def __init__(self, host="127.0.0.1", buffer_size=1024, server_name = "SERVER",
                 exit_msg="/kill"):
        port = self.get_port()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        self.BUFFER_SIZE = buffer_size
        self.SERVER_NAME = server_name
        self.NICK_NAME_MESSAGE = "***NICK_NAME***"
        self.NICK_NAME_TAKEN = "***TAKEN***"
        self.NICK_NAME_ACCEPTED = "***ACCEPTED***"
        self.EXIT_MESSAGE = exit_msg
        open("chat_log.txt", "w").close()
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

    def server_write(self):
        # while True:
        #     try:
        #         message = input("")
        #         if message == self.EXIT_MESSAGE:
        #             raise Exception
        #         else:
        #             timestamp = datetime.datetime.now().strftime("%D %T")
        #             message = f"[{timestamp}] {self.SERVER_NAME}: {message}".encode("ascii")
        #             self.broadcast(message)
        #     except:
        #         timestamp = datetime.datetime.now().strftime("%D %T")
        #         self.broadcast(f"[{timestamp}] {self.SERVER_NAME}: The server is shutting down, all clients will be disconnected.".encode("ascii"))
        #         for client in self.clients:
        #             client.send(self.EXIT_MESSAGE.encode("ascii"))
        #             client.close()
        #         self.server.close()
        #         break
        while True:
            try:
                message = input("")
                if message == self.EXIT_MESSAGE:
                    if not self.clients:
                        raise Exception
                    else:
                        print("There are still clients connected, cannot shutdown.")
                else:
                    timestamp = datetime.datetime.now().strftime("%D %T")
                    message = f"[{timestamp}] {self.SERVER_NAME}: {message}".encode("ascii")
                    self.broadcast(message)
            except:
                print("Closing the server.")
                self.server.close()
                timestamp = datetime.datetime.now().strftime("%D %T")
                self.broadcast(f"[{timestamp}] {self.SERVER_NAME}: The server is shutting down.".encode("ascii"))
                break

    def broadcast(self, msg):
        for client in self.clients:
            client.send(msg)
        print(msg.decode("ascii"))
        with open("chat_log.txt", "a") as file:
            print(msg.decode("ascii"), file=file)

    def handle(self, client):
        while True:
            try:
                message = client.recv(self.BUFFER_SIZE)
                decoded_message = message.decode("ascii")

                if decoded_message == self.EXIT_MESSAGE:
                    print("Client requested disconnect.")
                    raise Exception
                
                timestamp = datetime.datetime.now().strftime("%D %T")
                message = f"[{timestamp}] {decoded_message}".encode("ascii")
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                nickname = self.nicknames[index]
                self.clients.remove(client)
                self.nicknames.remove(nickname)
                client.close()
                timestamp = datetime.datetime.now().strftime("%D %T")
                self.broadcast(f"[{timestamp}] {self.SERVER_NAME}: {nickname} left the chat.".encode("ascii"))
                print(f"{nickname} has disconnected.")

                # if not self.clients:
                #     print("All clients have disconnected. Shutting down the server.")
                #     self.server.close()

                break

    def receive(self):
        while True:
            try:
                client, address = self.server.accept()
                print(f"Connected with {str(address)}.")

                client.send(self.NICK_NAME_MESSAGE.encode("ascii"))
                nickname = client.recv(self.BUFFER_SIZE).decode("ascii")
                if nickname == self.SERVER_NAME or nickname in self.nicknames:
                    client.send(self.NICK_NAME_TAKEN.encode("ascii"))
                    client.close()
                    continue
                client.send(self.NICK_NAME_ACCEPTED.encode("ascii"))   
                self.nicknames.append(nickname)
                self.clients.append(client)

                print(f"nickname of the client is {nickname}")
                client.send(f"Welcome, you are connected to the server. \"{self.EXIT_MESSAGE}\" to exit.\n".encode("ascii"))
                timestamp = datetime.datetime.now().strftime("%D %T")
                self.broadcast(f"[{timestamp}] {self.SERVER_NAME}: {nickname} has joined the chat.".encode("ascii"))

                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
            except OSError:
                break
    
    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.server_write)
        write_thread.start()

if __name__ == "__main__":
    server = Server()
    server.run()