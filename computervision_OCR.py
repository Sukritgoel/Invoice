#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import time
import datetime
import sys
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
import constants


def OCR_v1(filepath,imagePath):

            # COMPUTERVISION_LOCATION = os.environ.get("COMPUTERVISION_LOCATION", constants.OCR_LOCATION)

            subscription_key = constants.OCR_SUBSCRIPTION_KEY
            assert subscription_key


            client = ComputerVisionClient(
                    endpoint="https://ey-computer-vision-ocr.cognitiveservices.azure.com/",
                    credentials=CognitiveServicesCredentials(subscription_key)
            )

            with open(os.path.join(imagePath), "rb") as image_stream:
                    job = client.recognize_text_in_stream(
                            image=image_stream,
                            mode="Printed",
                            raw=True
                    )
            operation_id = job.headers['Operation-Location'].split('/')[-1]
            image_analysis = client.get_text_operation_result(operation_id)
        
            while image_analysis.status in ['NotStarted', 'Running']:
                    time.sleep(1)
                    image_analysis = client.get_text_operation_result(operation_id=operation_id)

            lines = image_analysis.recognition_result.lines
            with open(filepath, 'rb')as image_stream:
                    image_analysis1 = client.analyze_image_in_stream(
                            image=image_stream,
                            visual_features=[
                                    VisualFeatureTypes.image_type, # Could use simple str "ImageType" 
                                    VisualFeatureTypes.faces,      # Could use simple str "Faces"
                                    VisualFeatureTypes.categories, # Could use simple str "Categories"
                                    VisualFeatureTypes.color,      # Could use simple str "Color"
                                    VisualFeatureTypes.tags,       # Could use simple str "Tags"
                                    VisualFeatureTypes.description # Could use simple str "Description"
                            ]
                    )


            for tag in image_analysis1.tags:
                    if(tag.name=='text'or tag.name=='Text'):
                            textConfidence1=tag.confidence
            text = []
            for line in lines:
                    line_text = " ".join([word.text for word in line.words])
                    text.append(line_text)
            print(text)                
            return text