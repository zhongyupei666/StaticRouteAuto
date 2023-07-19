try:
    from Createnode.node import Node
except ModuleNotFoundError:
    from node import Node
    
import copy

try:
    from Createnode.pict import NetworkPic
except ModuleNotFoundError:
    from pict import NetworkPic
    
class ConfigTable:
    def __init__(self,networkNet):
        self.IpAddressTable = []
        self.RouteTable = []
        self.networkNet = networkNet
    def CreateTable(self):    
        for i in self.networkNet.nodes:
            i.handleIPaddress()
            self.IpAddressTable.append({f"{i.name}":{"host":i.host,
                                                     "port":i.port,
                                                     "interface":i.address}})
        for i in range(self.networkNet.length):
            self.networkNet.Spanning_tree(i)
            self.networkNet.CreateStaticRouteTable(i)
            self.networkNet.liftLoop()
            mid = copy.deepcopy(self.networkNet.staticRoute)
            self.RouteTable.append(mid)
            self.networkNet.ClearTable()
            self.networkNet.Treeclear()
            
if __name__ == "__main__":
    pc = {"f0/0":"192.168.1.1/24","f1/0":"192.168.2.1 255.255.255.0","loopback 1":"1.1.1.1 255.255.255.255"}
    a = {"f0/0":"1.1.1.1 255.255.255.255","loopback 2":"2.2.2.2 255.255.255.255"}
    b = {"f0/1":"192.168.2.1/24","f0/0":"192.168.10.1/24"}
    c = {"loopback 1":"2.2.2.2 255.255.255.255"}
    d = {"loopback 1":"192.168.10.3/24"}
    e = {"f0/0":"192.168.1.2/24","f1/0":"192.168.3.2/24"}
    pcnode = Node("127.0.0.1","0",pc,"pc","Cisco","123123")
    anode = Node("127.0.0.1","1",a,"a")
    bnode = Node("127.0.0.1","2",b,"b")
    cnode = Node("127.0.0.1","3",c,"c")
    dnode = Node("127.0.0.1","4",d,"d")
    enode = Node("127.0.0.1","5",e,"e")
    li = [pcnode,anode,bnode,cnode,dnode,enode]
    for i in li:
        # 生成各个节点的网络地址
        i.createNetw()
    pict = NetworkPic(li)
    
    tableOne = ConfigTable(pict)
    tableOne.CreateTable()
    for i in tableOne.IpAddressTable:
        print(list(i.values())[0]["interface"])
    print("\n-------------------- Static Route Table ------------------------")
    print(tableOne.RouteTable)