import heapq
import random

class Message:
    def __init__(self, messageId, src, dest, messageType, time):
        self.messageId = messageId
        self.src = src
        self.dest = dest
        self.messageType = messageType
        self.time = time
     
    def __str__(self):
        return '[' + str(self.messageId) + ', ' + str(self.src) + ', ' + str(self.dest) + ', ' + self.messageType + ']' 
    
    def __eq__(self, otherMessage):
        return self.messageId == otherMessage.messageId
        
                      
class Node (object):
    def __init__(self, nid, name = ''):
        self.nodeId = nid
        self.name = name
        self.sendQ = []
        self.recvQ = []
        self.recvFunc = None
        self.network = None
        
        self.alive = True
         
    def getId(self):
        return self.nodeId
    
    def getSendQ(self):
        return self.sendQ
        
    def getRecvQ(self):
        return self.recvQ
            
    def cycle(self, time):
        pass
        
        
    def sendMessage(self, to, message):
        delay = random.randint(1, self.network.maxLatency)
        self.sendMessageD(to, message, delay)


    def sendMessageD(self, to, message, delay):
        if not self.alive: return
        
        #if self.network.debug: 
            #print 'Time:', self.network.getCurrentTime(), 'Node', self, 'Send', message, 'to', to, 'delay', delay 
        heapq.heappush(self.sendQ, (self.network.getCurrentTime() + delay, to, message))
    
    
    def recvMessage(self, frm, message, time):
        if not self.alive: return                        
        #if self.network.debug:
            #print 'Time:', self.network.getCurrentTime(), 'Node', self, 'Receive', message, 'from', frm
                
    def isAlive(self):
        return self.alive
        
    def failed(self):
        self.alive = False
    
    def recovered(self):
        self.alive = True
        self.sendQ = []
        self.recvQ = []
    
    def __repr__(self):
        return str(self.nodeId)
                   
    def __str__(self):
        if self.name != '':
            return self.name
        else:
            return '' + str(self.nodeId)     
     
    def __eq__(self, anotherNode):
       return self.nodeId == anotherNode.nodeId
       
       
        
        
class Network:
    def __init__(self):
        self.nodes = {}
        self.endTime = 0
        self.currentTime = 0
        
        self.debug = True
        self.maxLatency = 10
        random.seed(0)
    
    def addNode(self, node):
        if not node.nodeId in self.nodes:
            self.nodes[node.nodeId] = node 
            node.network = self 
        else:
            raise Error('Node with the same Id exists!!!')
                  
    def cycle(self, time):
        
        nodelist = self.nodes.values()
        random.shuffle(nodelist)
        
        # Receive Loop
        for node in nodelist:
            if node.isAlive() and len(node.getRecvQ()) > 0:                
                while len(node.getRecvQ()) > 0:
                    frm, msg = node.getRecvQ().pop(0)
                    node.recvMessage(frm, msg, time)
                   
           
        # Each node cycle
        random.shuffle(nodelist)        
        for node in nodelist:
            if node.isAlive():
                node.cycle(time)                        
                        
        # Transfer Loop
        random.shuffle(nodelist)
        for node in nodelist:
            # Check if node has non-empty message queue. If so, transfer them
            if node.isAlive() and len(node.getSendQ()) > 0:
                while len(node.getSendQ()) > 0 and node.getSendQ()[0][0] <= self.getCurrentTime(): 
                    time, to, msg = heapq.heappop(node.getSendQ())
                    if (to.isAlive()) : to.getRecvQ().append((node, msg)) 
    
    def run(self):
        for time in range(self.endTime):
            self.currentTime = time
            self.cycle(time)
            
        self.currentTime = self.endTime    
        self.cycle(self.endTime)           
    
    def getCurrentTime(self):
        return self.currentTime
                


class Simulator:
    def __init__(self):
        self.network = Network()                
    
    def addNode(self, node):
        self.network.addNode(node)
    
    def addNodes(self, nodes):
        for node in nodes:
            self.network.addNode(node)
                
    def setEndTime(self, endTime):
        self.network.endTime = endTime
    
    def run(self):
        self.network.run()
                    
