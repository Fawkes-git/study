import cv2
import numpy as np
import time, math, serial, os.path, csv

from time import sleep
#path = os.path.join(os.getcwd(),'train.tsv')
path = "/Users/takato/study/analysis/data/train.tsv"
ser = serial.Serial('/dev/cu.usbmodem14511',9600) #Connection to Arduino
start_time = time.time()

def serial_read(angle,bytes_data,elapsed_time):
    serial_data = bytes_data.decode('utf-8')
    serial_data = serial_data.rstrip('\r\n')
    str_data = str(elapsed_time) + '\t' + serial_data + str(angle)
    print(str_data)
    write_csv(str_data)

def write_csv(str_data):
    file = open(path, 'a')
    writer = csv.writer(file, lineterminator='\n')
    csvlist = []
    csvlist.append(str_data)
    writer.writerow(csvlist)
    file.close()

def mask_color(mask,frame):
    mu = cv2.moments(mask, False)
    if mu["m00"] != 0:
        x,y = int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
    
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask = mask)
    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    vector = np.array([x,y])

    return vector

def main():
    cap = cv2.VideoCapture(0)

    #width = 640
    #height = 480
    #width = 1280
    #height = 960
    width = 1920
    height = 1080


    fps = 60
    # define camera settings
    cap.set(3,width)  # Width
    cap.set(4,height)  # Height
    cap.set(5,fps)   # FPS

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

    # define range of red color in HSV
    lower_red = np.array([0,100,100])
    upper_red = np.array([2,255,255])
    # define range of green color in HSV
    lower_green = np.array([45,50,50])
    upper_green = np.array([75,255,255])

    # define range of blue color in HSV
    lower_blue = np.array([100,100,50])
    upper_blue = np.array([140,255,255])

    # define range of yellow color in HSV
    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([30,255,255])

    while(1):
        # Take each frame
        _, frame = cap.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get colors
        #mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        #vec_red = mask_color(mask_red,frame)
        vec_green = mask_color(mask_green,frame)
        vec_blue = mask_color(mask_blue,frame)
        vec_yellow = mask_color(mask_yellow,frame)

        #vec_m = vec_red - vec_green
        vec_p = vec_green - vec_blue
        vec_i = vec_blue - vec_yellow

        #print(vec_p,vec_i)

        #mp = math.degrees(math.acos(vec_m.dot(vec_p)/(np.linalg.norm(vec_m)*np.linalg.norm(vec_p))))
        angle = math.degrees(math.acos(vec_p.dot(vec_i)/(np.linalg.norm(vec_p)*np.linalg.norm(vec_i))))

        #mp = round(mp)
        angle = round(angle)
        #print(mp,pip)
        print(angle)

        bytes_data = ser.readline()
        serial_read(angle,bytes_data,elapsed_time)

        #cv2.circle(frame, (vec_red[0],vec_red[1]), 6, (0,0,0), -1)
        cv2.circle(frame, (vec_green[0],vec_green[1]), 6, (0,0,0), -1)
        cv2.circle(frame, (vec_blue[0],vec_blue[1]), 6, (0,0,0), -1)
        cv2.circle(frame, (vec_yellow[0],vec_yellow[1]), 6, (0,0,0), -1)

        #cv2.line(frame,(vec_red[0],vec_red[1]),(vec_green[0],vec_green[1]),(0,0,0), 3)
        cv2.line(frame,(vec_green[0],vec_green[1]),(vec_blue[0],vec_blue[1]),(0,0,0), 3)
        cv2.line(frame,(vec_blue[0],vec_blue[1]),(vec_yellow[0],vec_yellow[1]),(0,0,0), 3)
        frame = cv2.flip(frame, 1)

        fontType = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(frame, 'MP:{0} degrees'.format(str(mp)), (10, 420), fontType, 1, (0, 255, 0))
        cv2.putText(frame, 'Joint angle:{0} degrees'.format(str(pip)), (10, 30), fontType, 1, (0, 0, 0))
        cv2.imshow('frame',frame)

        out.write(frame)

        # Interrupt
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
             break


    cv2.destroyAllWindows()

if __name__=='__main__':
    main()