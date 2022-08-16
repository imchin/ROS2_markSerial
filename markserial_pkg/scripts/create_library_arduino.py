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
        print('Get '+q+' Fail'+'Something went wrong when opening YAML.')

    return 0
def mkdir():
    path="Fail"
    try:
        path = get_params("path_arduino")
        path=path+"/libraries/MarkSerial"
        path = os.path.join(os.path.expanduser('~'), path)
        os.mkdir(path)
        print("make folder Done path: "+path)
        return path
    except:
        print("path: "+path)
        return path
def setupvarforcreatelib():
    id_mcu=0
    id_topic=[]
    nameofTopic=[]
    interfacefile=[]
    dataType=[]
    dataName=[]
    try:
        id_mcu=get_params("Idmcu")
        Setup_Pub=get_params("Setup_Pub")
        for i in range(0,len(Setup_Pub)):
            id_topic.append(Setup_Pub[i][0])
            nameofTopic.append(Setup_Pub[i][1])
            interfacefile.append(Setup_Pub[i][2])
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

def setupvarforcreatelibSub():
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


def create_hstruct(fw):
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName=setupvarforcreatelibSub()
    public_struct=[]
    fw.write("\r\r\r        // gen\r")
    for i in range (0,len(dataType)):
        q="        struct{\r"
        for j in range (0,len(dataType[i])):
            if(convertdatatype(dataType[i][j])!="String"):
                q=q+"            "+convertdatatype(dataType[i][j])+" "+dataName[i][j]+"= 0;\r"
            else:
                q=q+"            "+convertdatatype(dataType[i][j])+" "+dataName[i][j]+"= \"\";\r"
        q=q+"        } Sub_"+nameofTopic[i]+";\r\r"
        public_struct.append(q)
        fw.write(q)
    return public_struct
def getMaxNdata(q):
    w=0
    for i in range (0,len(q)):
        if(len(q[i])>=w):
            w=len(q[i])
    return w
def Arraymaptype(dataType):
    q="{"
    for i in range(len(dataType)):
        q=q+"{"
        for j in range(len(dataType[i])):
            if(j<len(dataType[i])-1):
                q=q+typetoProtocol(dataType[i][j])+","
            else:
                q=q+typetoProtocol(dataType[i][j])
        if(i<len(dataType)-1):
            q=q+"},"
        else:
            q=q+"}"
    q=q+"};\r"
    return q
def typetoProtocol(typee):
    if(typee=="uint8"):
        return  "8"
    elif(typee=="uint16"):
        return  "16"
    elif(typee=="uint32"):
        return  "32"
    elif(typee=="uint64"):
        return  "64"
    elif(typee=="int8"):
        return  "18"
    elif(typee=="int16"):
        return  "116"
    elif(typee=="int32"):
        return  "132"
    elif(typee=="int64"):
        return  "164"
    elif(typee=="float32" or typee=="float64" ):
        return  "111"
    elif(typee=="string" ):
        return  "242"
    else:
        return "0"
def ArraytotalVar(q):
    w="{"
    for i in range (0,len(q)):
        if(i<len(q)-1):
            w=w+str(len(q[i]))+","
        else:
            w=w+str(len(q[i]))
    w=w+"};\r"
    return w
def gen_privateStruct(fw):
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName=setupvarforcreatelibSub()
    fw.write("\r\r\r        // gen\r")
    q="        void* _nonverify["+str(len(id_topic))+"]["+str(getMaxNdata(dataType))+"];\r"
    q=q+"        void* _verify["+str(len(id_topic))+"]["+str(getMaxNdata(dataType))+"];\r"
    q=q+"        uint8_t _Idtopic_sub["+str(len(id_topic))+"]={"
    for i in range (0,len(id_topic)):
        if(i<len(id_topic)-1):
            q=q+str(id_topic[i])+","
        else:
            q=q+str(id_topic[i])
    q=q+"};\r"
    q=q+"        uint8_t _TopicType["+str(len(id_topic))+"]["+str(getMaxNdata(dataType))+"]="+Arraymaptype(dataType)
    q=q+"        uint8_t _Totalvar["+str(len(id_topic))+"]="+ArraytotalVar(dataType)
    fw.write(q)
    return 1
def publicStructToprivateStruct(fw,q):
    w=""
    tt=1
    fw.write("\r\r\r        // gen\r")
    for i in range(0,len(q)):
        e=""
        for j in range(0,len(q[i])):
            if(q[i][j]=="}"):
                e=e+"}_"
                tt=0
            elif(tt):
                e=e+q[i][j]
            else:
                tt=1
        w=w+e
    fw.write(w)
    return 1
def create_hFile(listVoid):
    try:
        path = mkdir()
        path = path +"/MarkSerial.h"
        fw  = open(path, "w+")
        pathr= os.path.join(os.path.expanduser('~'), 'mark_serial_ws', 'src','markserial_pkg','scripts', '.arduino_h_preSetup.txt')
        fr=open(pathr, 'r') 
        fw.write("// ***************************************************************************************************************************************************\r")
        fw.write("//      |          This script was auto-generated by create_library_arduino.py which received parameters from setup_markSerial.yaml            |\r")
        fw.write("//      |                                         EDITING THIS FILE BY HAND IS NOT RECOMMENDED                                                 |\r")
        fw.write("// ***************************************************************************************************************************************************\r\r")
        public_struct=[]
        c=0
        for line in fr:
            c=c+1
            if(c==7):
                try:
                    fw.write("\r\r\r        // gen\r")
                    for i in range(0,len(listVoid)):
                        fw.write(listVoid[i])
                        fw.write("\n")
                    print("gen voidPub Done")
                    public_struct=create_hstruct(fw)
                    print("gen public_struct Done")
                except:
                    print("gen public_struct or voidPub Fail.")
            elif(c==55):
                try:
                    gen_privateStruct(fw)
                    publicStructToprivateStruct(fw,public_struct)
                    print("gen private_struct Done")
                except:
                    print("gen private_struct Fail")
            else:
                fw.write(line)
        print(".h Done.")
    except:
        print(".h Fail.")
    return 0

def genPointer(fw):
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName=setupvarforcreatelibSub()
    fw.write("\r    // gen\r")
    q=""
    w=""
    for i in range(0,len(id_topic)):
        for j in range(0,len(dataName[i])):
            q=q+"    _nonverify["+str(i)+"]["+str(j)+"]"+"=&_Sub_"+nameofTopic[i]+"."+dataName[i][j]+";\r"
            w=w+"    _verify["+str(i)+"]["+str(j)+"]"+"=&Sub_"+nameofTopic[i]+"."+dataName[i][j]+";\r"
    q=q+"\r\r"
    q=q+w
    fw.write(q)
    fw.write("\r\r\r")
    return 1

def create_cppFile(listVoid,id_mcu,id_topic,dataType,dataName):
    try:
        path = mkdir()
        path = path +"/MarkSerial.cpp"
        fw  = open(path, "w+") 
        pathr= os.path.join(os.path.expanduser('~'), 'mark_serial_ws', 'src','markserial_pkg','scripts', '.arduino_cpp_preSetup.txt')
        fr=open(pathr, 'r') 
        fw.write("// ***************************************************************************************************************************************************\r")
        fw.write("//      |          This script was auto-generated by create_library_arduino.py which received parameters from setup_markSerial.yaml            |\r")
        fw.write("//      |                                         EDITING THIS FILE BY HAND IS NOT RECOMMENDED                                                 |\r")
        fw.write("// ***************************************************************************************************************************************************\r\r")
        c=0
        for line in fr:        
            c=c+1
            if(c==124): 
                try:
                    fw.write("\r\r\r// gen\r")
                    for i in range(0,len(listVoid)):
                        fw.write(listVoid[i][8:12]+" MarkSerial::"+listVoid[i][13:len(listVoid[i])-1])
                        fw.write(("{\n"))
                        fw.write("    _sum=0;\r")
                        fw.write("    _Sendstart();\n")
                        fw.write("    _SendHands("+str(id_mcu)+","+str(id_topic[i])+");\n")
                        for j in range(0,len(dataType[i])):
                            fw.write(typetoVoid(dataType[i][j],dataName[i][j]))
                            if(j<len(dataType[i])-1):
                                fw.write("    _Sendcontinue();\n")
                            else:
                                fw.write("    _Sendstop();\n")
                        fw.write("    _SendSum();\r")
                        fw.write("}\n")
                    print("gen functionPub Done.")
                except:
                    print("gen functionPub Fail.")
            elif(c==9):
                try:
                    genPointer(fw)
                    print("gen pointer Done.")
                except:
                    print("gen pointer Fail.")
            else:
                fw.write(line)
        fw.close
        print(".cpp Done.")
    except:
        print(".cpp Fail.")
    return 0
def convertdatatype(strr):
    if(strr=="uint8"or strr=="uint16" or strr=="uint32" or strr=="uint64" or strr=="int8"or strr=="int16" or strr=="int32" or strr=="int64" ):
        return (strr+"_t")
    elif(strr=="float32" or strr=="float64" ):
        return "float"
    elif(strr=="string"):
        return "String"
    else:
        return "bool"
    
def typetoVoid(typee,namee):
    if(typee=="uint8"):
        return  "    _SendUint8("+namee+");\n"
    elif(typee=="uint16"):
        return  "    _SendUint16("+namee+");\n"
    elif(typee=="uint32"):
        return  "    _SendUint32("+namee+");\n"
    elif(typee=="uint64"):
        return  "    _SendUint64("+namee+");\n"
    elif(typee=="int8"):
        return  "    _SendInt8("+namee+");\n"
    elif(typee=="int16"):
        return  "    _SendInt16("+namee+");\n"
    elif(typee=="int32"):
        return  "    _SendInt32("+namee+");\n"
    elif(typee=="int64"):
        return  "    _SendInt64("+namee+");\n"
    elif(typee=="float32" or typee=="float64" ):
        return  "    _SendFloat32("+namee+");\n"
    elif(typee=="string" ):
        return  "    _SendString("+namee+");\n"
    else:
        return "0"

def strVoid(nameofTopic,dataType,dataName):
    temp=[]
    for i in range(0,len(nameofTopic)):
        t="        "
        t=t+"void publish_"+nameofTopic[i]+"("
        for j in range(0,len(dataType[i])):
            t=t+convertdatatype(dataType[i][j])+" "+dataName[i][j]
            if(convertdatatype(dataType[i][j])=="char"):
                t=t+"[] "
            else:
                t=t+" "
            if(j>=0 and j<len(dataType[i])-1):
                t=t+","
        t=t+");"
        temp.append(t)
    # print(temp)
    return temp

def gen():
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName=setupvarforcreatelib()
    listVoid=strVoid(nameofTopic,dataType,dataName)
    create_hFile(listVoid)
    create_cppFile(listVoid,id_mcu,id_topic,dataType,dataName)
 


def main():
    try:
        gen()
        print("*******Create library arduino complete*******")
    except:
        print("*******Create library arduino failed*******")
if __name__ == '__main__':
    main()