#coding utf-8
import serial
import time
import readchar
from tqdm import tqdm
import pandas as pd
import os.path

def serial_read(gesture,length,trial):
    for iter in range(1,301):
        bytes_data = ser.readline()
        str_data = bytes_data.decode('utf-8')
        str_data = str(iter) +"\t"+str(trial) +"\t"+ str_data.rstrip('\r\n') + str(gesture) +'\t'+length+'\n'
        print(str_data)

        file = open(path, 'a')
        file.write(str_data)
        file.close()

if __name__=="__main__":
    ser = serial.Serial('/dev/cu.usbmodem14511',9600) #Connection to Arduino
    print('Type Your Name')
    name = input()
    path = "/Users/takato/study/analysis/data/"+name+"_train.tsv"
  
    if not(os.path.exists(path)):
        print("type length of your finger")
        length = input()
        file = open(path, 'w')
        file.write('Time'+'\t'+'Trial_id'+'\t'+'Volt'+'\t'+'Gesture'+'\t'+"Length"+'\n')
        file.close()

    print('---------------------')
    print(' Space: Collect data')
    print('   q  : Quit')
    print('---------------------')

    list_gesture = [0,15,30,45,60,75,90]

    for gesture in list_gesture:

        for iter in tqdm(range(1,11)):
            print("your gesture is",gesture)
            while True:
                string = bytes(readchar.readchar(),'utf-8')
                if string  == bytes(' ','utf-8') or string == bytes('q','utf-8'):
                    break

            if string == bytes(' ','utf-8'):
                print('Collecting...')
                ser.write(string)
                serial_read(gesture,length,iter)

            elif string == bytes('q','utf-8'):
                 break




