#Original code from Mithi Sevilla
#converted to a library for easy access
#https://github.com/mithi/basic-lane-detection
#Robo-Geek is proud of being part of the open-source community, we also
#share our projects at:
#https://github.com/robogeekcanada


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
#%matplotlib inline

import math

# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML



#File manipulation functions
def read(path):
    return mpimg.imread(path)

def show(image):
    print('This image is:', type(image), 'with dimensions:', image.shape)
    plt.imshow(image)

def save(image, path = 'test.png'):
    plt.imsave(path, image)

def convert_to_color(image):
    return np.dstack((image, image, image))

# Image Conversion functions

def gray(raw_image):
    '''convert the colored imaged to grayscale image'''
    return cv2.cvtColor(raw_image, cv2.COLOR_RGB2GRAY)  

def reduce_noise(gray_image, kernel_size):
    '''reduce noise of grayscale image using gausian blur'''
    return cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), 0)

def get_edges(blur_image, low_threshold, high_threshold):
    '''find edges using canny transform algorithm'''
    return cv2.Canny(blur_image, low_threshold, high_threshold)

def get_vertices(x, y, axc, bxc, cyc, dyc, maxyc = 1.0, maxxc = 1.0, startxc = 0.0):
    ax = int(axc*x)
    bx = int(bxc*x)
    cy = int(cyc*y)
    dy = int(dyc*y)
    maxy = int(maxyc*y)
    maxx = int(maxxc*x)
    startx = int(startxc*x)
    bottom_left = (startx, maxy)
    top_left = (ax, cy)
    top_right = (bx, dy)
    bottom_right = (maxx, maxy)
    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    return vertices


def get_roi(edge_image, vertices, ignore_value = 255):
    '''get the polygon to be used to block out everything in the image except the region of interest'''
    roi = np.zeros_like(edge_image)
    cv2.fillPoly(roi, vertices, ignore_value)
    return roi

def mask(edge_image, roi):
    '''block out everything in the image except the edges in the region of interest'''
    return cv2.bitwise_and(edge_image, roi)

def get_lines(masked_edge_image, rho, theta_coef, min_votes, min_line_length, max_line_gap):
    '''convert edges into lines using hough transform algorithm '''
    theta = theta_coef*np.pi/180
    return cv2.HoughLinesP(masked_edge_image, rho, theta, min_votes, np.array([]), minLineLength = min_line_length, maxLineGap = max_line_gap)

def draw(lines, image, color=[255, 0, 0], thickness = 2, thresh = 0.5):
    ''' draw the lines on a blank image'''
    lined_image = np.copy(image)*0
  
    if lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:
                slope, intercept = np.polyfit((x1,x2), (y1,y2), 1)
                if abs(slope) > thresh:
                    cv2.line(lined_image, (x1, y1), (x2, y2), color, thickness)
        
    return lined_image


# equation of a line: y = slope*x + intercept 
# left lane has a positive slope, right lane has a negative slope 

def extrapolate_lines(lines, image, color=[255, 0, 0], thickness = 10,
                      positive_thresh = 0.5, negative_thresh = 0.5):
    
    imshape = image.shape
    image = np.copy(image)*0
    
    #initialize minimum and maximum y coordinate 
    minimum_y = image.shape[0] 
    maximum_y = image.shape[0]
  
    #initialize groups of values into empty lists
    left_slopes = []
    left_xs = []
    left_ys = []   
    right_slopes = []
    right_xs = []
    right_ys = []
  
    # segregate the small line segments into the left lane group or right lane group
    if lines is not None:  
        for line in lines:
            for x1,y1,x2,y2 in line:
        
                # get the slope and intercept of the line (as defined by two points) using the polyfit function
                slope, intercept = np.polyfit((x1,x2), (y1,y2), 1)
            
                if (slope > positive_thresh): #if positive slope, put value to left lane group
                  left_slopes += [slope]
                  left_xs += [x1, x2]
                  left_ys += [y1, y2]
                elif (slope < negative_thresh): #if negative slope, put value to right lane group
                  right_slopes += [slope]
                  right_xs += [x1, x2]
                  right_ys += [y1, y2]
        
                # update the minimum y_coordinate based on values seen
                minimum_y = min(min(y1, y2), minimum_y)
  
    #average all the values in each group to get the slope, x, and y
    left_slope = np.mean(left_slopes)
    left_x = np.mean(left_xs)
    left_y = np.mean(left_ys)
    right_slope = np.mean(right_slopes)
    right_x = np.mean(right_xs)
    right_y = np.mean(right_ys)
    
    #derive the intercept using the equation of the line and average value
    left_intercept = left_y - (left_slope * left_x)
    right_intercept = right_y - (right_slope * right_x)

    if ((len(left_slopes) > 0) and (len(right_slopes) > 0)): #make sure we have points in each group
        #derive the x coordinate using the equation of the lines and derived values
        upper_left_x = int((minimum_y - left_intercept) / left_slope)
        lower_left_x = int((maximum_y - left_intercept) / left_slope)
        upper_right_x = int((minimum_y - right_intercept) / right_slope)
        lower_right_x = int((maximum_y - right_intercept) / right_slope)
    
        #draw the line based on two points 
        cv2.line(image, (upper_left_x, minimum_y), (lower_left_x, maximum_y), color, thickness)
        cv2.line(image, (upper_right_x, minimum_y), (lower_right_x, maximum_y), color, thickness)
    
    return image


def overlap(first_image, second_image, α = 0.8, β = 0.5, λ = 0.0):
    '''first_image * α + second_image * β + λ (colored)'''
    return cv2.addWeighted(first_image, α, second_image, β, λ)








