import network
from threading import Thread
from collections import deque
from random import randint
from network import send_msg
from time import sleep
from solver import log

slaveAddress = 'localhost',22222



class masterServer(network.Server):
    def __init__(self,port = 22223):
        network.Server.__init__(self,port = port)
        self.slaveAddr = slaveAddress
        self.workThread = masterWorkingThread(self)
        self.commThread = masterCommThread(self)
        
class masterCommThread(network.communicationThread):
    def onMsgArrival(self,message):
        "do nothing at the master end"
        #log(message)

class masterWorkingThread(network.workingThread):
    def __init__(self, serv):
        Thread.__init__(self)
        self.running = True
        self.server = serv
    
    def problemGenerator(self):
        varNum = randint(3,12)
        clauseNum = randint(10,120)
        result=''
        for i in xrange(3*clauseNum):
            if randint(0,1):
                result = result+'-'
            
            result=result+str(randint(1,varNum))+','
        
        return str(varNum)+' '+result[:-1]
                
    
    def run(self):
        while self.running:
            #read file
            #line is expected to have the format: VarNum ProblemStr
            proMsg=""
            for i in xrange(100):
                proStr = self.problemGenerator()
                proMsg = proMsg+'NEW '+proStr+'\n'
            #log(proMsg)
            send_msg(self.server.slaveAddr, proMsg)
            sleep(60)
            
            
mServer = masterServer()
mServer.startServer()           
            


        
