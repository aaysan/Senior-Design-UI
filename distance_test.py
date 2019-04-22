# import bluetooth
import struct
import requests
import os
import time
import serial


ser = serial.Serial('/dev/rfcomm0', baudrate=9600)
ser.reset_input_buffer()

data = ""
os.system("vcgencmd display_power 0")
while(1):
    data += ser.read(1).decode("utf-8")
    print(data)
    if("Detected" in data):
        ## print(data)
        os.system("vcgencmd display_power 1")
        data = ""
        # time.sleep(4)
        ser.reset_input_buffer()
        time.sleep(3.424)
        break


'''
while True:
	

b_addr = "20:19:02:13:00:59"
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((b_addr,port))
'''
