
import win32com.client as win32
import warnings
import sys
import pythoncom
import xlwt
import xlrd
import time
import urllib
import sys
import requests
import json
import base64
import traceback
import configparser

#>>>
import pandas as pd
from io import BytesIO
from datetime import date
pd.options.display.max_columns = 30
#


warnings.filterwarnings('ignore')




from script.Database.database import *
#from time import time,localtime
from script.Log.log import logging,log_stub,add_log_at_begin_and_end

log=logging

def receive_crontab():
    
    pythoncom.CoInitialize()    
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    accounts= win32com.client.Dispatch("Outlook.Application").Session.Accounts;
    for account in accounts:
        global inbox
        inbox = outlook.Folders(account.DeliveryStore.DisplayName)
        print("****Account Name**********************************",file=f)
        print(account.DisplayName,file=f)
        print(account.DisplayName)
        print("***************************************************",file=f)
        folders = inbox.Folders
            for folder in folders:
                print("****Folder Name**********************************", file=f)
                print(folder, file=f)
                print("*************************************************", file=f)
                emailleri_al(folder)
                a = len(folder.folders)
                if a>0 :
                        global z
                        z = outlook.Folders(account.DeliveryStore.DisplayName).Folders(folder.name)
                        x = z.Folders
                        for y in x:
                        emailleri_al(y)
                        print("****Folder Name**********************************", file=f)
                        print("..."+y.name,file=f)
                        print("*************************************************", file=f)
                        print("Finished Succesfully")
    
def emailleri_al(folder):
    messages = folder.Items
    a=len(messages)
    if a>0:
        for message2 in messages:
            try:
                sender = message2.SenderEmailAddress
                if sender != "":
                    print(sender, file=f)
            except:
                print("Error")
                print(account.DeliveryStore.DisplayName)
                pass
            try:
                message2.Save
                message2.Close(0)
            except:
                pass    