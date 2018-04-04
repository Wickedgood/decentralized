import socket
import threading
import sys
import time
import random
import binascii


class Server:

    connections = []
    peers = []

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(('0.0.0.0',10000))
        sock.listen(1)
        print("Server running...")
        while True:
            c,a = sock.accept()
            cThread = threading.Thread(target=self.handler,args=(c,a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append(a[0])
            print("{}:{} connected".format(str(a[0]),str(a[1])))
            self.sendPeers()

    def handler(self,c,a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not data:
                print("{}:{} disconnected".format(str(a[0]), str(a[1])))
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break
    def sendPeers(self):
        p = ""
        for peer in self.peers:
            p = p+peer + ","
        for connection in self.connections:
            connection.send(b'\x11' + bytes(p,"utf-8"))

class Client:

    def sendMsg(self,sock):
        while True:
            sock.send(bytes(input(""),"utf-8"))

    def __init__(self,address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        sock.connect((address,10000))
        iThread = threading.Thread(target=self.sendMsg, args=(sock,))
        iThread.daemon = True
        iThread.start()
        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':
                print("update Peers")
                self.updatePeers(data[1:])
            else:
                print(data.decode("utf-8"))

    def updatePeers(self,peerData):
        p2p.peers = str(peerData,"utf-8").split(",")[:-1]

class p2p:
    peers = ['127.0.0.1']

while True:
    try:
        print("Trying to connect ...")
        time.sleep(random.randint(1,5))
        for peer in p2p.peers:
            try:
                client = Client(peer)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            try:
                server = Server()
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print("Couldn't start the server")
    except KeyboardInterrupt:
        sys.exit(0)
