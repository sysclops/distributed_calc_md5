
import socket
import threading


class ClientThread(threading.Thread):
	def __init__(self, clientAddress, clientsocket):
		threading.Thread.__init__(self)
		self.csocket = clientsocket
		print ("New connection added: ", clientAddress)

	def run(self):
		print ("Connection from : ", clientAddress)
		hash = "EC9C0F7EDCC18A98B1F31853B1813301"
		per = 500000

		last = 0

		while True:
			core_num = self.csocket.recv(1024)
			print core_num
			if "String was found" in core_num:
				self.csocket.send("FINISHED")
				break
			to = (int(core_num) * per + last) - 1
			self.csocket.send(hash)
			self.csocket.recv(1024)
			self.csocket.send(str(last))
			self.csocket.recv(1024)
			self.csocket.send(str(to))

			last = to + 1
			print self.csocket.recv(1024)
			self.csocket.send("   ")
		print ("Client at ", clientAddress, " disconnected...")


LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
	server.listen(1)
	clientsock, clientAddress = server.accept()
	newthread = ClientThread(clientAddress, clientsock)
	newthread.start()
