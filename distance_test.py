# import bluetooth
import struct
import requests
import os
import time
import serial


ser = serial.Serial('/dev/rfcomm0', baudrate=9600)
ser.reset_input_buffer()

data = ""
#os.system("vcgencmd display_power 0")
os.system("xset -display :0 dpms force off")
while(1):
    data += ser.read(1).decode("utf-8")
    print(data)
    if("Detected" in data):
        ## print(data)
        #os.system("vcgencmd display_power 1")
        os.system("xset -display :0 dpms force on")
        data = ""
        #time.sleep(4)
        ser.reset_input_buffer()
        ser.flush()
        time.sleep(4)
        break


'''
while True:
	

b_addr = "20:19:02:13:00:59"
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((b_addr,port))
'''
