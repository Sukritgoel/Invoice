import os
import cv2
from PIL import Image, ImageEnhance 
import numpy as np

def contrast(filename,output):
    path=os.path.basename(filename).split('.')[0]
    img = cv2.imread(filename) 
    im=Image.open(filename)
    Y = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)[:,:,0]
    min = np.min(Y)
    max = np.max(Y)
    contrast = (max-min)/(max+min)
    print(contrast)
    if contrast<5:
        enhancer = ImageEnhance.Contrast(im)
        enhanced_im = enhancer.enhance(1.48)       
        #new_file = 'processed_' +path + ".jpg"        
        enhanced_im.save(output)
    else:
        enhancer=ImgaeEnhancer.Contrast(im)
        enhanced_im=enhancer.enhance(0.0)
        enhanced_im.save(output)