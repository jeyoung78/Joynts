# This file is to test if a Python Script is capable of reading what Arduino Nano sends from serial port.

import serial
import time

# Adjust this to your Arduino's serial port name and baud rate
ser = serial.Serial('COM3', 500000)
trigger = 0
thumbDown = False
thumbSide = False
pointDown = False
pointSide = False
middleDown = False


try:
    while True:
        # Read a line from serial
        line = ser.readline().decode('utf-8').strip()

        # Convert the comma-separated string to a list of integers
        data = list(map(str, line.split(',')))

        # Print the entire array
        # print(data)

        thumbOne = float(data[0])
        thumbTwo = float(data[1])
        pointOne = float(data[2])
        pointTwo = float(data[3])
        middleOne = float(data[4])

        # print(thumbOne)

    
        if pointDown == True or pointSide == True or middleDown == True or thumbDown == True or thumbSide == True:
            pass
        elif (pointOne > 2.5 and pointDown == False and trigger != 3):
            pointDown = True
            trigger = 1
            with open('morse.txt', 'w') as file:
                # Write content to the file
                file.write(str([[True,False,False,False,False]]))
            # print("trig1")
            time.sleep(2)
        elif (pointTwo > 1.5 and pointSide == False and trigger != 3):
            pointSide = True
            trigger = 2
            with open('morse.txt', 'w') as file:
                # Write content to the file
                file.write(str([[False,True,False,False,False]]))
            time.sleep(2)
        elif (middleOne > 3 and middleDown == False):
            middleDown = True
            trigger = 3
            with open('morse.txt', 'w') as file:
                # Write content to the file
                file.write(str([[False,False,True,False,False]]))
            time.sleep(3)
        elif (thumbOne > 2.5 and thumbDown == False):
            thumbDown = True
            trigger = 4
            with open('morse.txt', 'w') as file:
                # Write content to the file
                file.write(str([[False,False,False,True,False]]))
            time.sleep(2)
        elif (thumbTwo > 2 and thumbSide == False):
            thumbSide = True
            trigger = 5
            with open('morse.txt', 'w') as file:
                # Write content to the file
                file.write(str([[False,False,False,False,True]]))
            time.sleep(2)
        else:
            pointDown = False
            pointSide = False
            middleDown = False
            thumbDown = False
            thumbSide = False
            trigger = 0

        if pointDown == True or pointSide == True or middleDown == True or thumbDown == True or thumbSide == True:
            # print("notrig")
            if (pointOne < -2.5 and pointDown == True):
                pointDown = False
                # trigger = 1
            elif (pointTwo < -1 and pointSide == True):
                pointSide = False
                #trigger = 2
            elif (middleOne < -2.5 and middleDown == True):
                middleDown = False
                #trigger = 3
            elif (thumbOne < -2 and thumbDown == True):
                thumbDown = False
                #trigger = 4
            elif (thumbTwo < -2 and thumbSide == True):
                thumbSide = False
                #trigger = 5
        print(trigger)
    

        

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()

'''

Test Result: The Python script outputs [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], as intended.

'''