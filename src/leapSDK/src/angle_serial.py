################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys, thread, time, math, serial, os.path, csv
sys.path.append("/Users/takato/study/LeapSDK/lib/")
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
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

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']



    def on_init(self, controller):
        print ("Initialized")

    def on_connect(self, controller):
        print ("Connected")

    def on_disconnect(self, controller):
        print ("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
 
        # Get hands
        for hand in frame.hands:
            current_time = time.time()
            elapsed_time = current_time - start_time
            elapsed_time = round(elapsed_time,1)
            if elapsed_time > 30.2:
              sys.exit()

            finger = hand.fingers[1]
            #m = finger.bone(0).direction
            p = finger.bone(1).direction
            i = finger.bone(2).direction
            #d = finger.bone(3).direction 

            angle = math.degrees(math.acos(i.dot(p)))
            bytes_data = ser.readline()

            #print("1: %.1f degrees" %math.degrees(math.acos(d.dot(i))))
            #print("2: %.1f degrees" %math.degrees(math.acos(i.dot(p))))
            #print("3: %.1f degrees" %math.degrees(math.acos(p.dot(m))))
            serial_read(angle,bytes_data,elapsed_time)


        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ("")

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"


def main():

    if not(os.path.exists(path)):
        file = open(path, 'w')
        file.write('Time'+'\t'+'Volt'+'\t'+'Leap_angle'+'\n')
        file.close()

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    #print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
