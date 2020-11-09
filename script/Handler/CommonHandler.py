import os
basedir=os.path.dirname(os.path.abspath(__file__))+'\\..\\..\\'
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"
controler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Controler"
database_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Database"
datamart_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\..\\datamart"
static_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\..\\static"
conf_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\..\\conf"
log_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\..\\logs"

import sys
sys.path.append(basedir)
sys.path.append(handler_path)
sys.path.append(controler_path)
sys.path.append(database_path)

from database import *
import configparser
import requests
import base64

import xml.sax as sax
import pandas as pd
from io import BytesIO

###################
import win32com.client as wincom
import warnings
#import sys
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
#import os

import pandas as pd
from io import BytesIO
from datetime import date
pd.options.display.max_columns = 30
#


warnings.filterwarnings('ignore')











class JiraFilterHandler(sax.ContentHandler):

    def __init__(self):
        pass
        self.currentTag = ""
        self.currentAttr = ''
        self.currentData = ""
        self.tickets = []
        self.issueishere = "no"

    def startElement(self, tag, attributes):  # attributes 是一个字典。
        self.currentTag = tag

        for k in attributes.keys():
            self.currentAttr = str(k) + ":" + str(attributes[k])
        if tag=="tr":
            if "class" in attributes.keys():
                if attributes["class"]=="issuerow":
                    ticket={}
                    self.tickets.append(ticket)
                    self.issueishere = "yes"
                else:
                    self.issueishere="no"

        if tag=="td":
            if "class" in attributes.keys():
                if self.issueishere=="yes":
                    if attributes["class"]=="issuekey":
                        self.currentAttr="key"
                    elif attributes["class"]=="summary":
                        self.currentAttr="summary"




    def endElement(self, tag):
        self.currentTag=""
        if tag == "tr":
            self.issueishere="no"
        if tag=="td":
            self.curissueattr=""

    def characters9(self, content):  # 简单来说这个事件在每次遇到标签时触发，不管是开始标签还是结束标签。标签之间的字符串都是content
        if self.currentTag=="td":
            self.tickets[-1][self.currentAttr]=content






ConfigFile = conf_path+"\\Deployment.cfg"
Config = configparser.ConfigParser()
Config.read(ConfigFile, encoding="utf-8")

def logging(message):
    message=str(message)+'''\n'''
    logfile=log_path+"\\SEM.log"
    log=open(logfile,"a")
    sys.stdout.write(message)
    sys.stdout.flush()
    log.write(message)
    log.flush()
    log.close()

def password_decryption(encrypted):
    return base64.b64decode(encrypted).decode()


# This function will be decommision
def InitConfig_compliance():
    ConfigObj = configparser.ConfigParser()
    ConfigFile = "C:\\WorkSpace\\PythonProgram\\Deployment\\Deployment.cfg"
    ConfigObj.read(ConfigFile, encoding="utf-8")
    return ConfigObj

# This function will be decommision
def InitConfig_swapshift():
    ConfigObj = configparser.ConfigParser()
    ConfigFile = sys.path[0] + "\Deployment.cfg"
    ConfigFile = "C:\WorkSpace\PythonProgram\Deployment\Deployment.cfg"
    ConfigObj.read(ConfigFile, encoding="utf-8")
    return ConfigObj

# This function will be decommision
def InitConfig():
    ConfigObj = configparser.ConfigParser()
    ConfigFile = "C:\\WorkSpace\\PythonProgram\\Deployment\\Deployment.cfg"
    ConfigObj.read(ConfigFile, encoding="utf-8")
    return ConfigObj



def GetTlaList():
    tlas=[]
    TlaList=Tla.query.order_by(Tla.tla).all()
    for tla in TlaList:
        tlas.append(tla.tla.upper())
    return tlas


###JIRA System has been upgraded, so the form of the request is changed

def GetJiraTickets(JiraFilterURL):
    jira_tickets = []
    # Config=InitConfig2()
    TicketFilterURL = Config.get("Authentication", JiraFilterURL)
    print("Compliacnce Handler", TicketFilterURL)
    UserName = Config.get("Authentication", "UserName")
    PassWord = Config.get("Authentication", "PassWord")
    Auth = base64.b64encode((UserName + ":" + PassWord).encode('utf8'))
    Auth = Auth.decode('utf8')

    Header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": 'Basic {}'.format(Auth),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }

    response = requests.request(
        "POST",
        TicketFilterURL,
        data=None,
        headers=Header
    )

    tempfile = open("C:\\WorkSpace\\PythonProgram\\pycharm\\SEM\\logs\\jirafilter.html", "w")
    print(response.text, file=tempfile, flush=True)
    tempfile.close()

    issuetablebeg = '''<issuetable-web-component data-content="issues">'''
    issuetablebeg = '''<issuetable-web-component'''
    issuetablebeg_len = len(issuetablebeg)
    issuetableend = '''</issuetable-web-component>'''
    issuetablebeg_position = response.text.find(issuetablebeg)
    issuetableend_position = response.text.find(issuetableend)
    print("beg", issuetablebeg_position, "end", issuetableend_position)

    issuetablexml = response.text[issuetablebeg_position + issuetablebeg_len: issuetableend_position]
    issuetablexml = issuetablexml.replace('''\n''','')
    # xmlparser = sax.make_parser()
    # xmlparser.setFeature(sax.handler.feature_namespaces, 0)  # turn off namepsaces
    #Handler = JiraFilterHandler()
    # xmlparser.setContentHandler(Handler)
    # xmlparser.parse(xmlfilepath)
    #sax.parseString(issuetablexml, Handler)

    issuelist = issuetablexml
    jira_tickets=[]
    i=0
    j=0
    k=0
    while True:
        issuebeg="<tr"
        issuebeg2='>'
        issueend='''</tr>'''
        issueattr="issuerow"
        issuebeg_position=issuelist.find(issuebeg)
        issuebeg2_position=issuelist.find(issuebeg2)
        issueend_position=issuelist.find(issueend)

        if issuebeg_position>=0 and issuebeg2_position>=0 and issueend_position>=0:
            curissuehead = issuelist[issuebeg_position:issuebeg2_position+1]
            #print("curissuehead:",curissuehead)
            if curissuehead.find("issuerow") >=0:
                curissue = issuelist[issuebeg2_position + 1:issueend_position]
                curissue=curissue.strip()
                #print("curissue:", curissue)
                jiraticket = {}

                while True:
                    colbeg = '''<td'''
                    colbeg2 = '''>'''
                    colend = '''</td>'''
                    colbeg_position = curissue.find(colbeg)
                    colbeg2_position = curissue.find(colbeg2)
                    colend_position = curissue.find(colend)

                    if colbeg_position >= 0 and colbeg2_position >= 0 and colend_position>=0:
                        curcolhead = curissue[colbeg_position:colbeg2_position + 1]
                        if curcolhead.find("issuekey") >= 0 or curcolhead.find("summary") >= 0:
                            curcol = curissue[colbeg2_position + 1:colend_position]
                            while True:
                                tagbeg = '''<'''
                                tagend = '''>'''
                                tagbeg_position = curcol.find(tagbeg)
                                tagend_position = curcol.find(tagend)
                                if tagbeg_position >= 0 and tagend_position >= 0:
                                    curcol = curcol[0:tagbeg_position] + curcol[tagend_position + 1:]

                                    continue #next tag
                                else:
                                    break
                            curcol=curcol.strip()
                            if curcolhead.find("issuekey") >= 0:
                                jiraticket["issuekey"] = curcol
                                print("issuekey:", curcol)
                            if curcolhead.find("summary") >= 0:
                                jiraticket["summary"] = curcol
                                print("summary:", curcol)

                            curissue = curissue[colend_position + len(colend):]
                            #print("curissue:", curissue)
                            continue #next td
                        else:#next td
                            curissue = curissue[colend_position + len(colend):]
                            #print("curissue3:", curissue)
                            continue
                    else:#cur tr out
                        break


                jira_tickets.append(jiraticket)
                #print(jiraticket)
                issuelist = issuelist[issueend_position + len(issueend):]
                continue
            else:#next tr
                issuelist=issuelist[issueend_position+len(issueend):]
                continue
        else: #done
            break

    return jira_tickets

# >>>2019-10-21 9:23
def GetServiceNowTickets(SNfilterURL):
    servicenow_tickes = []
    # Config=InitConfig2()
    session = requests.session()
    # session.auth = ('ghusps_qaops_api', password_decryption('R280dGhzYXM='))
    SNUserName = Config.get("ServiceNow", "snusername")
    SNPassWord = Config.get("ServiceNow", "snpassword")
    SNPassWord = password_decryption(SNPassWord)
    CRDSNTicketsURL = Config.get("ServiceNow", SNfilterURL)

    session.auth = (SNUserName, SNPassWord)
    first_response = session.get(CRDSNTicketsURL)
    first_response.raise_for_status()

    # Checking the return result before processing
    if first_response.status_code != 200:
        print('ERROR: Status is', first_response.status_code, "The request is failed")
        exit()
    elif first_response.content.__str__() == "b''":
        print('ERROR: Status is', first_response.status_code, "GRC issues request is succeed, but has no content")
        exit()

    rpt_excel = pd.read_excel(BytesIO(first_response.content))

    for row in rpt_excel.iterrows():
        servicenow_ticke = ''
        for col in row:
            # snticketshtml=snticketshtml + '''['''+str(row[1][0])+''']&nbsp;&nbsp;'''+str(row[1][1])+'''&nbsp;&nbsp;('''+str(row[1][3])+''')<br/>'''
            servicenow_ticke += str(col) + '''  |  '''
        servicenow_tickes.append(servicenow_ticke)

    return servicenow_tickes

################################
###    outlook accessing
###############################
def get_mail_folder(target_name):
    pythoncom.CoInitialize()
    outlook = wincom.Dispatch("Outlook.Application").GetNamespace("MAPI")
    accounts = wincom.Dispatch("Outlook.Application").Session.Accounts;
    for account in accounts:
        global inbox
        mailbox = outlook.Folders(account.DeliveryStore.DisplayName)
        # print("****Account Name**********************************")
        # print(account.DisplayName)
        # print("***************************************************")
        folders = mailbox.Folders
        for folder in folders:
            if folder.name != "Inbox":
                continue
            return recursive_mailbox(target_name, folder)


def recursive_mailbox(target_name, folder):
    # print("query:",parent_name+"->"+folder.name)
    target_folder = None
    if folder.name == target_name:
        return folder
    else:
        for sub_folder in folder.folders:
            # print("structure:" sub_folder.name)
            target_folder = recursive_mailbox(target_name, sub_folder)
            if target_folder != None:
                return target_folder
    return target_folder


def save_all_attachment(mail_folder_name,tgt_path=static_path+"\\temp"):
    mail_folder=get_mail_folder(mail_folder_name)
    messages = mail_folder.Items
    save_path=tgt_path
    for message in messages:
        print(message.subject)
        # print(message.body)
        if (hasattr(message, 'Attachments')):
            for atta in message.Attachments:
                atta.SaveASFile(os.path.join(save_path, atta.FileName))

def save_attachment_by_id(mail_folder_name,mail_id,tgt_path=static_path+"\\temp"):
    mail_folder=get_mail_folder(mail_folder_name)
    messages = mail_folder.Items
    save_path = tgt_path
    saved_file_list=[]
    for message in messages:
        #print(message.subject)
        # print(message.body)

        if message.EntryID==mail_id:
            print("message:", message.EntryID)
            if hasattr(message, 'Attachments'):
                print("attachment:",str(message.Attachments))
                for atta in message.Attachments:
                    atta.SaveASFile(os.path.join(save_path, atta.FileName))
                    saved_file_list.append(atta.FileName)
    return saved_file_list

def get_maillist(mail_folder_name):
    mail_folder=get_mail_folder(mail_folder_name)
    messages = mail_folder.Items
    maillist=[]
    for message in messages:
        #print(message.subject)
        # print(message.body)
        if (hasattr(message, 'EntryID')):
            mail={"EntryID":message.EntryID,"ReceivedTime":message.ReceivedTime,"Subject":message.Subject,"Body":message.Body,"Attachments":message.Attachments}
            maillist.append(mail)
    return maillist
