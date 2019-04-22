import serial
import struct
import requests
import os
import time
import numpy as np

sock = None

b_addr = "20:19:02:13:00:59"
port = 1
NGROK = 'http://35.243.174.102:8080/get_name'
CLIENT_ID = "Your_applicatoins_client_id"

def _blt_init():
    ser = serial.Serial('/dev/rfcomm0', baudrate=9600)
    ser.reset_input_buffer()
    return ser

def get_name():
    os.system("raspistill -t 1000 -vf -o tmp.png")

    t0 = time.time()
    files = {'file': open("tmp.png","rb")}
    response = requests.post(NGROK,files=files)

    t1 = time.time()
    print(response.text)
    return response.text

    print(t1-t0)

def closet_open(displacement):
    if displacement < 10:
        text = 'o0' + str(displacement)
    else:
        text = 'o' + str(displacement)

    ser = _blt_init()
    ser.write(text.encode("utf-8"))
    data = ""
    while(1):
        data += ser.read(1).decode("utf-8")
        if 'cc done dd\n' in data:
            print('Done closet open')
            break
    return


def closet_close():
    ser = _blt_init()
    ser.write(b'ccc')
    data = ""
    while(1):
        data += ser.read(1).decode("utf-8")
        if 'cc done dd\n' in data:
            print('Done closet close')
            break
    return


def read_data():
    ser = _blt_init()
    ser.write(b'rrr')
    count = 0
    data = ""
    while(1):
        data += ser.read(1).decode("utf-8")
        #print(data)
        if(' ts' in data and 'te\n' in data):
            idx = data.find(" ts")
            print(data[idx:])
            indoort = data[idx:]
            data = ""
            count += 1
        elif(' hs' in data and 'he\n' in data):
            idx = data.find(" hs")
            print(data[idx:])
            indoorh = data[idx:]	
            data = ""
            count += 1
        elif(' ms' in data and 'me\n' in data):
            idx = data.find(" ms")
            print(data[idx:])
            data = ""
            count += 1
        else:
            pass
        if(count == 3):
            break
    return indoort,indoorh

