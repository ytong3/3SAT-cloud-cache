import network
import solver
from solver import log
from threading import Thread
import time
from collections import deque


class slaveServer(network.Server):
    def __init__(self, port=22222):
        network.Server.__init__(self,port=port)
        self.solver = solver.Solver()
        self.taskList = deque([])
        self.commThread = slaveCommThread(self)
        self.workThread = slaveWorkingThread(self)
        
class slaveCommThread(network.communicationThread):
    def onMsgArrival(self, message):
        #log(message)
        if message[0:3]=='NEW':
            (varNum, probStr) = message[4:].split(' ',1)
            self.server.taskList.append((varNum, probStr))
        if message[0:3]=='END':
            self.server.taskList.append('END')
         
class slaveWorkingThread(network.workingThread):
    "slave working thread"
    def __init__(self,serv):
        Thread.__init__(self)
        self.server = serv
        self.running = True
        
    def run(self):
        "handle the task in the task list and remove once it is done"
        while self.running:
            #taskList is queue storing the task tuples
            if len(self.server.taskList):
                task = self.server.taskList.popleft()
                log(task)
                                
                if task=='END':
                    self.running=False
                else:
                    #task is a tuple
                    self.server.solver.recursionSolve(int(task[0]),self.server.solver.problemStrToList(task[1]))
                    
            time.sleep(0.01)
 

#instantiate a solver
sServer = slaveServer(port = 22222)
#start the server
sServer.startServer()






