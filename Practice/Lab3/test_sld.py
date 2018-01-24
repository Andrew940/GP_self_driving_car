#Original code from Mithi Sevilla
#converted to a library for easy access
#https://github.com/mithi/basic-lane-detection
#Robo-Geek is proud of being part of the open-source community, we also
#share our projects at:
#https://github.com/robogeekcanada

import numpy as np
import simple_lane_detection as sld

# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML

param = {
    #blur parameters
    'kernel_size': 5, 
    
    #canny transform parameters
    'canny_lo': 100, 
    'canny_hi': 200, 

    #region of interest parameters
    'ax_coef': 10.0/25,
    'bx_coef': 14.0/25,
    'cy_coef': 0.6,
    'dy_coef': 0.6,
    'maxy_coef': 1.0,
    'maxx_coef': 1.0,
    'startx_coef': 0.0,

    #hough parameters
    'rho': 1, 
    'theta_coef': 1, 
    'min_votes': 30, 
    'min_line_length': 20, 
    'max_line_gap': 20
}


def pipeline(path, file, name, param = param):
    
    name = path + name

    raw_image = sld.read(path + file)
    image = sld.read(path + file)
    sld.save(image, path = name + '1-raw.png')
  
    gray_image = sld.gray(image)
    sld.save(gray_image, path = name + '2-grey.png')
    
    blur_image = sld.reduce_noise(gray_image, param['kernel_size'])
    sld.save(blur_image, path = name + '3-blur.png')
    
    edge_image = sld.get_edges(blur_image, param['canny_lo'], param['canny_hi'])
    sld.save(edge_image, path = name + '4-edges.png')
  
    x = image.shape[1]
    y = image.shape[0]
    vertices = sld.get_vertices(x, y, param['ax_coef'], param['bx_coef'],
                                param['cy_coef'], param['dy_coef'],
                                param['maxy_coef'], param['maxx_coef'], param['startx_coef'])
  
    roi = sld.get_roi(edge_image, vertices)
    sld.save(roi, path = name + '5-roi.png')
  
    mask_image = sld.mask(edge_image, roi)
    sld.save(mask_image, path = name + '6-mask.png')
  
    lines = sld.get_lines(mask_image, param['rho'], param['theta_coef'],
                           param['min_votes'], param['min_line_length'],
                           param['max_line_gap'])
   
    line_image = sld.draw(lines, raw_image)
    sld.save(line_image, path = name + '7-lines.png')
  
  
    line_image2 = sld.extrapolate_lines(lines, raw_image)
    sld.save(line_image2, path = name + '8-lines.png')

    image = sld.overlap(line_image, raw_image)
    sld.save(image, path = name + '9-overlap.png')

    image = sld.overlap(line_image2, raw_image)
    sld.save(image, path = name + '10-overlap.png')


def process_image(image):

    raw_image = np.copy(image)
    gray_image = sld.gray(image)    
    blur_image = sld.reduce_noise(gray_image, param['kernel_size'])
    
    edge_image = sld.get_edges(blur_image, param['canny_lo'], param['canny_hi'])
  
    x, y = image.shape[1], image.shape[0]
    vertices = sld.get_vertices(x, y, param['ax_coef'], param['bx_coef'],
                                param['cy_coef'], param['dy_coef'],
                                param['maxx_coef'], param['maxy_coef'],
                                param['startx_coef'])
    
    roi = sld.get_roi(edge_image, vertices)  
    mask_image = sld.mask(edge_image, roi)
  
    lines = sld.get_lines(mask_image, param['rho'], param['theta_coef'],
                           param['min_votes'], param['min_line_length'],
                           param['max_line_gap'])
   
    #line_image = sld.draw(lines, raw_image)  
    #result = sld.overlap(line_image, raw_image)
 
    line_image2 = sld.extrapolate_lines(lines, raw_image) 
    result = sld.overlap(line_image2, raw_image)

    return result


def main():


    #Test Pipeline function
    pipeline(path = 'test_images/', file = 'solidWhiteCurve.jpg', name = 'A')
    pipeline(path = 'test_images/', file = 'solidWhiteRight.jpg', name = 'B')
    pipeline(path = 'test_images/', file = 'solidYellowCurve.jpg', name = 'C')
    pipeline(path = 'test_images/', file = 'solidYellowCurve2.jpg', name = 'D')
    pipeline(path = 'test_images/', file = 'solidYellowLeft.jpg', name = 'E')
    pipeline(path = 'test_images/', file = 'whiteCarLaneSwitch.jpg', name = 'F')


    #Test process image
    white_output = 'white.mp4'
    clip1 = VideoFileClip("videos/solidWhiteRight.mp4")
    white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
    white_clip.write_videofile(white_output, audio=False)

    yellow_output = 'yellow.mp4'
    clip2 = VideoFileClip('videos/solidYellowLeft.mp4')
    yellow_clip = clip2.fl_image(process_image)
    yellow_clip.write_videofile(yellow_output, audio=False)



  
main()
