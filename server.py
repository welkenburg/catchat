import socket, sys, asyncio

HOST = '192.168.100.82'
PORT = 502

class client:
	def __init__(self, ide, username, addr, connection):
		self.id = ide
		self.username = username
		self.ip = addr
		self.connection = connection

class server:
	def __init__(self, name, ip, port=502, clientMax=10):
		self.name = name
		self.ip = ip
		self.port = port
		self.clientMax = clientMax
		self.clients = []
		self.start()

	def start(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.socket.bind((self.ip, self.port))
		except:
			raise "Le serveur n'a pas pu etre créé"
		while 1:
			print("### Server Started ###")
			self.socket.listen(self.clientMax)

			con, addr = self.socket.accept()
			_, username = con.recv(1024).decode("utf8").split("\6")
			newClient = client(0,username,addr, con)
			if len(self.clients) > 0:
				newClient = client(self.clients[-1].id + 1,username,addr, con)

			# nom= "paul"
			# f"bonjour {nom}"
			print (f"new conncetion {addr[0]}:{addr[1]}")
			con.send(bytes(f"{newClient.id}", "utf8"))
			con.send(bytes(f"Bienvenue sur {self.name}. Vous Pouvez a present envoyer des messages !", "utf8"))
			self.clients.append(newClient)
			asyncio.run(self.handleConnection(newClient))
			

	async def handleConnection(self, client):
		running = True
		while running:
			try:
				ide, msg = client.connection.recv(1024).decode("utf8").split("\6")
				print(msg)
			except ConnectionResetError:
				return False
			if msg == "END":
				con.send("Au revoir !")
				con.close()
				running = False
				msg = f"{client.username} left the chat..."
			for user in self.clients:
				user.connection.send(bytes(f"yo", "utf8"))

serv = server("LES COCHONOUX DU 31", HOST)