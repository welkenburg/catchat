import socket, sys, asyncio
from utils import UI
from config import CONFIG

class Client:
    
    def __init__(self, username, host, port):
        self.username = username
        self.HOST = host
        self.PORT = port
        self.ENCODING = "utf8"
        self.ui = UI()
        self.id = None
        self.__connect()
        asyncio.run(self.listenSend())
        self.__listen()
    
    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.HOST, self.PORT))
            self.ui.show("s", f"Connected to {self.HOST}:{self.PORT}")
        except socket.error:
            self.ui.show("e", "Connection failed")
            sys.exit()
        self.send(self.username)
        self.id = self.__receive()
        self.ui.show("m", self.__receive())

    def __receive(self):
        return self.socket.recv(1024).decode(self.ENCODING)

    def send(self, msg):
        self.socket.send(bytes(f"{self.id}\6{msg}", self.ENCODING))
    
    def close(self):
        self.socket.close()
        self.ui.show("s", "Connection closed")
    
    async def __listen(self):
        while True:
            if self.__receive() == "END":
                break
            if self.__receive() != "":
                self.ui.show("m", self.__receive())
        self.close()
    
    async def listenSend(self):
        while True:
            m = input("msg: ")
            if m == "END":
                break
            self.send(m)

c = Client("flo", CONFIG["HOST"], CONFIG["PORT"])