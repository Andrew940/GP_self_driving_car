#Original code from Mithi Sevilla
#converted to a library for easy access
#https://github.com/mithi/basic-lane-detection
#Robo-Geek is proud of being part of the open-source community, we also
#share our projects at:
#https://github.com/robogeekcanada

import numpy as np
import cv2
import sld.simple_lane_detection as sld

param = {
    #blur parameters
    'kernel_size': 5, 
    
    #canny transform parameters
    'canny_lo': 200, 
    'canny_hi': 300, 

    #region of interest parameters
    'ax_coef': 6.0/25,
    'bx_coef': 18.0/25,
    'cy_coef': 0.6,
    'dy_coef': 0.6,
    'maxy_coef': 1.0,
    'maxx_coef': 1.0,
    'startx_coef': 0.0,

    #hough parameters
    'rho': 1, 
    'theta_coef': 1, 
    'min_votes': 10, 
    'min_line_length': 10, 
    'max_line_gap': 10
}


def process_image(image):

    raw_image = np.copy(image)
  
    gray_image = sld.gray(raw_image)    

    blur_image = sld.reduce_noise(gray_image, param['kernel_size'])
    
    edge_image = sld.get_edges(blur_image, param['canny_lo'], param['canny_hi'])
  
    x, y = image.shape[1], image.shape[0]
    vertices = sld.get_vertices(x, y, param['ax_coef'], param['bx_coef'],
                                param['cy_coef'], param['dy_coef'],
                                param['maxx_coef'], param['maxy_coef'],
                                param['startx_coef'])

    coord1 = vertices[0][0]
    coord2 = vertices[0][1]
    coord3 = vertices[0][2]
    coord4 = vertices[0][3]

    x1 = coord1[0]
    y1 = coord1[1]

    x2 = coord2[0]
    y2 = coord2[1]

    x3 = coord3[0]
    y3 = coord3[1]

    x4 = coord4[0]
    y4 = coord4[1]


    lanes_image = np.copy(raw_image)
    cv2.line(lanes_image, (x1,y1), (x2,y2),(255,0,0),5)
    cv2.line(lanes_image, (x3,y3), (x4,y4),(255,0,0),5)
    cv2.line(lanes_image, (x2,y2), (x3,y3),(255,0,0),5)


    #return lanes_image

    roi = sld.get_roi(edge_image, vertices)  
    mask_image = sld.mask(edge_image, roi)

    #return mask_image
  
    lines = sld.get_lines(mask_image, param['rho'], param['theta_coef'],
                           param['min_votes'], param['min_line_length'],
                           param['max_line_gap'])
   
    line_image, line_mean = sld.draw(lines, raw_image)

    x1 = line_mean[0]
    y1 = line_mean[1]
    x2 = line_mean[2]
    y2 = line_mean[3]

    if (x1 & y1 & x2 & y2 != 0):
        slope, intercept = np.polyfit((x1,x2), (y1,y2), 1)
        #print(slope, line_mean)

        if(slope > -1.6 and slope < -1.4):
            print("going straight")

    return mask_image, line_image


if __name__ == "__main__":

    cap = cv2.VideoCapture('sld_videos/gpcropped_video.mp4')

    while(cap.isOpened()):
        ret, frame = cap.read()

        edges_image, lines_image = process_image(frame)

        cv2.imshow('edges',edges_image)
        cv2.imshow('lines',lines_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
