import os
import yaml


def get_params(q):
    try:
        path = os.path.join(os.path.expanduser('~'), 'mark_serial_ws', 'src','markserial_pkg','config', 'setup_markSerial.yaml')
        with open(path,'r') as f:
            yml_dict = yaml.safe_load(f)
            ans = yml_dict.get(q)
        print('Get '+q+' Done.')
        return  ans
    except:
        print('Get '+q+' Failed'+'Something went wrong when opening YAML.')
    return 0

def setupvarforcreatelib():
    id_mcu=0
    id_topic=[]
    nameofTopic=[]
    interfacefile=[]
    dataType=[]
    dataName=[]
    try:
        id_mcu=get_params("Idmcu")
        Setup_Sub=get_params("Setup_Sub")
        for i in range(0,len(Setup_Sub)):
            id_topic.append(Setup_Sub[i][0])
            nameofTopic.append(Setup_Sub[i][1])
            interfacefile.append(Setup_Sub[i][2])
        for i in range (0,len(interfacefile)):
            tempType=[]
            tempName=[]
            tempdatagrab=[]
            path = os.path.join(os.path.expanduser('~'), 'mark_serial_ws', 'src','markserial_interfaces','msg',  interfacefile[i])
            msg = open(path, 'r').read().splitlines()
            for j in range(0,len(msg)):
                line=msg[j].split()
                tempType.append(line[0])
                tempName.append(line[1])
                tempdatagrab.append(0)
            dataType.append(tempType)
            dataName.append(tempName)
           
    except:
        print("Error setup variable.")

    return id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName
def getbeforedot(q):
    qq=""
    for i in range (0,len(q)):
        if(q[i]=="."):
            break
        else:
            qq=qq+q[i]
    return qq

def getafterdot(q):
    qq=""
    flag=0
    for i in range (0,len(q)):
        if(flag):
            qq=qq+q[i]
        if(q[i]=="."):
            flag=1
    return qq

def genSub(fw,nameofTopic,interfacefile):
    try:
        callback=[]
        fw.write("\r\r        #gen\r")
        for i in range (0,len(nameofTopic)):
            q="        self.subscription_"
            q=q+nameofTopic[i]
            w=" = self.create_subscription("
            w=w+getbeforedot(interfacefile[i])+",'"+nameofTopic[i]+"'," 
            e="self.callback_"+nameofTopic[i]
            w=w+e+",10)"
            callback.append(e)
            fw.write(q+w+"\r")
            fw.write("        "+e+"\r")
        fw.write("\r\r\r\r")
        print("gennerate Sub Done.")
    except:
        print("gennerate Sub Fail.")
    return callback

def typetofunc(typee,namee):
    try:
        if(typee=="uint8"):
            return  "        self._SendUint8(msg."+namee+")\n"
        elif(typee=="uint16"):
            return  "        self._SendUint16(msg."+namee+")\n"
        elif(typee=="uint32"):
            return  "        self._SendUint32(msg."+namee+")\n"
        elif(typee=="uint64"):
            return  "        self._SendUint64(msg."+namee+")\n"
        elif(typee=="int8"):
            return  "        self._SendInt8(msg."+namee+")\n"
        elif(typee=="int16"):
            return  "        self._SendInt16(msg."+namee+")\n"
        elif(typee=="int32"):
            return  "        self._SendInt32(msg."+namee+")\n"
        elif(typee=="int64"):
            return  "        self._SendInt64(msg."+namee+")\n"
        elif(typee=="float32" or typee=="float64" ):
            return  "        self._SendFloat32(msg."+namee+")\n"
        elif(typee=="string" ):
            return  "        self._SendString(msg."+namee+")\n"
        else:
            return "0"
    except:
        print("Format .msg wrong")
    return "0"
def gencallback(fw,callback,id_mcu,id_topic,dataType,dataName):
    try:
        fw.write("    # gen\r")
        for i in range(len(callback)):
            fw.write("    def "+getafterdot(callback[i])+"(self,msg):\r")
            fw.write("        self.sum=0\r")
            fw.write("        self._Sendstart()\r")
            fw.write("        self._SendHands("+str(id_mcu)+","+str(id_topic[i])+")\r")
            for j in range (0,len(dataType[i])):
                fw.write(typetofunc(dataType[i][j],dataName[i][j]))
                if(j<len(dataType[i])-1):
                    fw.write("        self._Sendcontinue()\r")
            fw.write("        self._Sendstop()\r")
            fw.write("        self._Sendsum()\r")
            fw.write("\r        return 1\r\r\r\r")
        print("gennerate Callback Done.")
        return 1
    except:
        print("gennerate Callback Fail.")
    return 0
def gennerate(): 
    
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName=setupvarforcreatelib()
    pathr= os.path.join(os.path.expanduser('~'), 'mark_serial_ws', 'src','markserial_pkg','scripts', '.node_preSetup.txt')
    pathw= os.path.join(os.path.expanduser('~'), 'mark_serial_ws', 'src','markserial_pkg','markserial_pkg', 'markserial_node.py')
    fr=open(pathr, 'r') 
    fw=open(pathw, 'w+') 
    fw.write("# ***************************************************************************************************************************************************\r")
    fw.write("#      |          This script was auto-generated by generate_markserial_node.py which received parameters from setup_markSerial.yaml          |\r")
    fw.write("#      |                                         EDITING THIS FILE BY HAND IS NOT RECOMMENDED                                                 |\r")
    fw.write("# ***************************************************************************************************************************************************\r\r")
    c=0
    callback=[]
    for line in fr:
        c=c+1
        if(c==275):
            callback=genSub(fw,nameofTopic,interfacefile)
        elif(c==399):
            gencallback(fw,callback,id_mcu,id_topic,dataType,dataName)
        else:
            fw.write(line)
    return 1
def main():
    try:
        gennerate()
        print("----------------------generate markserial_node.py Done----------------------")
    except:
        print("----------------------generate markserial_node.py Fail----------------------")
    return 1

if __name__=='__main__':
    main()