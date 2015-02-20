import socket
from threading import Thread
import time
from solver import log

class communicationThread(Thread):
    def __init__(self, serv):
        Thread.__init__(self)
        self.server = serv
        self.clientList = serv.clientList
        self.running = True
        print("Communication thread created. . .")

    
    def onMsgArrival(self, msg):
        raise NotImplementedError("Please implement this method")
    
    def run(self):
        print("Beginning communication thread loop. . .")
        while self.running:
            for client in self.clientList:
                for message in client.linesplit():
                    if message != None and message != "":
                        self.onMsgArrival(message)
                        #client.update(message)
            self.clientList = []
            time.sleep(0.5)
            



        
            
class workingThread(Thread):
    def __init__(self, serv):
        raise NotImplementedError("Please implement this interface")
    
    def run(self):
        raise NotImplementedError("Please implement this interface")
            

class clientObject(object):
    def __init__(self,clientInfo):
        self.sock = clientInfo[0]
        self.address = clientInfo[1]
        
    def linesplit(self):
        # untested
        sock_buffer = self.sock.recv(2048)
        done = False
        while not done:
            if "\n" in sock_buffer:
                (line, sock_buffer) = sock_buffer.split("\n", 1)
                yield line
            else:
                more = self.sock.recv(2048)
                if not more:
                    done = True
                else:
                    sock_buffer = sock_buffer+more
        if sock_buffer:
            yield sock_buffer
    
    def update(self,message):
        #print('Message received: '+message)
        #self.sock.send("ACK".encode())
        return

class Server(object):
    def __init__(self, port=22222):
        #configure and open the socket
        self.HOST = 'localhost'
        self.PORT = port
        self.BUFFSIZE = 1024
        self.ADDRESS = (self.HOST,self.PORT)
        self.clientList = []
        #key = input("Press enter to start the server. . .")
        self.running = True
        self.serverSock = socket.socket()
        self.serverSock.bind(self.ADDRESS)
        self.serverSock.listen(2)
        self.commThread = None
        self.workThread = None
        
    def startServer(self):
        print "Starting communication thread"
        self.commThread.start()
        print "Starting working thread"
        self.workThread.start()
        print("Awaiting connections. . .")
        while self.running:
            clientInfo = self.serverSock.accept()
            print("Client connected from {}.".format(clientInfo[1]))
            self.commThread.clientList.append(clientObject(clientInfo))
            time.sleep(0.2)

        self.serverSock.close()
        print("- end -")
    
def send_msg(address, msg):
    "send message to address"
    client_socket = socket.socket()
    client_socket.connect(address)
    client_socket.sendall(msg.encode())
    #client expecting response from the server.
    #print client_socket.recv(200)
    client_socket.close()
    
    


    
    