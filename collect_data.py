import os
import numpy as np
import shutil

try:
    import serial
except:
    os.system("pip3 install pyserial")
try:
    import serial.tools.list_ports
except:
    os.system("pip3 install pyserial")

import serial.tools.list_ports
import warnings
import time

for p in serial.tools.list_ports.comports():
    print("Dev ",p.description)
    pass

arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Generic' in p.description or 'USB' in p.description or 'tty' in p.description or 'Arduino' in p.description
]

if not arduino_ports:
    print("No Arduino Device Found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduino found - using the first')

try:
    
    port = arduino_ports[0] # Comment this line when running on Beaglebone
    # port = "/dev/ttyO1" # UnComment this line when running on Beaglebone
    device = serial.Serial(port, 9600, timeout=1)  # /dev/ttyUSB0
    print("Communication Established with Device.")
    time.sleep(1)

except:

    print("Unable to Initialize ")

count = 0

os.chdir(os.getcwd())

while True:
    character = input("Enter Name of Character: ")
    try:
        os.mkdir(os.getcwd()+"/Data/"+character)
        os.mkdir(os.getcwd()+"/DataA/"+character)
        os.mkdir(os.getcwd()+"/DataG/"+character)
        print("Folder Created Successfully")
    except Exception as e:
        print("Folder already Exist, Data will be appended ", e)
        
    count = len(os.listdir(os.getcwd()+"/Data/"+character))
    
    device.readall()
    print("Waiting for Data: \n")
    device.flushInput()
    while True:
        a = device.readall()
        
        if len(a) > 5:
            try:
                a = a.decode()
                a = a.replace(" ","")
                if("CD" not in a or "EOD" not in a ):
                    print("CORRUPTED DATA-1")
                    raise(NameError)
                else:
                    print("Full Data Received\n")
                    
                a = a.replace("CD","")
                a = a.replace("EOD","")
                a = a.strip()

                dataA = str()
                dataG = str()

                b = a.split("\n")
                # print(b)
                for i in b:
                    print(i)
                    if(i.count(',') == 5):
                        tList = i.split(',')
                        dataA += str(int(tList[0]))+","+str(int(tList[1]))+","+str(int(tList[2]))+"\n"
                        dataG += str(int(tList[3]))+","+str(int(tList[4]))+","+str(int(tList[5]))+"\n"
                        # print('OK')
                    else:
                        print("CORRUPTED DATA-2 at: ",b.index(i))
                        raise(NameError)
                
                print(a)
                time.sleep(0.1)
                verify = input("Enter n to discard data | S to Stop after Saving this| Press Enter to Accept Data : ")
                
                if verify.lower() == 'n':
                    print("Data Discarded.\nWaiting for Data: ")
                else:
                    file = open(os.getcwd()+"/Data/"+character+"/"+str(count)+".csv",'w')
                    file.write(a)
                    file.close()
                    print("Data Successfully Collected to /Data/"+character+"/"+str(count)+".csv")

                    file = open(os.getcwd()+"/DataA/"+character+"/"+str(count)+".csv",'w')
                    file.write(dataA)
                    file.close()
                    print("Data Successfully Collected to /DataA/"+character+"/"+str(count)+".csv")

                    file = open(os.getcwd()+"/DataG/"+character+"/"+str(count)+".csv",'w')
                    file.write(dataG)
                    file.close()
                    print("Data Successfully Collected to /DataG/"+character+"/"+str(count)+".csv")


                    count += 1
                    device.flushInput()
                    print("Waiting for Data: \n")

                    if verify.lower() == 's':
                        break

            except Exception as e:
                print("ERROR OCCURED: ",e)
                print("Waiting for Data: ")
        
