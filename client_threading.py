from hashlib import md5
import socket
import threading
import multiprocessing

IP = "127.0.0.1"
PORT = 8080

'''
The function each thread runs

Attributes:
    :start: Start of the range
    :end: End of the range
    :hash: Original hash

'''
def thread_func(start, end, hash):

    for num in range(start, end):
        string = str(num)
        while len(string) < 10:
            string = "0" + string
        new_hash = encrypt_md5(string)
        mid = string
        if new_hash == hash:
            my_socket.send("String was found: " + string)
            break
        print mid + "\n" + t.getName() + " has just finished!"

'''
Encrpyting a string with MD5

Attributes:
    :string: The string which we want to encrypt
'''

def encrypt_md5(string):
    hash = md5()
    hash.update(string.encode('utf-8'))
    return hash.hexdigest()


my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((IP, PORT))

while True:
    my_socket.send(str(multiprocessing.cpu_count()))
    my_hash = my_socket.recv(1024)
    print my_hash
    my_socket.send("ok")
    start = int(my_socket.recv(1024))
    print str(start)
    my_socket.send("ok")
    end = int(my_socket.recv(1024))
    print str(end)

    list = []
    length = 5
    for i in range(length):
        t = threading.Thread(target=thread_func, args=(start*(i+1)/length, (end*(i+1))/length, my_hash))
        list.append(t)

    for t in list:
        t.start()

    for t in list:
        t.join()

    my_socket.send("Client is finished")
    finish = my_socket.recv(1024)
    print "Final response is: " + finish
    if finish == "FINISHED":
        break
