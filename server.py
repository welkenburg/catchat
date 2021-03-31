#py 3.9
#author : welkenburg

import socket, sys, threading

HOST = '192.168.1.14'
PORT = 502

class client:
	def __init__(self, ide, username, addr, connection):
		self.id = ide					# int, id of the client
		self.username = username 		# str, username is sent during the first connection
		self.ip = addr					# tuple, ip adress and port
		self.connection = connection 	# connecion socket object to send and receive from the client

class server:
	def __init__(self, name, ip, port=502, clientMax=10):
		self.name = name				# str, server's name
		self.ip = ip					# str, server's ip adress
		self.port = port				# int, port you want to listen to
		self.clientMax = clientMax		# int, max number of users
		self.clients = []				# list of the users
		self.start()

	def start(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # new socket

		# try to create a server
		try:
			self.socket.bind((self.ip, self.port))
		except:
			raise "Le serveur n'a pas pu etre créé"

		# server created
		print("### Server Started ###")
		while 1:
			# listen for clients
			self.socket.listen(self.clientMax)

			# a client is trying to connect !
			con, addr = self.socket.accept()
			username = con.recv(1024).decode("utf8")
			newClient = client(0,username,addr, con)
			if len(self.clients) > 0:
				newClient = client(self.clients[-1].id + 1,username,addr, con)

			# client connected, creating a thread
			print (f"{newClient.username}#{newClient.id} connected with ip {addr[0]}:{addr[1]}")
			con.send(bytes(f"{newClient.id}", "utf8"))
			con.send(bytes(f"Bienvenue sur {self.name}. Vous Pouvez a present envoyer des messages !", "utf8"))
			self.clients.append(newClient)
			threading.Thread(target=self.handleConnection, args=(newClient,)).start()
			

	# case to case client handling 
	def handleConnection(self, client):
		running = True
		# listening for event
		while running:
			try:
				msg = client.connection.recv(1024).decode("utf8")
			# client closed the chat
			except ConnectionResetError:
				msg = f"{client.username} left the chat..."
				self.clients.remove(client)
				running = False
			except ValueError:
				msg = ""

			# client sent the exit() command
			if msg == "exit()":
				msg = f"{client.username} left the chat..."
				client.connection.send("Au revoir !")
				client.connection.close()
				running = False

			# an empty message means that the client sent junk 
			if msg != "":
				print(f"{client.username}> {msg} ")
				for user in self.clients:
					user.connection.send(bytes(f"{client.username}> {msg}", "utf8"))

if __name__ == "__main__":
	try:
		serv = server("LES COCHONOUX DU 31", HOST)
	except KeyboardInterrupt:
		print("server stoped !")