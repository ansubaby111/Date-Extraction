
###############################################################################################################
####                                            Required Packages                                          ####
###############################################################################################################
#import the libraries

import pytesseract
import cv2
import re
import datetime
import glob
import pandas as pd
import sys
import os

################################################################################################################
####                                    Date Extract Part                                                   ####
################################################################################################################

def Date_Extract(img_path,pytes_path):
    # Path of working folder
    img_path_jpeg = os.path.join(img_path,'*.jpeg')
    
    # Path of pytesseract
    pytess_path = os.path.join(pytes_path)
    pytesseract.pytesseract.tesseract_cmd = pytess_path
    
    # import multiple images
    filelist = glob.glob(img_path_jpeg)
    
    for i in  range(len(filelist)):  
        # Read image with opencv
        img= cv2.imread(filelist[i],0)
        
        # resize the image 
        img_s = cv2.resize(img, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_LINEAR) 
        
        # Recognize text with tesseract for python
        text = pytesseract.image_to_string(img_s, lang='eng')
        text = text.lower()
        
        # Recognize Date with regular expression with different format
        Expense_date1 = re.findall("\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}-\d{1,2}-\d{2,4}|\d{4}-\d{1,2}-\d{1,2}|[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}\.[\d]{1,2}\’[\d]{2,4}|[\d]{1,2}-[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}-[\d]{2,4}|[\d]{1,2}/[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}/[\d]{2,4}|[\d]{1,2}[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}\"[\d]{2,4}|[\d]{1,2} [jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}\’[\d]{2,4}",text)   
       
        if len(Expense_date1)>=1:
            if len(Expense_date1)>=2:
                Expense_date1 = Expense_date1[0]
            Expense_date1= Expense_date1    
            Expense_date2 = ''.join(Expense_date1)    
            Expense_date3 = re.sub('[^A-Za-z0-9-/.]+', ' ', Expense_date2)
            Expense_date4 = pd.to_datetime(Expense_date3,errors='coerce')
            if pd.isnull(Expense_date4)==True:
               Expense_date = "null"
            else:
                Expense_date = Expense_date4.strftime('%Y-%m-%d')
            Expense_date = dict(date=Expense_date)
        else:
            Expense_date = dict(date='null')
        Expense_date = Expense_date
        print(Expense_date)
    return Expense_date

Date_Extract(img_path,pytes_path)

##############################################################################################################
####                                      END                                                             ####
##############################################################################################################       

