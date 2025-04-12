import socket
import threading

class Client:
    def __init__(self, host="127.0.0.1", port=55555, buff_size=1024):
        self.nickname = input("Choose a nickname: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.buff_size = buff_size

    def receive(self):
        while True:
            try:
                message = self.client.recv(self.buff_size).decode("ascii")
                if message == "***NICK_NAME***":
                    self.client.send(self.nickname.encode("ascii"))
                else:
                    print(message)
            except:
                print("An error occurred")
                self.client.close()
                break
    
    def write(self):
        while True:
            message = f"{self.nickname}: {input("")}"
            self.client.send(message.encode("ascii"))

    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

if __name__ == "__main__":
    client = Client()
    client.run()