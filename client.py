import socket
import threading

class Client:
    def __init__(self, host="127.0.0.1", port=55555, buff_size=1024,
                 nick_name_msg="***NICK_NAME***", exit_msg = "/kill"):
        self.nickname = input("Choose a nickname: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.BUFFER_SIZE = buff_size
        self.NICK_NAME_MESSAGE = nick_name_msg
        self.EXIT_MESSAGE = exit_msg

    def receive(self):
        while True:
            try:
                message = self.client.recv(self.BUFFER_SIZE).decode("ascii")
                if message == self.NICK_NAME_MESSAGE:
                    self.client.send(self.nickname.encode("ascii"))
                else:
                    print(message)
            except:
                print("You have disconnected from the server.")
                self.client.close()
                break
    
    def write(self):
        while True:
            #message = f"{self.nickname}: {input("")}"
            message = input("")
            if message == self.EXIT_MESSAGE:
                self.client.send(self.EXIT_MESSAGE.encode("ascii"))
                self.client.close()
                break
            else:
                self.client.send(f"{self.nickname}: {message}".encode("ascii"))

    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

if __name__ == "__main__":
    client = Client()
    client.run()