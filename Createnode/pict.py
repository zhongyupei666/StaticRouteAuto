import copy
import xml.etree.ElementTree as ET2   
from  xml.dom.minidom import Document                                                              
try:
    from Createnode.node import Node
except ModuleNotFoundError:
    from node import Node
    
class NetworkPic:
    def __init__(self,nodelist):
        self.nodes = sorted(nodelist,key=Node.length,reverse=True)
        self.length = len(self.nodes)
        self.arry = self.CreateNums()
        self.recode = []
        self.staticRoute = {}
        self.midRouteValue = []
        
    def Spanning_tree(self,iindex):
        self.recode.append(iindex)
        while len(self.recode):
            index = self.recode.pop(0)
            rootnode = self.nodes[index]
            self.arry[index] = 1
            searchTable = rootnode.netw.values()
            for i in searchTable:
                for j in range(0,self.length):
                    if(i in self.nodes[j].netw.values()) and (self.arry[j] != 1) and (j != iindex):
                        self.arry[j] = 1
                        self.recode.append(j)
                        rootnode.next.append(self.nodes[j])
                        rootnode.indexnext.append(j)
        if 0 in self.arry.values():
            print("exist alone node.")
        self.arry = self.CreateNums()
    def ShowSpanningTree(self,nodeOne):
        print(nodeOne.name,end=" ")
        if len(nodeOne.next) == 0:
            return
        sizenums = len(nodeOne.next)
        for i in range(sizenums):
            mid = nodeOne
            nodeOne = nodeOne.next[i]
            self.ShowSpanningTree(nodeOne)
            nodeOne = mid
    def treeStaticRouteTable(self,nodeOne):
        for i,j in nodeOne.netw.items():
            self.midRouteValue.append(j)
        if len(nodeOne.next) == 0:
            return
        sizenums = len(nodeOne.next)
        for i in range(sizenums):
            mid = nodeOne
            nodeOne = nodeOne.next[i]
            self.treeStaticRouteTable(nodeOne)
            nodeOne = mid
    def CreateStaticRouteTable(self,index):
        midroute = []
        nodemid = copy.deepcopy(self.nodes[index])
        i = 0
        for j in nodemid.indexnext:
            nodetest = copy.deepcopy(self.nodes[j])
            self.treeStaticRouteTable(nodetest)
            midroute.append({f"{nodemid.netcard[i]}":list(set(self.midRouteValue))})    
            self.midRouteValue.clear()
            i += 1
        self.staticRoute[f"{nodemid.name}"] = midroute
    def Treeclear(self):
        for i in self.nodes:
            i.next.clear()   
            i.indexnext.clear()
    def ClearTable(self):
        self.staticRoute.clear()
    def show(self,index):
        nodetest = copy.deepcopy(self.nodes[index])
        self.ShowSpanningTree(nodetest)
    def CreateNums(self):
        arry = {}
        for i in range(self.length):
            arry[i] = 0
        return arry
    def liftLoop(self):
        host = list(self.staticRoute.keys())[0]
        newList = {}
        for i in self.staticRoute[host]:
            nitcard = list(i.keys())[0]
            for j in i[nitcard]:
                newList[f"{j}"] = nitcard
        self.staticRoute[host] = newList
    


if __name__ == "__main__":
    pc = {"f0/0":"192.168.1.1/24","f1/0":"192.168.2.1 255.255.255.0","loopback 1":"1.1.1.1 255.255.255.255"}
    a = {"f0/0":"1.1.1.1 255.255.255.255","loopback 2":"2.2.2.2 255.255.255.255"}
    b = {"f0/1":"192.168.2.1/24","f0/0":"192.168.10.1/24"}
    c = {"loopback 1":"2.2.2.2 255.255.255.255"}
    d = {"loopback 1":"192.168.10.3/24"}
    pcnode = Node("127.0.0.1","0",pc,"pc","Cisco","123123")
    anode = Node("127.0.0.1","1",a,"a")
    bnode = Node("127.0.0.1","2",b,"b")
    cnode = Node("127.0.0.1","3",c,"c")
    dnode = Node("127.0.0.1","4",d,"d")
    li = [pcnode,anode,bnode,cnode,dnode]
    for i in li:
        # 生成各个节点的网络地址
        i.createNetw()
    pict = NetworkPic(li)
    for i in range(pict.length):
        pict.Spanning_tree(i)
        pict.CreateStaticRouteTable(i)
        pict.liftLoop()
        print(pict.staticRoute)
        pict.ClearTable()
        pict.Treeclear()
    print("\n------------------------------")