import socket
import threading
import multiprocessing

#comment

class ClientProcess(multiprocessing.Process):
    '''
    A single thread of the clients

    Attributes:
    :csocket: The client socket
    '''

    def __init__(self, clientAddress, clientsocket):
        multiprocessing.Process.__init__(self)
        self.csocket = clientsocket
        self.to = 0
        self.last = 0
        print ("New connection added: ", clientAddress)
        '''
        The function that runs through each connected client
        '''
    def run(self):

        print ("Connection from : ", clientAddress)
        hash = "b5a1382b577b8c190031534841b70dd0"
        per = 500000

        #last = 0

        while True:
            core_num = self.csocket.recv(1024)
            print core_num
            if "String was found" in core_num:
                self.csocket.send("FINISHED")
                break
            self.to = (int(core_num) * per + self.last) - 1
            self.csocket.send(hash)
            self.csocket.recv(1024)
            self.csocket.send(str(self.last))
            self.csocket.recv(1024)
            self.csocket.send(str(self.to))

            self.last = self.to + 1
            print self.csocket.recv(1024)
            self.csocket.send("   ")
        print ("Client at ", clientAddress, " disconnected...")


LOCALHOST = "127.0.0.1"
PORT = 8080
last = 0
to = 0
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientProcess(clientAddress, clientsock)
    newthread.start()
