import copy
import re
import numpy as np

def countMask(numslist):
    res = 0
    index = 7
    for i in numslist:
        res += i * (2 ** index)
        index -= 1
    return res

def convertMask(nums):
    li = []
    for i in range(nums):
        li.append(1)
    for i in range(32 - nums):
        li.append(0)
    # return "{}.{}.{}.{}".format(countMask(li[0:8]),countMask(li[8:16]),countMask(li[16:24]),countMask(li[24,32]))
    return f"{countMask(li[0:8])}.{countMask(li[8:16])}.{countMask(li[16:24])}.{countMask(li[24:32])}"
def decompose(nums,bits):
    li = []
    nums = int(nums)
    for i in range(bits):
        li.insert(0,nums % 2)
        nums = int(nums / 2)
    return np.array(li)

def countNet(ipAddress,Mask):
    ipaddresslist = re.findall("(\w+)\.",ipAddress)
    ipaddresslist.append(list(re.findall("\.(\w+)",ipAddress))[-1])
    masklist = re.findall("(\w+)\.",Mask)
    masklist.append(list(re.findall("\.(\w+)",Mask))[-1])
    res = []
    # print("len(masklist): ",len(masklist),masklist)
    for i,j in zip(ipaddresslist,masklist):
        mid = decompose(i,8) * decompose(j,8)
        mid = countMask(mid)
        res.append(mid)
    return f"{res[0]}.{res[1]}.{res[2]}.{res[3]}"

class Node:
    def __init__(self,hostname,portnumber,networkInterfaceDict,name,username=None,passwd=None):
        self.host = hostname
        self.port = portnumber
        self.user = username
        self.pasd = passwd
        self.nicd = networkInterfaceDict
        self.name = name
        self.netcard = self.createnetcard()
        self.address = {}
        self.netw = {}
        self.next = []
        self.indexnext = []

    def handleIPaddress(self):
        middleAddress = copy.deepcopy(self.nicd)
        for i,j in middleAddress.items():
            if '/' in j:
                self.address[i] = j[:-3]+ " " + convertMask(int(j[-2:]))
            else:
                a = re.findall("(\w+.\w+.\w+.\w+) (\w+.\w+.\w+.\w+)",j)
                self.address[i] = a[0][0] + " " + a[0][1]
    def createNetw(self):
        middleDict = copy.deepcopy(self.nicd)
        for i,j in middleDict.items():
            if '/' in j:
                self.netw[i] = countNet(j[:-3],convertMask(int(j[-2:]))) + " " + convertMask(int(j[-2:]))
            else:
                a = re.findall("(\w+.\w+.\w+.\w+) (\w+.\w+.\w+.\w+)",j)
                self.netw[i] = countNet(a[0][0],a[0][1]) + " " + a[0][1]
    def ShowNetwork(self):
        for i,j in self.netw.items():
            print(f"{i} --> {j}")
    
    def createnetcard(self):
        mid = []
        for i in self.nicd.keys():
            mid.append(i)
        return mid
    
    def length(self):
        return len(self.nicd)
    
if __name__ == "__main__":
    pc = {"f0/0":"192.168.1.1/24","f1/0":"192.168.2.1 255.255.255.0","loopback 1":"1.1.1.1 255.255.255.255"}
    a = Node("127.0.0.1","0",pc,"pc","Cisco","123123")
    a.createNetw()
    a.ShowNetwork()
    a.handleIPaddress()
    print(a.netcard)