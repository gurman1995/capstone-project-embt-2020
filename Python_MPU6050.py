import os
import numpy as np
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
    if 'Generic' in p.description or 'Arduino' in p.description or 'tty' in p.description
]

if not gsm_ports:
    print("No Arduino Device Found")
if len(gsm_ports) > 1:
    warnings.warn('Multiple Arduino found - using the first')

try:
    port = gsm_ports[0]
    device = serial.Serial(port, 9600, timeout=0.5)  # /dev/ttyUSB0
    print("Communication Established with Device.")
    time.sleep(3)

except:

    print("Unable to Initialize ")
path = "Data/9/"
i = 0
while True:
    a = device.readall()
    if len(a) > 5:
        a = a.decode()
        print(a)
        break
    time.sleep(0.1)

while True:
    a = device.readall()
    if len(a) > 5:
        a = a.decode()
        # if (input("0-discard/1-save: ") == '0'):
        #     continue
        data = a.split("\n\r\n")[1]
        parsed = []
        for i in data.split("\n"):
            i = i.split(",")
            try:
                int(i[0])
                i = list(map(int, i))
                parsed.append(i)
            except:
                pass
        parsed = np.array(parsed).flatten()
        print("Predicted Shape: ")
        predict(parsed)

    time.sleep(0.1)
