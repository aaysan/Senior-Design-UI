# import bluetooth
import struct
import requests
import os
import time
import numpy as np
import cv2

b_addr = "98:D3:11:FC:18:90"
port = 1
##sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
##sock.connect((b_addr,port))
NGROK = 'http://35.243.174.102:8080/get_name'
CLIENT_ID = "Your_applicatoins_client_id"


##sock.close()


def get_name():
    # os.system("raspistill -vf -o tmp.png")


    cap = cv2.VideoCapture(0)
    time.sleep(0.5)
    # while True:
    ret, frame = cap.read()
    cv2.imwrite("tmp.png",frame)
        # input1 = input()
        # if input1 == "o":
        #     break



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
    sock.send(text)
    data = ""
    while(1):
        data += sock.recv(1).decode("utf-8")
        if 'cc done dd\n' in data:
            print('Done closet open')
            break
    return


def closet_close():
    sock.send('ccc')
    data = ""
    while(1):
        data += sock.recv(1).decode("utf-8")
        if 'cc done dd\n' in data:
            print('Done closet close')
            break
    return


def read_data():
    sock.send('rrr')

    count = 0
    data = ""
    while(1):
        data += sock.recv(1).decode("utf-8")
        #print(data)
        if(' ts' in data and 'te\n' in data):
            idx = data.find(" ts")
            print(data[idx:])
            data = ""
            count += 1

        elif(' hs' in data and 'he\n' in data):
            idx = data.find(" hs")
            print(data[idx:])
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


    '''


    try:
        size = 4 ;
        real_data = b''
        while len(real_data) != size:
            data = sock.recv(1)
            real_data += data;

        print(real_data)
        tmp = struct.unpack("f",real_data)
        print(tmp)

##        text = input("give me a text:")
##        print("\nread")
##        sock.send(text)
##
    except KeyboardInterrupt:
        break
        '''
# text = input("Sending: ")
# sock.send(text)
# closet_close()
# read_data()
# sock.close()
