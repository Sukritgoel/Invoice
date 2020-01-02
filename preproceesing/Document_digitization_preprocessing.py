#!/usr/bin/env python
# coding: utf-8

# In[17]:


# required packages are imported
import argparse
import cv2
import os
import re
import io
import json
import ftfy
import sys
from pdf2image import convert_from_path, convert_from_bytes
import PyPDF2
import re
import numpy as np
np.seterr(over='ignore')
from PIL import Image, ImageEnhance 
from preproceesing import Deskew
import math
import numpy as np
from scipy.ndimage import rotate 
from scipy import ndimage
from scipy.ndimage.filters import rank_filter
from cropping import *
from contrast import *
from pdf_type import *


# # Preprocessing

# In[ ]:


def image_preprocessing(file):
    #pdfdoctype=pdftype(file) 
    path=os.path.basename(file).split('.')[0]
    #print(path)
    pages = convert_from_path(file, 500) 
    image_counter = 1
    for page in pages: 
        image_path=os.path.join(r'C:\Users\Mehak.1\Documents\invoices\invoicedemo\Invoice_solution\input_images',path)
        imagefiles = image_path+ str(image_counter)+ ".jpg" 
        # Save the image of the page in system 
        page.save(imagefiles, 'JPEG')    
        #cv2.imwrite(skew_out, rotated) 
        skewout=os.path.join(r'C:\Users\Mehak.1\Documents\invoices\invoicedemo\Invoice_solution\deskew_output', path) 
        skew_out=skewout+'_skew'+str(image_counter)+".jpg"
        skew_correction(imagefiles,skew_out)
        print("skew_correction done")
        contrastout=os.path.join(r'C:\Users\Mehak.1\Documents\invoices\invoicedemo\Invoice_solution\contrast_output',path)
        contrast_out=contrastout+'_contrast'+str(image_counter)+ ".jpg"
        contrast(skew_out,contrast_out)
        print("contrast_correction done")
        cropout=os.path.join(r'C:\Users\Mehak.1\Documents\invoices\invoicedemo\Invoice_solution\cropping_output',path)
        crop_out=cropout+'_cropped'+str(image_counter)+".jpg"
        crop_image(contrast_out,crop_out)
        print("cropping done")
        image_counter = image_counter + 1
    return crop_out

            




def skew_correction(image,out):
    d=Deskew(
	input_file=image,
	display_image='preview the image on screen',
	output_file=out,
	r_angle=0)
    d.run()
    





  # pdf to image conversion


# In[ ]:




