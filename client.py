import socket
import threading
import sys

class Client:
    def __init__(self, host="127.0.0.1", buff_size=1024, exit_msg = "/kill"):
        port = self.get_port()
        self.nickname = self.get_nick_name()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = True
        try:
            self.client.connect((host, port))
        except:
            self.connected = False
            print("No server found on TCP port, closing client.")
        self.BUFFER_SIZE = buff_size
        self.NICK_NAME_MESSAGE = "***NICK_NAME***"
        self.NICK_NAME_TAKEN = "***TAKEN***"
        self.NICK_NAME_ACCEPTED = "***ACCEPTED***"
        self.EXIT_MESSAGE = exit_msg

    @staticmethod
    def get_nick_name():
        nickname = ""
        while not nickname.strip():
            nickname = input("Choose a nickname: ")
            if not nickname.strip():
                print("Cannot enter whitespace for name.")
        return nickname

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
                print("Enter an integer.")

    def receive(self):
        while True:
            try:
                message = self.client.recv(self.BUFFER_SIZE).decode("ascii")
                if message == self.NICK_NAME_MESSAGE:
                    self.client.send(self.nickname.encode("ascii"))
                elif message == self.NICK_NAME_TAKEN:
                    print("Nickname taken, terminating connection.")
                    self.client.send(self.EXIT_MESSAGE.encode("ascii"))
                    raise Exception
                elif message == self.NICK_NAME_ACCEPTED:
                    write_thread = threading.Thread(target=self.write)
                    write_thread.start()
                elif message == self.EXIT_MESSAGE:
                    #self.client.close()
                    raise Exception
                else:
                    print(message)
            except:
                print("You have disconnected from the server.")
                self.client.close()
                break
    
    def write(self):
        while True:
            try:
                message = input("")
                if message == self.EXIT_MESSAGE:
                    self.client.send(self.EXIT_MESSAGE.encode("ascii"))
                    self.client.close()
                    break
                else:
                    self.client.send(f"{self.nickname}: {message}".encode("ascii"))
            except:
                self.client.close()
                break

    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        # write_thread = threading.Thread(target=self.write)
        # write_thread.start()

if __name__ == "__main__":
    client = Client()
    if client.connected:
        client.run()