# !/usr/bin/env python
# coding: utf-8
import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from CommonHandler import *
import win32com.client as win32
import warnings
import sys
import pythoncom
import xlwt
import xlrd
import time
import sys
import re
import configparser
import traceback
#from script.Handler.CommonHandler import InitConfig



warnings.filterwarnings('ignore')


userid = '''Zhiqiang Zhang'''
tel = '''+86-10-8319 3844'''
mobile = '''+86-1580-131 3126'''
email = '''Zhiqiang.Zhang@sas.com'''

mailtoinner = 'CRDSSOOncall@sas.com'
#mailtoinner = 'zhiqiang.zhang@sas.com'


# mailtoouter='Owen.Hoyt@sas.com;Dave.Setzer@sas.com;Ken.Persson@sas.com;Lynne.Rowley@sas.com;ams_mi_team@wnt.sas.com;ssoappmgt@wnt.sas.com'
mailtoouter = 'Lynne.Rowley@sas.com;ETLOperationsteam@wnt.sas.com'
#mailtoouter='zhiqiang.zhang@sas.com'


mailccinner = ''
mailccouter = 'Kunzhuang.Xia@sas.com;CRDSSOOncall@sas.com;punessoams@wnt.sas.com'
#mailccouter='zhiqiang.zhang@sas.com'
logtrack = list()



def getopt():
    # print(sys.argv)
    if len(sys.argv) == 1:
        return 'inner'
    elif len(sys.argv) == 2:
        return sys.argv[1]
    else:
        return 'inner'


def logging(message):
    print(message)
    #message = str(message) + '''\n'''
    #Config = InitConfig()
    #logfile = Config.get("Default", "LogFile")
    ## print("logfile")
    #log = open(logfile, "a")
    #sys.stdout.write(message)
    #sys.stdout.flush()
    #log.write(message)
    #log.flush()
    #log.close()





def getdate():
    dt = time.time()
    dt = time.localtime(dt)
    # print(dt[0])
    return dt


def readissue(sheetflag):
    curissues = list()
    tmprow = list()
    valrow = list()
    try:
        #Config = InitConfig()
        #shiftreportpath = Config.get("Default", "shiftreportpath")
        shiftreportpath = '''\\\\huanghe\\CCD\\SSO\\AMS\\Misc\shift_report_2020.xlsx'''
        #print(shiftreportpath)
        excel = xlrd.open_workbook(shiftreportpath)
        if type(sheetflag) == type(0):
            sheet = excel.sheets()[sheetflag]
        elif type(sheetflag) == type(''):
            sheetflag = sheetflag.strip()
            sheetflag = sheetflag.upper()
            sheet = excel.sheet_by_name(sheetflag)
        else:
            print('PLEASE CHOSE RIGHT SHEET!')

            return 'ER:readissue-1'
    except Exception as e:
       raise  e

    # rows=sheet.row_values
    # rows=sheet.nrow
    # rnum=len(sheet.row_values)
    sheetnm = sheet.name
    curissues.append(sheetnm)

    if sheetnm == 'ISSUE':
        validcol = [0, 1, 2, 3, 4, 7, 8, 9]
    elif sheetnm == 'DUTY TASK':
        validcol = [0, 1, 2, 3, 4, 6, 7]
    else:
        return 'ER:readissue-3'
    tmprow = sheet.row_values(0)[0:]
    for i in validcol:
        valrow.append(tmprow[i])

    curissues.append(valrow)
    valrow = []

    # cnum=sheet.ncols
    # print("rnum="+str(rnum)+" : cnum="+str(cnum))
    rnum = sheet.nrows

    curdt = getdate()
    # for i in range(rnum-1,-1,-1)[:rnum-1]:
    for i in range(rnum - 1, 0, -1):
        try:
            tmprow = sheet.row_values(i)[0:]

            # print(i,end='')
            # print(": ", end='')
            dt = xlrd.xldate_as_tuple(tmprow[0], 0)
            # tmprow[0]=str(dt[1])+'/'+str(dt[2])+'/'+str(dt[0])
            # print(tmprow[0:6])
            if curdt[0] == dt[0] and curdt[1] == dt[1] and curdt[2] == dt[2]:
                print(curdt)
                tmprow[0] = str(dt[1]) + '/' + str(dt[2]) + '/' + str(dt[0])

                for i in validcol:
                    valrow.append(tmprow[i])

                curissues.append(valrow)
                valrow = []

            else:
                continue
        except:
            return 'ER:readissue-4'

    # print(curissues)
    return curissues


def createhtmltr(issue, trtype=0):
    if trtype == 1:
        trflagbeg = '''<th><b>'''
        trflagend = '''</b></th>'''
    elif trtype == 0:
        trflagbeg = '''<td>'''
        trflagend = '''</td>'''
    else:
        return 'ER:createhtmltr-1'

    htmlstrtr = '''<tr>'''
    for item in issue:
        htmlstrtr = htmlstrtr + trflagbeg + str(item) + trflagend
    htmlstrtr = htmlstrtr + '''</tr>'''
    return htmlstrtr


def createhtmltable(issues):
    logging("Cnt of issues/Tasks: " + str(len(issues)))
    htmlstring = '''<font size="3"><b>''' + str(issues[0]) + '''</b></font>'''
    htmlstring = htmlstring + ''' <table border="1" cellspacing="0"> '''
    htmlstring = htmlstring + createhtmltr(issues[1], 1)
    for item in issues[2:]:
        htmlstring = htmlstring + createhtmltr(item)
    htmlstring = htmlstring + '''</table>'''
    if len(issues) == 2:
        htmlstring = '''<font size="3"><b>''' + str(issues[0]) + '''</b></font> <br />None<br /><br />'''
    return htmlstring


def createhtmlbody():
    head = '''Dear All,<br /><br />Please review CRD shift wrap up report:<br /><br />'''
    issues = readissue('issue')
    if type(issues) == type('') and issues[0:3] == 'ER:':
        return issues + '|createhtmlbody-1'
    body = createhtmltable(issues)
    body = body + '''<br /><br />'''

    tasks = readissue('duty task')
    if type(tasks) == type('') and tasks[0:3] == 'ER:':
        return tasks + '|createhtmlbody-2'
    body = body + createhtmltable(tasks)
    body = body + '''<br />'''
    end = '''Regards,<br />'''
    signature = userid + '''<br />''' + '''<i>Global Hosting and US Professional Services(Beijing Office)</i><br />''' + '''Tel: ''' + tel + '''  *  ''' + '''Cell Phone: ''' + mobile + '''<br />''' + '''Email: <u><font color="blue">''' + email + '''</font></u><br />''' + '''<font size="3" face="arial" color="darkblue"><b>SAS® … THE POWER TO KNOW®</b></font><br />''' + '''<img src="C:\WorkSpace\PythonProgram\logo.png"/><br />''' + '''<font size="1" color="darkgray">This message and any attachments contain information that may be confidential and privileged. 
        Unless you are the addressee (or authorized to receive for the addressee), you may not use, copy, 
        print or disclose to anyone the message or any information contained in the message. 
        If you have received this e-mail in error, please advise the sender by reply and delete the message and any attachments. 
        Thank you.</font>'''
    signature = ''
    # htmlbody=head + body+end+signature
    htmlbody = head + body + signature  # The end is included by signature already, so remve it.

    return htmlbody


def sendmail(flag='inner'):
    print(flag)
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.GetInspector  # 这里很关键，有了这代码，下面才能获取到outlook默认签名
    # mail.BodyFormat=2  #添加这个设置后无法自动获取outlook签名

    #mail.BodyFormat = 2  # 添加这个设置后无法自动获取outlook签名
    mailcontent = createhtmlbody()

    # mail.Attachments.Add('C:\Users\xxx\Desktop\git_auto_pull_new.py')
    # print(mailcontent)


    if flag == 'outer':
        mail.To = mailtoouter
        mail.CC = mailccouter
        mail.Subject = 'CRD shift wrap up report'
    else:
        mail.To = mailtoinner
        mail.CC = mailccinner
        mail.Subject = 'CRD shift wrap up report -- inner view'
        # mail.HTMLBody = mailcontent


    bodystart = re.search("<body.*?>", mail.HTMLBody)  # 找到签名里面的body头，签名是html格式的
    mail.HTMLBody = re.sub(bodystart.group(), bodystart.group() + mailcontent, mail.HTMLBody)  # 在签名里的body头后面插入正文
    mail.Send()




