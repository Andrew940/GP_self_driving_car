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
    'kernel_size': 3, 
    
    #canny transform parameters
    'canny_lo': 50, 
    'canny_hi': 150, 

    #region of interest parameters
    'ax_coef': 0.41,
    'bx_coef': 0.60,
    'cy_coef': 0.65,
    'dy_coef': 0.65,
    'maxy_coef': 0.9,
    'maxx_coef': 0.85,
    'startx_coef': 0.15,

    #hough parameters
    'rho': 1, 
    'theta_coef': 1, 
    'min_votes': 20, 
    'min_line_length': 50, 
    'max_line_gap': 20
}

def process(image):

    raw_image = np.copy(image)

    gray_image = sld.gray(image)    
    blur_image = sld.reduce_noise(gray_image, param['kernel_size'])
    
    edge_image = sld.get_edges(blur_image, param['canny_lo'], param['canny_hi'])
  
    #return convert_to_color(edge_image) #check if canny parameters detect edges of lanes

    x = image.shape[1]
    y = image.shape[0]
    vertices = sld.get_vertices(x, y, param['ax_coef'], param['bx_coef'],
                                param['cy_coef'], param['dy_coef'],
                                param['maxy_coef'], param['maxx_coef'], param['startx_coef'])
  
    roi = sld.get_roi(edge_image, vertices)
    mask_image = sld.mask(edge_image, roi)
  
    #return overlap(convert_to_color(roi), raw_image) #check if roi is good
    
    lines = sld.get_lines(mask_image, param['rho'], param['theta_coef'],
                                param['min_votes'], param['min_line_length'],
                                param['max_line_gap'], )
   
    #line_image = draw(lines, raw_image, thresh = 0.5)  
    #result = overlap(line_image, raw_image)
 
    line_image2 = sld.extrapolate_lines(lines, raw_image, 
                                  positive_thresh = 0.5, negative_thresh = -0.5) 
    result = sld.overlap(line_image2, raw_image)
  
    return result


def main():

    challenge_output = 'extra.mp4'
    clip2 = VideoFileClip('videos/challenge.mp4')
    challenge_clip = clip2.fl_image(process)
    challenge_clip.write_videofile(challenge_output, audio=False)

   
main()
    
