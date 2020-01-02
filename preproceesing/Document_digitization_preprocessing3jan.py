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
#from pdf2image import convert_from_path, convert_from_bytes
#import PyPDF2
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
import constants


# # Preprocessing

# In[ ]:


def image_preprocessing(filename,file):
	#pdfdoctype=pdftype(file) 
	path=os.path.basename(filename).split('.')[0]
	image_counter=0
	inpdirectory = constants.INPUT_IMAGESPATH
	skewdirectory=constants.SKEW_IMAGESPATH
	contdirectory=constants.CONTRAST_IMAGESPATH
	cropdirectory=constants.CROP_IMAGESPATH
	try:
		os.mkdir(inpdirectory)
		os.mkdir(skewdirectory)
		os.mkdir(contdirectory)
		os.mkdir(cropdirectory)
	except OSError:
	    print ("Directories already exist")

	
	image_path=os.path.join(constants.INPUT_IMAGESPATH,path)
	imagefiles=Image.open(filename)
	imagefiles_path = image_path+ ".jpg" 
	imagefiles=imagefiles.save(imagefiles_path)
	skewout=os.path.join(constants.SKEW_IMAGESPATH, path) 
	skew_out=skewout+'_skew'+".jpg"
	skew_correction(imagefiles_path,skew_out)
	print("skew_correction done")
	imginput=Image.open(imagefiles_path)
	(width1,height1)=imginput.size
	imgskew=Image.open(skew_out)
	(width2,height2)=imgskew.size
	if height2<height1:
		contrastout=os.path.join(constants.CONTRAST_IMAGESPATH,path)
		contrast_out=contrastout+'_contrast'+ ".jpg"
		contrast(imagefiles_path,contrast_out)
		print("contrast_correction done")
		cropout=os.path.join(constants.CROP_IMAGESPATH,path)
		crop_out=cropout+'_cropped'+".jpg"
		crop_image(contrast_out,crop_out)
		print("cropping done")
		image_counter = image_counter + 1
		imgcon=Image.open(contrast_out)
		(width3,height3)=imgcon.size
		img = Image.open(crop_out)
		(width4,height4)=img.size
		if width4<(0.75*width3):
			print('contrast')
			return contrast_out
		else:

			if img.size>(1300,1300):
				img2 = img.resize((1194,1738), Image.ANTIALIAS)  #resizing image
				destout=os.path.join(constants.INPUT_IMAGESPATH,path)
				dest_out=destout+'_resized'+".jpg"
				img2.save(dest_out)
				print('resize')
				return dest_out
			else:
				print('crop')
				return crop_out
	else:
		contrastout=os.path.join(constants.CONTRAST_IMAGESPATH,path)
		contrast_out=contrastout+'_contrast'+ ".jpg"
		contrast(skew_out,contrast_out)
		print("contrast_correction done")
		cropout=os.path.join(constants.CROP_IMAGESPATH,path)
		crop_out=cropout+'_cropped'+".jpg"
		crop_image(contrast_out,crop_out)
		print("cropping done")
		image_counter = image_counter + 1
		imgcon=Image.open(contrast_out)
		(width3,height3)=imgcon.size
		img = Image.open(crop_out)
		(width4,height4)=img.size
		if width4<(0.75*width3):
			print('contrast')
			return contrast_out
		else:

			if img.size>(1300,1300):
				img2 = img.resize((1194,1738), Image.ANTIALIAS)  #resizing image
				destout=os.path.join(constants.INPUT_IMAGESPATH,path)
				dest_out=destout+'_resized'+".jpg"
				img2.save(dest_out)
				print('resize')
				return dest_out
			else:
				print('crop')
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




