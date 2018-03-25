import numpy as np
import cv2
import time

from get_screen_inputs import capture_drivingwindow

def main():

    while True:

        drivingwindow = capture_drivingwindow()
        cv2.imshow('driving window',drivingwindow)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()




