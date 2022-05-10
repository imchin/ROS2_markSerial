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
def mkdir():
    path="Failure"
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


def create_hFile(listVoid):
    try:
        path = mkdir()
        path = path +"/MarkSerial.h"
        f  = open(path, "w+")
        f.write("#include \"Arduino.h\" \n")     
        f.write("class MarkSerial{\n\n")           
        f.write("    public:\n")
        f.write("        MarkSerial();\n")
        f.write("        void begin(Stream *SerialObject,uint8_t Idmcu);\n")
        for i in range(0,len(listVoid)):
            f.write(listVoid[i])
            f.write("\n")
        f.write("\n")
        f.write("    private:\n")
        f.write("        int _Idmcu=0;\n")
        f.write("        Stream* _serial;\n")
        f.write("        uint8_t _start[4]={73,109,64,99};\n")
        f.write("        uint8_t _stop[2]={126,126};\n")
        f.write("        uint8_t _continue[2]={42,42};\n")
        f.write("        void _Sendstart();\n")
        f.write("        void _SendHands(uint8_t Idmcu,uint8_t IdTopic);\n")
        f.write("        void _Sendstop();\n")
        f.write("        void _Sendcontinue();\n")
        f.write("        void _SendUint8(uint8_t data);\n")
        f.write("        void _SendUint16(uint16_t data);\n")
        f.write("        void _SendUint32(uint32_t data);\n")
        f.write("        void _SendUint64(uint64_t data);\n")
        f.write("        void _SendInt8(int8_t data);\n")
        f.write("        void _SendInt16(int16_t data);\n")
        f.write("        void _SendInt32(int32_t data);\n")
        f.write("        void _SendInt64(int64_t data);\n")
        f.write("        void _SendFloat32(float data);\n")
        f.write("        void _SendString(char data[]);\n")
        f.write("};\n")
        f.close()
        print(".h Done.")
    except:
        print(".h Failed.")
    return 0
def create_cppFile(listVoid,id_mcu,id_topic,dataType,dataName):
    try:
        path = mkdir()
        path = path +"/MarkSerial.cpp"
        f  = open(path, "w+")
        f.write("#include \"MarkSerial.h\"\n")
        f.write("MarkSerial::MarkSerial(){\n")
        f.write("}\n")
        f.write("void MarkSerial::begin(Stream *SerialObject,uint8_t Idmcu){\n")
        f.write("    _serial=SerialObject;\n")
        f.write("    _Idmcu=Idmcu;\n")
        f.write("}\n")
        f.write("void MarkSerial::_Sendstart(){\n")
        f.write("    _serial->write(_start,4);\n")
        f.write("}\n")
        f.write("void MarkSerial::_Sendstop(){\n")
        f.write("    _serial->write(_stop,2);\n")
        f.write("}\n")
        f.write("void MarkSerial::_Sendcontinue(){\n")
        f.write("    _serial->write(_continue,2);\n")
        f.write("}\n")
        f.write("void MarkSerial::_SendHands(uint8_t Idmcu,uint8_t IdTopic){\n")
        f.write("   uint8_t q[1]={0};\n")
        f.write("   q[0]=Idmcu<<4;\n")
        f.write("   q[0]=q[0]|IdTopic;\n")
        f.write("   _serial->write(q,1);\n")
        f.write("}\n")
        f.write("void MarkSerial::_SendUint8(uint8_t data){\n")
        f.write("    uint8_t buff[2]={8,0};\n")
        f.write("    buff[1]=data;\n")
        f.write("    _serial->write(buff,2);\n")
        f.write("}\n")
        f.write("void MarkSerial::_SendUint16(uint16_t data){\n")
        f.write("    uint8_t buff[3]={16,0,0};\n")
        f.write("    buff[1]=(data&(0xff<<8))>>8;\n")
        f.write("    buff[2]=data&0xff;\n")
        f.write("    _serial->write(buff,3);\n")
        f.write("}\n")
        f.write("void MarkSerial::_SendUint32(uint32_t data){\n")
        f.write("    uint8_t buff[5]={32,0,0,0,0};\n")
        f.write("    buff[1]=(data&(0xff<<24))>>24;\n")
        f.write("    buff[2]=(data&(0xff<<16))>>16;\n")
        f.write("    buff[3]=(data&(0xff<<8))>>8;\n")
        f.write("    buff[4]=data&0xff;\n")
        f.write("    _serial->write(buff,5);\n")
        f.write("}\n")
        f.write("void MarkSerial::_SendUint64(uint64_t data){\n")
        f.write("    uint8_t buff[9]={64,0,0,0,0,0,0,0,0};\n")
        f.write("    buff[1]=(data&(0xff<<56))>>56;\n")
        f.write("    buff[2]=(data&(0xff<<48))>>48;\n")
        f.write("    buff[3]=(data&(0xff<<40))>>40;\n")
        f.write("    buff[4]=(data&(0xff<<32))>>32;\n")
        f.write("    buff[5]=(data&(0xff<<24))>>24;\n")
        f.write("    buff[6]=(data&(0xff<<16))>>16;\n")
        f.write("    buff[7]=(data&(0xff<<8))>>8;\n")
        f.write("    buff[8]=data&0xff;\n")
        f.write("    _serial->write(buff,9);\n")
        f.write("}\n")
        f.write("void MarkSerial::_SendInt8(int8_t data){\n")
        f.write("    uint8_t buff[2]={8,0};\n")
        f.write("    buff[1]=data;\n")
        f.write("    _serial->write(buff,2);\n")
        f.write("}\n")
        f.write("void MarkSerial::_SendInt16(int16_t data){\n")
        f.write("    uint8_t buff[3]={16,0,0};\n")
        f.write("    buff[1]=(data&(0xff<<8))>>8;\n")
        f.write("    buff[2]=data&0xff;\n")
        f.write("    _serial->write(buff,3);\n")
        f.write("}\n")
        f.write("void MarkSerial::_SendInt32(int32_t data){\n")
        f.write("    uint8_t buff[5]={32,0,0,0,0};\n")
        f.write("    buff[1]=(data&(0xff<<24))>>24;\n")
        f.write("    buff[2]=(data&(0xff<<16))>>16;\n")
        f.write("    buff[3]=(data&(0xff<<8))>>8;\n")
        f.write("    buff[4]=data&0xff;\n")
        f.write("    _serial->write(buff,5);\n")
        f.write("}\n")
        f.write("void MarkSerial::_SendInt64(int64_t data){\n")
        f.write("    uint8_t buff[9]={64,0,0,0,0,0,0,0,0};\n")
        f.write("    buff[1]=(data&(0xff<<56))>>56;\n")
        f.write("    buff[2]=(data&(0xff<<48))>>48;\n")
        f.write("    buff[3]=(data&(0xff<<40))>>40;\n")
        f.write("    buff[4]=(data&(0xff<<32))>>32;\n")
        f.write("    buff[5]=(data&(0xff<<24))>>24;\n")
        f.write("    buff[6]=(data&(0xff<<16))>>16;\n")
        f.write("    buff[7]=(data&(0xff<<8))>>8;\n")
        f.write("    buff[8]=data&0xff;\n")
        f.write("    _serial->write(buff,9);\n")
        f.write("}\n")
        f.write("void MarkSerial::_SendFloat32(float data){\n")
        f.write("    byte * bb = (byte *) &data;\n")
        f.write("    uint8_t buff[1]={111};\n")
        f.write("    _serial->write(buff,1);\n")
        f.write("    _serial->write(bb,4);\n")
        f.write("}\n")
        f.write("void MarkSerial::_SendString(char data[]){\n")
        f.write("    uint8_t buffS[1]={242};\n")
        f.write("    uint8_t buffE[2]={42,126};\n")
        f.write("    _serial->write(buffS,1);\n")
        f.write("    _serial->print(data);\n")
        f.write("    _serial->write(buffE,2);\n")
        f.write("}\n")
        for i in range(0,len(listVoid)):
            f.write(listVoid[i][8:len(listVoid[i])-1])
            f.write(("{\n"))
            f.write("    _Sendstart();\n")
            f.write("    _SendHands("+str(id_mcu)+","+str(id_topic[i])+");\n")
            for j in range(0,len(dataType[i])):
                f.write(typetoVoid(dataType[i][j],dataName[i][j]))
                if(j<len(dataType[i])-1):
                    f.write("    _Sendcontinue();\n")
                else:
                    f.write("    _Sendstop();\n")
            f.write("}\n")
        f.close
        print(".cpp Done.")
    except:
        print(".cpp Failed.")
    return 0
def convertdatatype(strr):
    if(strr=="uint8"or strr=="uint16" or strr=="uint32" or strr=="uint64" or strr=="int8"or strr=="int16" or strr=="int32" or strr=="int64" ):
        return (strr+"_t")
    elif(strr=="float32" or strr=="float64" ):
        return "float"
    elif(strr=="string"):
        return "char"
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