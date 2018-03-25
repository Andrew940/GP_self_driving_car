import numpy as np
import cv2
import time

from get_screen_inputs import capture_drivingwindow
from sld_gp import param, process_image

def main():

    while True:

        drivingwindow = capture_drivingwindow()

        edges_image, lines_image = process_image(drivingwindow)
        
        cv2.imshow('driving window',drivingwindow)
        cv2.imshow('edges',edges_image)
        cv2.imshow('lines',lines_image)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

main()




