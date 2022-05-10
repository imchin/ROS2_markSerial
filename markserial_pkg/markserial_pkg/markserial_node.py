import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
import numpy as np
import os
import yaml
import serial
from markserial_interfaces.msg import *
import struct




supportTypetype=[["uint8","int8"],["uint16","int16"],["uint32","int32","float32"],["uint64","int64","float32"],["string"]]
supportType=[[8,18],[16,116],[32,132,111],[64,164,222],[242]]

def get_params(self,q):
    try:
        path = os.path.join(os.path.expanduser('~'), 'mark_serial_ws', 'src','markserial_pkg','config', 'setup_markSerial.yaml')
        with open(path,'r') as f:
            yml_dict = yaml.safe_load(f)
            ans = yml_dict.get(q)
        self.get_logger().info('Get '+q+' Done.')
        return  ans
    except:
        self.get_logger().info('Get '+q+' Failure'+'Something went wrong when opening the file.')

    return 0

def check_port_open(self,Port):
    try:
        ser = serial.Serial(Port, 115200, timeout=1000 ,parity="E",stopbits=1)  
        self.get_logger().info(Port + ': port is Open.')
        return ser
    except:
        self.get_logger().info(Port + ': open port Failed.')
    return 0

def setup_var_protocol(self):
    setup_pub=get_params(self,'Setup_Pub')
    Idmsg=[]
    nametopic=[]
    interfacetopic=[]
    for i in range(0,len(setup_pub)):
        Idmsg.append(setup_pub[i][0])
        nametopic.append(setup_pub[i][1])
        interfacetopic.append(setup_pub[i][2])
    self.get_logger().info('Done load YAML pub.')
    dataType=[]
    dataName=[]
    self.datagrab=[]
    try:
        for i in range (0,len(interfacetopic)):
            tempType=[]
            tempName=[]
            tempdatagrab=[]
            path = os.path.join(os.path.expanduser('~'), 'mark_serial_ws', 'src','markserial_interfaces','msg', interfacetopic[i])
            msg = open(path, 'r').read().splitlines()
            for j in range(0,len(msg)):
                line=msg[j].split()
                tempType.append(line[0])
                tempName.append(line[1])
                tempdatagrab.append(0)
            dataType.append(tempType)
            dataName.append(tempName)
            self.datagrab.append(tempdatagrab)
        self.get_logger().info('Generate variable from msg Done.')
    except:
        self.get_logger().info('Generate variable from msg Failed.')
        return 0,0,0,0,0,0
   
    return Idmsg,nametopic,interfacetopic,dataType,dataName,self.datagrab

def create_N_topic(self,name,interfaces):
    try:
        for i in range (0,len(interfaces)):
            msg= interfaces[i][0:len(interfaces[i])-4]
            interfaces[i] = self.create_publisher(globals()[msg] , name[i], 10)
            self.get_logger().info('Open Topic Name : '+name[i] +"  Use msg name : "+ msg)
        self.get_logger().info("Open Topic All Done.")
        return  interfaces
    except:
        self.get_logger().info("Open Topic Failed.")
        return 0

class ThreadOne(Node):

    def __init__(self):
        super().__init__('ThreadOne')
        self.Port= get_params(self,"Port")   
        self.ser= check_port_open(self,self.Port)
        self.Buffer= np.zeros(512)
        self.index= 0
        self.indexPre= 0
        timer_period = 0.00005  # seconds 20000Hz but uart can posible 10472.7272Hz
        self.timer = self.create_timer(timer_period, self.UartReceive)
        
    def UartReceive(self):
        try:
            s = self.ser.read()
            self.index=(self.index+1)%512
            self.Buffer[self.index]= int.from_bytes(s, byteorder="big",signed=0) 
            # self.get_logger().info(str(self.Buffer[self.index]))
        except:
            self.get_logger().info('Failed to receive Uart.')
            try:
                self.get_logger().info('Try open port again.')
                self.ser= check_port_open(self,self.Port)
            except:
                self.get_logger().info('Failed to open port.')
            
            
       
            

class ThreadTwo(Node):
    def __init__(self,dma):
        super().__init__('ThreadTwo')
        self.dma= dma
        self.Idmcu= get_params(self,"Idmcu")   
        self.Idmsg , self.nametopic ,  self.interfaceTopic ,self.dataType , self.dataName ,self.datagrab = setup_var_protocol(self)
        self.emptydatagrab=self.datagrab.copy()
        # print(self.dataName)
        self.obj= create_N_topic(self,self.nametopic,self.interfaceTopic.copy())
        # print(self.interfaceTopic)
        timer_period = 0.00002
        self.timer = self.create_timer(timer_period, self.Protocol)
        self.state=0
        self.i=0
        self.n=0
        self.b=[]
        self.N=0
        self.OnIdmsg=0
        self.indexIdmsg=0

    def Protocol(self): 
        if(self.dma.index!=self.dma.indexPre):
            self.dma.indexPre=(self.dma.indexPre+1)%512
            state=self.state
            buff=self.dma.Buffer
            indexPre=self.dma.indexPre 
            Idmsg=self.Idmsg
            Idmcu=self.Idmcu
            datagrab=self.datagrab


            # print(buff[indexPre])
            if(state==0 and buff[indexPre]==73 ):
                state=1
            elif(state==1 and buff[indexPre]==109 ):
                state=2
            elif(state==2 and buff[indexPre]==64 ):
                state=3
            elif(state==3 and buff[indexPre]==99 ):
                # print("Done check Start")
                state=4
            elif(state==4):
                self.OnIdmsg=0
                for j in range(0,len(Idmsg)):
                    if( (int( (buff[indexPre] ))&0b11110000 )>>4 == Idmcu  and int(buff[indexPre])&0b1111 == Idmsg[j]  ):
                        self.OnIdmsg=Idmsg[j]
                        # print("Done check Idmcu and Idmsg :  " + str(self.OnIdmsg))
                        self.i=-1
                        state=5
                        self.indexIdmsg=j
                        break
                    else:
                        state=0
            elif(state==5):
                self.i=self.i+1
                self.N=0
                for j in range (0,len(supportType)):
                    for k in range (0,len(supportType[j])):
                        if(supportType[j][k] == int(buff[indexPre]) ):
                            if(buff[indexPre] == supportType[4][0]):
                                self.N=99
                                self.b=[]
                                state=20
                            else:
                                self.N=supportType[j][0]/8
                                self.n=0
                                self.b=[]
                                state=6
                            break
                if(self.N==0):
                    state=0
            elif(state==6):
                self.n=self.n+1
                self.b.append(int(buff[indexPre]))
                if(self.n==self.N):
                    datagrab[self.indexIdmsg][self.i]=self.b
                    state=7
            elif(state==7 and buff[indexPre]==126 ):
                # print(datagrab)
                self.datagrab=datagrab
                self.pubb()
                state=0
            elif(state==7 and buff[indexPre]==42 ):
                state=8
            elif(state==8 and buff[indexPre]==42 ):
                state=5

            elif(state==20):
                if(buff[indexPre]==42 ):
                    state=21
                else:
                    self.b.append(int(buff[indexPre]))

            elif(state==21 and buff[indexPre]==126):
                datagrab[self.indexIdmsg][self.i]=self.b
                state=7
            elif(state==21 and buff[indexPre]==42):
                state=8
            else:
                state=0

          
            self.state=state
            
            # return self.Protocol()

            # self.get_logger().info(str(self.dma.Buffer[self.dma.indexPre]))
    def pubb(self):
        # print(self.interfaceTopic[self.indexIdmsg])
        # print(self.dataType[self.indexIdmsg])
        # print(self.datagrab[self.indexIdmsg])



        convdata=self.emptydatagrab.copy()
        convdata=convdata[self.indexIdmsg]

        msg= self.interfaceTopic[self.indexIdmsg][0:len(self.interfaceTopic[self.indexIdmsg])-4]
        msg=globals()[msg]()
        
        
        for i in range(0,len(self.dataType[self.indexIdmsg])):
            
            if(self.dataType[self.indexIdmsg][i]== "uint8" or self.dataType[self.indexIdmsg][i]== "uint16" or self.dataType[self.indexIdmsg][i]== "uint32" or self.dataType[self.indexIdmsg][i]== "uint64"):
                bytes_val = bytearray(self.datagrab[self.indexIdmsg][i])
                # print(int.from_bytes(bytes_val, byteorder="big",signed=0)  )
                exec("%s = %d" % (("msg."+self.dataName[self.indexIdmsg][i]) ,int.from_bytes(bytes_val, byteorder="big",signed=0) ))
       
            elif(self.dataType[self.indexIdmsg][i]=="int8" or self.dataType[self.indexIdmsg][i]== "int16" or self.dataType[self.indexIdmsg][i]== "int32" or self.dataType[self.indexIdmsg][i]== "int64"):
                b=self.datagrab[self.indexIdmsg][i]
                bytes_val = bytearray(b)
                # print(int.from_bytes(bytes_val, byteorder="big",signed=1)  )
                exec("%s = %d" % (("msg."+self.dataName[self.indexIdmsg][i]) ,int.from_bytes(bytes_val, byteorder="big",signed=1)  ))
                
           
                
            elif(self.dataType[self.indexIdmsg][i]=="float32" ):
                b=self.datagrab[self.indexIdmsg][i]
                # print(b)
                bytes_val = bytearray(b)
                # print(bytes_val)
                # print(struct.unpack('>f', bytes_val))
                exec("%s = %.50f" % (("msg."+self.dataName[self.indexIdmsg][i]) ,struct.unpack('<f', bytes_val)[0]))
              
            elif(self.dataType[self.indexIdmsg][i]=="float64"):
                b=self.datagrab[self.indexIdmsg][i]
                # print(b)
                bytes_val = bytearray(b)
                # print(bytes_val)
                # print(struct.unpack('>d', bytes_val))
                exec("%s = %.50f" % (("msg."+self.dataName[self.indexIdmsg][i]) ,struct.unpack('>d', bytes_val)[0]))
               
            elif(self.dataType[self.indexIdmsg][i]=="string"):
                b=self.datagrab[self.indexIdmsg][i]
                # print(b)
                bytes_val = bytearray(b)
                # print(str(bytes_val ,'utf-8'))
                exec("%s = %s" % (("msg."+self.dataName[self.indexIdmsg][i]) ,"str(bytes_val ,'utf-8')"  ))

        # msg= self.interfaceTopic[self.indexIdmsg][0:len(self.interfaceTopic[self.indexIdmsg])-4]
        # msg=globals()[msg]()
        
        # exec("%s = %d" % ("msg.a",50))
        self.obj[self.indexIdmsg].publish(msg)
        # print("W")
        # for i in range(0,len(self.dataName[self.indexIdmsg])):
        #     print(self.dataName[self.indexIdmsg][i])


        
        return 0 
       
       
            
          
    
    

class ThreadThree(Node):
    def __init__(self):
        super().__init__('ThreadThree')       






def main(args=None):
    rclpy.init(args=args)
    try:
        threadOnee= ThreadOne()
        threadTwoo= ThreadTwo(dma=threadOnee)
        threadThreee= ThreadThree() 
        executor = MultiThreadedExecutor(num_threads=8)
        executor.add_node(threadOnee)
        executor.add_node(threadTwoo)
        executor.add_node(threadThreee)
        try:
            print("spin")
            executor.spin()

        finally:
            executor.shutdown()
            print("eror")
          
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()