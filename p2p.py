import socket
import threading
import sys
import time
import random
import binascii

class Server:
    connections = []
    
    performclientconnection = False
    def __init__(self,address = "0.0.0.0"):
        if address != "0.0.0.0":
            self.performclientconnection = True
            outsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            outsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            outsock.connect((address,10000))
            c,a = outsock.getpeername()
            self.connections.append(c)

        print("Server __init__")
        #every server needs to listen. this is to listen for the connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(('0.0.0.0',10000))
        sock.listen(1)
        
        while True:
            c,a = sock.accept()
            cThread = threading.Thread(target=self.handler,args=(c,a))
            cThread.daemon = True
            cThread.start()
            print(str(c))
            self.connections.append(c)
            print("{}:{} connected".format(str(a[0]),str(a[1])))

    def handler(self,c,a):
		#This gets once per client
        if self.performclientconnection:
            iThread = threading.Thread(target=self.sendMsg, args=(c,a))
            iThread.daemon = True
            iThread.start()
		
		#
        while True:
		# Run on every message in
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not data:
                print("{}:{} disconnected".format(str(a[0]), str(a[1])))
                self.connections.remove(c)
                c.close()
                break
				
    def sendMsg(self,sock):
        print("Client  sendMsg")
        while True:
            i = bytes(input(""),"utf-8")
            sock.send(i)
            print("sent",i)
'''
class Client:

    def sendMsg(self,sock):
        print("Client  sendMsg")
        while True:
            i = bytes(input(""),"utf-8")
            sock.send(i)
            print("sent",i)

    def __init__(self,address):
        print("Client __init__")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        print(str(address))
        sock.connect(address,10000))
        iThread = threading.Thread(target=self.sendMsg, args=(sock,))
        iThread.daemon = True
        iThread.start()
        while True:
            data = sock.recv(1024)
            if not data:
                break

if len(sys.argv) > 1:
	client = Client(sys.argv[1])
else:
	server = Server()
'''
if len(sys.argv) > 1:
    server = Server(sys.argv[1])
else:
    server = Server()
