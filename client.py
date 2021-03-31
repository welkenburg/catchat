import socket, sys, threading
from utils import UI
from config import CONFIG

class UI:
    status = {
        "s": "STATUS",
        "m": "MESSAGE",
        "e": "ERROR"
    }

    def show(self, type, msg):
        print(f"[{self.status[type]}] {msg}")

class Client:
    
    def __init__(self, username, host, port):
        self.username = username
        self.HOST = host
        self.PORT = port
        print(f"{self.HOST}:{self.PORT}")
        self.ENCODING = "utf8"
        self.ui = UI()
        self.__connect()
        threading.Thread(target=self.listenSend).start()
        threading.Thread(target=self.__listen).start()
    
    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.HOST, self.PORT))
            self.ui.show("s", f"Connected to {self.HOST}:{self.PORT}")
        except socket.error:
            self.ui.show("e", "Connection failed")
            sys.exit()
        self.send(self.username)
        self.ui.show("m", self.__receive())

    def __receive(self):
        return self.socket.recv(1024).decode(self.ENCODING)

    def send(self, msg):
        self.socket.send(bytes(f"{msg}", self.ENCODING))
    
    def close(self):
        self.socket.close()
        self.ui.show("s", "Connection closed")
    
    def __listen(self):
        while True:
            if self.__receive() == "END":
                break
            if self.__receive() != "":
                self.ui.show("m", self.__receive())
        self.close()
    
    def listenSend(self):
        while True:
            m = input("msg: ")
            if m == "END":
                break
            self.send(m)

c = Client("welk", CONFIG["HOST"], CONFIG["PORT"])