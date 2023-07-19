from Createnode.node import Node
from Createnode.pict import NetworkPic
from Createnode.table import ConfigTable
import telnetlib
import time

def ConfigDevice(hostname,portnum,loopbackdict,name):
    tn = telnetlib.Telnet(host=hostname,port=portnum)
    time.sleep(15)
    print(f"[+] {name} device setting ip address. ")
    tn.write(b"\r")
    tn.write(b"configure terminal\r")
    
    tn.write(b"line vty 0 14\r")
    tn.write(b"no privilege level 15\r")
    tn.write(b"exit\r")
    for i,j in loopbackdict.items():
        tn.write(f"interface {i}\r".encode("ascii"))
        tn.write(b"no shutdown\r")
        tn.write(f"ip address {j}\r".encode("ascii"))
        tn.write(b"exit\r")
    tn.write(b"end\r")
    tn.write(b"show ip interface brief\r")
    tn.write(b"exit\r")
    tn.write(b'\r')
    time.sleep(5)
    with open("configureIpAddressText",'a') as filename:
        filename.write(tn.read_very_eager().decode("utf-8"))
    print(f"[+] {name} ip address set is over.")
    tn.close()
    
    
def ConfigStaticRoute(hostnum,portnum,staticroutedict,name):
    tn = telnetlib.Telnet(host=hostnum,port=portnum)
    time.sleep(15)
    print(f"[+] {name} static route config start. ")
    tn.write(b"\r")
    tn.write(b"configure terminal\r")
    for i,j in staticroutedict.items():
        tn.write(f"ip route {i} {j}\r".encode("ascii"))
    tn.write(b"\r")
    tn.write(b"end\r")
    tn.write(b"show running | include ip route\r")
    tn.write(b"exit\r")
    tn.write(b'\r')
    time.sleep(5)
    with open("configureStaticRouteText",'a') as filename:
        filename.write(tn.read_very_eager().decode("utf-8"))
    print(f"[+] {name} Static Route set is over.")
    tn.close()
    
    
class connectHandle:
    def __init__(self,iptable,statictable,mape):
        self.ipaddress = iptable
        self.staticaddress = statictable
        self.mapp = mape
    def setIPaddress(self):
        for i in self.ipaddress:
            pcname = list(i.keys())[0]
            hostname1 = i[pcname]["host"]
            portname1 = i[pcname]["port"]
            interfaceDict1 = i[pcname]["interface"]
            ConfigDevice(hostname=hostname1,portnum=portname1,loopbackdict=interfaceDict1,name=pcname)
            
    def setStaticRoute(self):
        for i in self.staticaddress:
            pcname = list(i.keys())[0]
            hostname1 = self.mapp[pcname]["host"]
            portname1 = self.mapp[pcname]["port"]
            staticroutedict1 = i[pcname]
            ConfigStaticRoute(hostname1,portname1,staticroutedict1,pcname)
            
if __name__ == "__main__":
    portPool = list(range(5000,5005))
    R1 = {"e1/1":"12.1.1.1/24","e1/0":"17.1.1.2/24","loopback 1":"192.168.1.1 255.255.255.0"}
    R2 = {"e1/0":"12.1.1.2/24","e1/1":"13.1.1.1/24","e1/2":"16.1.1.2/24","loopback 1":"192.168.2.1/24"}
    R3 = {"e1/0":"13.1.1.2/24","e1/1":"14.1.1.1/24","loopback 1":"192.168.3.1/24"}
    R4 = {"e1/0":"14.1.1.2/24","e1/1":"15.1.1.2/24","loopback 1":"192.168.4.1/24"}
    R5 = {"e1/0":"17.1.1.1/24","e1/1":"15.1.1.1/24","e1/2":"16.1.1.1/24","loopback 1":"192.168.5.1/24"}
    interPool = [R1,R2,R3,R4,R5]
    node1 = Node("127.0.0.1",portPool[0],interPool[0],"R1")
    node2 = Node("127.0.0.1",5005,interPool[1],"R2")
    node3 = Node("127.0.0.1",portPool[2],interPool[2],"R3")
    node4 = Node("127.0.0.1",portPool[3],interPool[3],"R4")
    node5 = Node("127.0.0.1",portPool[4],interPool[4],"R5")
    mapneed ={}
    nodePool = [node1,node2,node3,node4,node5]
    for i in nodePool:
        mapneed[i.name] = {"host":i.host,"port":i.port}
        i.createNetw()
    pictureStruct = NetworkPic(nodePool)
    networkTable = ConfigTable(pictureStruct)
    networkTable.CreateTable()
    ConnectH = connectHandle(networkTable.IpAddressTable,networkTable.RouteTable,mape=mapneed)
    print(mapneed)
    ConnectH.setIPaddress()
    print("\n---------------- Waiting 10 second,We will Config Static route. -------------------")
    time.sleep(10)
    ConnectH.setStaticRoute()