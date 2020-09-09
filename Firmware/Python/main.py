#!/usr/bin/python3
import time
import threading
import os
import subprocess
import RPi.GPIO as GPIO

# pihat pin
led_pin = 17
pwm_pin = 13
reboot_pin = 16
shutdown_pin = 26

# init GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.OUT)
pwm = GPIO.PWM(pwm_pin, 100)
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(reboot_pin, GPIO.IN)
GPIO.setup(shutdown_pin, GPIO.IN)

# main loop of program
print("\nPress Ctl C to quit \n")
dc = 0
pwm.start(dc)
try:
    time.sleep(1)
    while(1):
        # get temperature
        file = open("/sys/class/thermal/thermal_zone0/temp")
        temp = float(file.read()) / 1000.00
        temp = float('%.2f' % temp)
        file.close()
        print("temp : %.2f %sC" % (temp, chr(176)))
        dc = 0
        if(temp > 40):
            dc = 40
        if(temp > 50):
            dc = 50
        if(temp > 60):
            dc = 60
        if(temp > 70):
            dc = 80
        if(temp > 80):
            dc = 100

        pwm.ChangeDutyCycle(dc)
        print("Fan duty cycle : ", dc)

        if GPIO.input(reboot_pin) == GPIO.LOW:
            print("Reboot button pressed")
            time.sleep(5)
            subprocess.call("reboot")
        if GPIO.input(shutdown_pin) == GPIO.LOW:
            print("Shutdown button pressed")
            time.sleep(5)
            subprocess.call(["shutdown", "-r", "now"])

        time.sleep(2)

except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")

pwm.stop()
GPIO.cleanup()
