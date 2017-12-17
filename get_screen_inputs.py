import numpy as np
import cv2
import time
from grabscreen import grab_screen


def capture_full_screen():

    captured_screen = grab_screen(region=(0,27,640,425))
    rgb_full_screen = cv2.cvtColor(captured_screen, cv2.COLOR_BGR2RGB)
    return rgb_full_screen

#drivingwindow
def capture_drivingwindow():

    captured_screen = grab_screen(region=(0,140,640,245))
    rgb_drivingwindow = cv2.cvtColor(captured_screen, cv2.COLOR_BGR2RGB)
    return rgb_drivingwindow


#race map
def capture_map():

    captured_screen = grab_screen(region=(0,27,170,100))
    rgb_map = cv2.cvtColor(captured_screen, cv2.COLOR_BGR2RGB)
    return rgb_map

#scoreboard
def capture_scoreboard():

    captured_screen = grab_screen(region=(490,31,630,88))
    rgb_scoreboard = cv2.cvtColor(captured_screen, cv2.COLOR_BGR2RGB)
    return rgb_scoreboard

#speedometer
def capture_speedometer():

    captured_screen = grab_screen(region=(205,250,255,275))
    rgb_speedometer = cv2.cvtColor(captured_screen, cv2.COLOR_BGR2RGB)
    return rgb_speedometer

#health meter
def capture_healthmeter():

    captured_screen = grab_screen(region=(268,250,435,270))
    rgb_healthmeter = cv2.cvtColor(captured_screen, cv2.COLOR_BGR2RGB)
    return rgb_healthmeter

#RPM gauge
def capture_RPMgauge():

    captured_screen = grab_screen(region=(255,295,385,395))
    rgb_RPMgauge = cv2.cvtColor(captured_screen, cv2.COLOR_BGR2RGB)
    return rgb_RPMgauge

#Steering wheel
def capture_steeringwheel():

    captured_screen = grab_screen(region=(180,270,460,420))
    rgb_steeringwheel = cv2.cvtColor(captured_screen, cv2.COLOR_BGR2RGB)
    return rgb_steeringwheel

#Gear box to shift gears
def capture_gears():

    captured_screen = grab_screen(region=(525,325,610,410))
    rgb_gears = cv2.cvtColor(captured_screen, cv2.COLOR_BGR2RGB)
    return rgb_gears

#Left rearview mirror
def capture_leftRvm():

    captured_screen = grab_screen(region=(0,250,130,300))
    rgb_leftRvm = cv2.cvtColor(captured_screen, cv2.COLOR_BGR2RGB)
    return rgb_leftRvm


#Right rearview mirror
def capture_rightRvm():

    captured_screen = grab_screen(region=(510,250,(510+130),300))
    rgb_rightRvm = cv2.cvtColor(captured_screen, cv2.COLOR_BGR2RGB)
    return rgb_rightRvm


def main():

    while True:

        #Capture game window and convert from BGR to RGB
        full_screen = capture_full_screen()
        drivingwindow = capture_drivingwindow()
        map_image = capture_map()
        scoreboard = capture_scoreboard()
        speedometer = capture_speedometer()
        healthmeter = capture_healthmeter()
        RPMgauge = capture_RPMgauge()
        steeringwheel = capture_steeringwheel()
        gears = capture_gears()
        leftRvm = capture_leftRvm()
        rightRvm = capture_rightRvm()

       
        #cv2.imshow('full screen',full_screen)
        cv2.imshow('driving window',drivingwindow)
        #cv2.imshow('map',map_image)
        #cv2.imshow('scoreboard',scoreboard)
        #cv2.imshow('speedometer',speedometer)
        #cv2.imshow('healthmeter',healthmeter)
        #cv2.imshow('RPMgauge',RPMgauge)
        cv2.imshow('steering wheel',steeringwheel)
        #cv2.imshow('gears',gears)
        #cv2.imshow('leftRvm',leftRvm)
        #cv2.imshow('rightRvm',rightRvm)


        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
       

main()

