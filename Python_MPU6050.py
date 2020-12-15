import os
import numpy as np
import joblib
from numpy.lib.npyio import load
import utils
import multiprocessing


input_shape = utils.training_fun("Data")
clf=joblib.load("svc_model.sav")
en=joblib.load("encoder_model.sav")



def writeFile(data):
    f1 = open("output.txt",'w')
    f1.write(data+'\n')
    f1.close()

def lcd():
    os.system("./lcd")

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
from deploy import predict


for p in serial.tools.list_ports.comports():
    print("Dev ",p.description)
    pass

gsm_ports = [
     p.device
     for p in serial.tools.list_ports.comports()
     if 'Generic' in p.description or 'USB' in p.description or 'tty' in p.description or 'Arduino' in p.description
 ]

if not gsm_ports:
    print("No Arduino Device Found")
if len(gsm_ports) > 1:
    warnings.warn('Multiple Arduino found - using the first')

try:
    port = gsm_ports[0] # Comment this line when running on Beaglebone
    #port = "/dev/ttyO1" # UnComment this line when running on Beaglebone
    print("Port USed: ",port)
    device = serial.Serial(port, 9600, timeout=2)  # /dev/ttyUSB0
    print("Communication Established with Device.")
    time.sleep(1)

except:
    print("Unable to Initialize Hc-12")


print('STARTED')
i = 0

while True:
    print("Waiting Initialization")
    a = device.readall()
    if len(a) > 5:
        a = a.decode()
        print(a)
        break
    time.sleep(0.1)

print("Waiting for Data: ")
device.flushInput()

t1 = multiprocessing.Process(target = lcd)
t1.start()

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
                print("Full Data Received")
                
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
                    writeFile("CORRUPTED DATA")
                    raise(NameError)
            
            #data = a.split("\n")[1]
            #data = dataA.split("\n")[:-1]
            data = dataG.split("\n")[:-1]
            print(data)
            
            pred_out = utils.predicting_fun(input_shape,data,en,clf)
            print(pred_out)
            writeFile(str(pred_out))

        except Exception as e:
            print("ERROR OCCURED: ", e)
            device.flushInput()
            print("Waiting for Data: ")

    time.sleep(0.1)
    
