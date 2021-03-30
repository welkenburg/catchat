import socket, sys

HOST = '192.168.100.82'
PORT = 502

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	mySocket.bind((HOST, PORT))
except socket.error:
	print("La liaison du socket à l'adresse choisie a échoué.")
	sys.exit()

while 1:
	print("Serveur prêt, en attente de requêtes ...")
	mySocket.listen(1)

	con, addr = mySocket.accept()
	print (f"[CONNECTED] {addr[0]}:{addr[1]}")
	con.send(bytes("Vous etes connecté au serveur Marcel. Envoyez vos messages.", "utf8"))
	msgClient = con.recv(1024).decode("utf8")
	while 1:
		print ("C>", msgClient)
		if msgClient.upper() == "END":
			break
		msgServeur = input("S> ")
		con.send(bytes(msgServeur, "utf8"))
		msgClient = con.recv(1024).decode("utf8")

	con.send("Au revoir !")
	print ("con interrompue.")
	con.close()

	ch = input("<R>ecommencer <T>erminer ? ")
	if ch.upper() =='T':
		break