import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from CommonHandler import *

import requests
import base64
import win32com.client as win32
import xlrd
import time
import sys
import jira
import configparser
import traceback
from script.Handler.CommonHandler import InitConfig







def GetReportTimeFlag():
    hour = time.localtime()[3]
    if hour // 12 == 1:
        return str(hour % 12) + 'PM'
    else:
        if hour == 0:
            hour = 12
        return str(hour) + 'AM'



def GetJiraConnect():
    # JiraURL = 'https://www.ondemand.sas.com/jira'
    JiraURL = Config.get("Authentication", "JiraURL")
    UserName = Config.get("Authentication", "UserName")
    PassWord = Config.get("Authentication", "PassWord")
    try:
        JiraConn = jira.JIRA(JiraURL, basic_auth=(UserName, PassWord))
        return JiraConn
    except Exception:
        print("Failed to connect to JIRA.")
        sys.exit()




def GetTicketKeyLst_old():
    TicketKeyLst = []
    # DMTicketFilterURL = "https://www.ondemand.sas.com/jira/issues/?filter=23310"
    DMTicketFilterURL = Config.get("Authentication", "DMTicketFilterURL")
    UserName = Config.get("Authentication", "UserName")
    PassWord = Config.get("Authentication", "PassWord")
    # Auth=base64.b64encode(b'scnzqz:Oracle-3i')
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
        DMTicketFilterURL,
        data=None,
        headers=Header
    )

    # print(response.status_code)
    # print(auth)
    # print(response.text.find('ACS-1425'))
    flagbeg = '<span class="issue-link-key">'
    flagend = '</span><br/><span class="issue-link-summary">'
    flagbeg_len = len(flagbeg)
    flagend_len = len(flagend)
    dmbeg = response.text.find(flagbeg)
    while dmbeg > -1:
        dmend = response.text.find(flagend, dmbeg)
        issue = response.text[dmbeg + flagbeg_len:dmend]
        TicketKeyLst.append(issue.strip())
        dmbeg = dmend + flagend_len
        dmbeg = response.text.find(flagbeg, dmbeg)
    return TicketKeyLst


def GetTicketKeyLst(Config):
    TicketKeyDic = Config["ActiveDMTickets"]
    TicketKeyLst = list(TicketKeyDic.values())
    return TicketKeyLst



def AddComment(JiraTicketKey, Comment, visibility=None, is_internal=False):
    print('''[AddComment]'''+JiraTicketKey +":"+Comment)
    JiraConn=GetJiraConnect()
    if JiraTicketKey and Comment:
        JiraConn.add_comment(JiraTicketKey, Comment, visibility=None, is_internal=False)

