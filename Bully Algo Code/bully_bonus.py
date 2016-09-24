from network import *
import sys

# Driver node drives the simulation, does not participate in Election
class Driver(Node):
    def __init__(self, nodeId):
        Node.__init__(self, nodeId)
        self.hosts = []
    
    def cycle(self, time):
        Node.cycle(self, time)
        
        
        if time == 0:
            # Host 2 starts election
            start = Message(100, self, self.hosts[2], 'START', time)            
            self.sendMessage(self.hosts[2], start)
            
        if time == 100:
            # Highest ID node fails, and Host 1 starts Election
            self.hosts[len(self.hosts)-1].failed()
            start = Message(100, self, self.hosts[1], 'START', time)
            self.sendMessage(self.hosts[1], start)

        
        if time == 200:
            # Highest Id node recovers, and Host 1 initiates election
            self.hosts[len(self.hosts)-1].recovered()
            start = Message(100, self, self.hosts[1], 'START', time)
            self.sendMessage(self.hosts[1], start)
        
        
# Election participating Node or Process            
class Host(Node):    
    def __init__(self, nodeId):
        Node.__init__(self, nodeId)     
        self.hosts = []
        
        # Your code goes below
        self.counter = 1
        self.oddAnswer = []
        self.evenAnswer = []
        self.odd = False
        self.even = False
        
        
    def cycle(self, time):
        super(Host, self).cycle(time)
        
        # Your code goes below
        if time % 15 == 0:
            if self.nodeId % 2 == 0:
                for host in self.hosts:
                    #print self.nodeId, 'Testing', host.nodeId
                    if host == self: continue
                    if host.nodeId % 2 == 0:
                        mcast = Message(self.counter, self, host, 'ELECT', time)
                        self.sendMessage(host, mcast) 
                        self.counter = self.counter + 1
            else:
                for host in self.hosts:
                    #print self.nodeId, 'Testing', host.nodeId
                    if host == self: continue
                    if host.nodeId % 2 == 1:
                        mcast = Message(self.counter, self, host, 'ELECT', time)
                        self.sendMessage(host, mcast) 
                        self.counter = self.counter + 1
            #print 'self counter', self.counter
        
            
    def recvMessage(self, frm, message, time):
        super(Host, self).recvMessage(frm, message, time)
       
        # Your code goes below
      
        if message.messageType == 'START':
            self.counter = 1
            self.oddAnswer = []
            self.evenAnswer = []
            self.odd = False
            self.even = False
            print 'Starting Election by', self.nodeId
            
        if message.messageType == 'ELECT':
            print message.dest, 'got Electtion msg', message.messageId, 'at', time, 'from', message.src
            if message.src > message.dest:
                #print message.src, 'here', message.dest
                ans = Message(message.messageId, self, message.src, 'ANSWER', time)
                self.sendMessage(message.src, ans)
                #self.counter = self.counter + 1
            else:
                print message.dest, 'dropped Electtion msg', message.messageId, 'at', time, 'from', message.src
                
        if message.messageType == 'ANSWER':
            print message.dest, 'got Answer msg', message.messageId, 'at', time, 'from', message.src
            if self.nodeId % 2 == 0:
                self.evenAnswer.append(message.src)
            if self.nodeId % 2 == 1:
                self.oddAnswer.append(message.src)
                
        if len(self.oddAnswer) > len(self.hosts)/2 and self.nodeId % 2 == 1 and self.odd == False:
            print self.nodeId, 'Got ANSWER from', self.oddAnswer
            count = 0;
            for host in self.hosts:
                if host.nodeId % 2 == 1:
                    if host in self.oddAnswer:
                        count = count + 1
            if count == len(self.hosts)/2 - 1:
                print 'Node', self.nodeId, 'becomes the ODD Leader at', time
                for host in self.hosts:
                    if host == self: continue
                    if host.nodeId % 2 == 1 and host in self.oddAnswer:
                        print 'Node', host.nodeId, 'sets', self.nodeId, 'as ODD Leader'
                print 'Total Election Message', self.counter
                print '\n ****************** \n'
                self.odd = True
                #sys.exit(0)
        if len(self.evenAnswer) > len(self.hosts)/2 and self.nodeId % 2 == 0 and self.even == False:
            print self.nodeId, 'Got ANSWER from', self.evenAnswer
            count = 0;
            for host in self.hosts:
                if host.nodeId % 2 == 0:
                    if host in self.evenAnswer:
                        count = count + 1
            if count == len(self.hosts)/2 - 1:
                print 'Node', self.nodeId, 'becomes the EVEN Leader at', time
                for host in self.hosts:
                    if host == self: continue
                    if host.nodeId % 2 == 0 and host in self.evenAnswer:
                        print 'Node', host.nodeId, 'sets', self.nodeId, 'as EVEN Leader'
                print 'Total Election Message', self.counter
                print '\n ****************** \n'
                print 'Leader selection for partitioned Network done!!!'
                self.even = True
                sys.exit(0)
       
        #if self.odd == True and self.even == True:
            #print 'Leader selection for partitioned Network done!'
            #sys.exit(0)
            #print self.counter, 'counter'
            #sys.exit(0)


         
def main():
    sim = Simulator()
    sim.network.maxLatency = 20
    sim.network.debug = True
    
    driver = Driver(0)
    
    noOfNodes = 10
    hosts = [Host(i + 1) for i in range(noOfNodes)]

    print hosts
    
    driver.hosts = hosts
    for h in hosts:
        h.hosts = hosts
    
            
    sim.addNode(driver)    
    sim.addNodes(hosts)
    
    sim.setEndTime(1000)
    sim.run()
            

if __name__ == "__main__":
    main()
                
