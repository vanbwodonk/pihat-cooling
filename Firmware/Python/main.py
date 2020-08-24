#!/usr/bin/python
import time
import threading
import os

try:
    time.sleep(1)
    while(1):
        # get temp
        file = open("/sys/class/thermal/thermal_zone0/temp")  
        temp = float(file.read()) / 1000.00  
        temp = float('%.2f' % temp)
        file.close()
        #print("temp :" , temp , chr(176) , "C")
        print("temp : %.2f %sC" %(temp,chr(176)))
        time.sleep(3)

except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")
