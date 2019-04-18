import bluetooth
import struct
import requests
import os
import time


b_addr = "20:19:02:13:00:59"
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((b_addr,port))

received = False

data = ""
os.system("vcgencmd display_power 0")
while(1):
    data += sock.recv(1).decode("utf-8")
    print(data)
    if("Detected" in data):
        ## print(data)
        os.system("vcgencmd display_power 1")
        data = ""
        break
sock.close()

