
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
import urllib
import sys
import requests
import json
import base64
import traceback
#import configparser

#>>>
#import pandas as pd
from io import BytesIO
from datetime import date
pd.options.display.max_columns = 30
#


warnings.filterwarnings('ignore')




from script.Database.database import *
#from time import time,localtime
from script.Log.log import logging,log_stub,add_log_at_begin_and_end

log=logging

#basedir=os.path.dirname(os.path.abspath(__file__))
#basedir="C:\\WorkSpace\\PythonProgram\\pycharm\\SEM\\"




class MyEncoder2(json.JSONEncoder):
 
    def default(self, obj):
        if isinstance(obj, EnvUIData2):
            return { "tla":obj.tla,"deployment_type":obj.deployment_type,"status":obj.status,"comment":obj.comment,"duty_rank":obj.duty_rank,"monitored_by":obj.monitored_by }
        return json.JSONEncoder.default(self, obj)
            
class EnvUIData2():
    tla="tla"
    deployment_type="deployment_type"
    status="status" 
    comment="comment"
    owner="owner"
    duty_rank="rank"
    monitored_by="monitored_by"
    def __init_(self,tla="",deployment_type="",status="",comment="",owner="",duty_rank="",monitored_by=""):
        self.tla=tla
        self.deployment_type=deployment_type
        self.status=status 
        self.comment=comment
        self.owner=owner
        self.duty_rank=duty_rank
        self.monitored_by=monitored_by
    
    def __repr__(self):
        return f" tla:{self.tla},deployment_type:{self.deployment_type},status:{self.status},comment:{self.comment},duty_rank: {self.duty_rank},monitored_by:{self.monitored_by}"
  
def query_environments2():
    report=Environment.query.all()
    return report
    
def create_compliance_report_instance2():
    return ComplianceReport()

def create_envrionment_instance2(tla="",deployment_type="",server_type="",server_machine="",terminal_machine="",comment="",monitored_by="",enabled="",key_words="",is_compliance=""):
    return Environment(tla=tla,deployment_type=deployment_type,server_type=server_type,server_machine=server_machine,terminal_machine=terminal_machine,comment=comment,monitored_by=monitored_by,enabled=enabled,key_words=key_words,is_compliance=is_compliance)
   


# create_compliance_report_template##################################
def InitConfig_compliance():
    ConfigObj = configparser.ConfigParser()
    ConfigFile = "C:\\WorkSpace\\PythonProgram\\Deployment\\Deployment.cfg"
    ConfigObj.read(ConfigFile, encoding="utf-8")
    return ConfigObj




def GetReportTimeFlag():
    hour = time.localtime()[3]
    if hour // 12 == 1:
        return str(hour % 12) + 'PM'
    else:
        if hour == 0:
            hour = 12
        return str(hour) + 'AM'


def GetJiraTickets_nouse():
    jira_tickets = []
    #Config = InitConfig()
    TicketFilterURL = Config.get("Authentication", "AMSTicketFilterURL")
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

    # print(response.status_code)
    # print(auth)
    # print(response.text.find('ACS-1425'))
    keybegflag = '<span class="issue-link-key">'
    keyendflag = '</span><br/><span class="issue-link-summary">'
    keybegflag_len = len(keybegflag)
    keyendflag_len = len(keyendflag)

    sumbegflag = '</span><br/><span class="issue-link-summary">'
    sumendflag = '</span></a></li>'
    sumbegflag_len = len(sumbegflag)
    sumendflag_len = len(sumendflag)
    keybeg = response.text.find(keybegflag)
    i = 1
    while keybeg > -1:
        keyend = response.text.find(keyendflag, keybeg)
        issuekey = response.text[keybeg + keybegflag_len:keyend]
        sumbeg = response.text.find(sumbegflag, keyend)
        sumend = response.text.find(sumendflag, sumbeg)
        issuesum = response.text[sumbeg + sumbegflag_len:sumend]
        # print(issuekey + ':'+issuesum)
        jira_tickets.append(f'{issuekey}:   {issuesum}')

        i = i + 1
        keybeg = keyend + keyendflag_len
        keybeg = response.text.find(keybegflag, keybeg)

    return jira_tickets


# >>>2019-10-21 9:23
def GetServiceNowTickets_nouse():
    servicenow_tickes = []
    #Config = InitConfig()
    session = requests.session()
    # session.auth = ('ghusps_qaops_api', password_decryption('R280dGhzYXM='))
    SNUserName = Config.get("ServiceNow", "snusername")
    SNPassWord = Config.get("ServiceNow", "snpassword")
    SNPassWord = password_decryption(SNPassWord)
    CRDSNTicketsURL = Config.get("ServiceNow", "CRDSNTicketsURL")

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


    
def add_compliance_report2(compliance_report):
    ComplianceReport.query.add(compliance_report)
    ComplianceReport.query.commit()
    
def create_compliance_report_template2():
    pass

def create_compliacne_report_view_template2():
    f = open(basedir + 'templates\\compliance_report_view_frame.html', 'r')
    compliance_report_frame = f.read()
    f.close()
    tla_status_stub_begin = compliance_report_frame.index("[%")
    # print(f'stubbeg:{tla_status_stub_begin}')
    tla_status_stub_end = compliance_report_frame.index("%]")
    # print(f"stubend:{tla_status_stub_end}")
    tla_status_stub = compliance_report_frame[tla_status_stub_begin:tla_status_stub_end + 2]
    # print("status-stub")
    # print(tla_status_stub)
    tla_status = CreateTableHtml()
    # print("tla_status")
    # print(tla_status)
    compliance_report = compliance_report_frame.replace(tla_status_stub, tla_status)
    html_file = open(basedir + 'templates\\compliance_report_view_template.html', 'w')
    print(compliance_report, file=html_file, flush=True)
    html_file.close()

#create_compliance_report_template##################################    

#def InitConfig2():
#    ConfigObj=configparser.ConfigParser()
#    ConfigFile="C:\\WorkSpace\\PythonProgram\\Deployment\\Deployment.cfg"
#    ConfigObj.read(ConfigFile,encoding="utf-8")
#    return ConfigObj
    

def GetReportTimeFlag2():
    hour=time.localtime()[3]
    if hour//12 == 1:
        return str(hour%12)+'PM'
    else:
        if hour==0:    
            hour=12
        return str(hour)+'AM'
   
def GetJiraTickets2_old(JiraFilterURL):
    jira_tickets=[]
    #Config=InitConfig2()
    TicketFilterURL = Config.get("Authentication",JiraFilterURL)
    print("Compliacnce Handler",TicketFilterURL)
    UserName = Config.get("Authentication","UserName")
    PassWord = Config.get("Authentication","PassWord")
    Auth =base64.b64encode((UserName+":"+PassWord).encode('utf8'))
    Auth=Auth.decode('utf8')

    Header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": 'Basic {}'.format(Auth),
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }

    response = requests.request(
       "POST",
       TicketFilterURL,
        data=None,
       headers=Header
    )

    tempfile=open("C:\\WorkSpace\\PythonProgram\\pycharm\\SEM\\logs\\jirafilter.html","w")
    print(response.text,file=tempfile,flush=True)
    tempfile.close()
#print(auth)
#print(response.text.find('ACS-1425'))
    keybegflag='<span class="issue-link-key">'
    keyendflag='</span><br/><span class="issue-link-summary">'
    keybegflag_len=len(keybegflag)
    keyendflag_len=len(keyendflag)

    sumbegflag='</span><br/><span class="issue-link-summary">'
    sumendflag='</span></a></li>'
    sumbegflag_len=len(sumbegflag)
    sumendflag_len=len(sumendflag)
    keybeg=response.text.find(keybegflag)
    i = 1
    while keybeg>-1:
        keyend=response.text.find(keyendflag,keybeg)
        issuekey=response.text[keybeg+keybegflag_len:keyend]
        sumbeg=response.text.find(sumbegflag,keyend)
        sumend=response.text.find(sumendflag,sumbeg)
        issuesum=response.text[sumbeg+sumbegflag_len:sumend]
        #print(issuekey + ':'+issuesum)
        jira_tickets.append(f'{issuekey}:   {issuesum}')
        
        i = i + 1
        keybeg=keyend+keyendflag_len
        keybeg=response.text.find(keybegflag,keybeg)  
    
    
    return jira_tickets


###JIRA System has been upgraded, so the form of the request is changed

def GetJiraTickets2_rm2comm(JiraFilterURL):
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

    issuetablebeg='''<issuetable-web-component data-content="issues">'''
    issuetablebeg_len=len(issuetablebeg)
    issuetableend='''</issuetable-web-component>'''
    issuetablebeg_position=response.text.find(issuetablebeg)
    issuetableend_position=response.text.find(issuetableend)
    print("beg",issuetablebeg_position,"end",issuetableend_position)

    issuetablexml=response.text[issuetablebeg_position + issuetablebeg_len,issuetableend_position]



    #xmlparser = sax.make_parser()
    #xmlparser.setFeature(sax.handler.feature_namespaces, 0)  # turn off namepsaces
    Handler = JiraFilterHandler()
    #xmlparser.setContentHandler(Handler)
    #xmlparser.parse(xmlfilepath)
    sax.parseString(issuetablexml,Handler)
    return Handler.tickets



#>>>2019-10-21 9:23
def GetServiceNowTickets2_rm2comm(SNfilterURL):
    servicenow_tickes=[]
    #Config=InitConfig2()
    session = requests.session()
    #session.auth = ('ghusps_qaops_api', password_decryption('R280dGhzYXM='))
    SNUserName = Config.get("ServiceNow","snusername")
    SNPassWord = Config.get("ServiceNow","snpassword")
    SNPassWord=password_decryption(SNPassWord)    
    CRDSNTicketsURL=Config.get("ServiceNow",SNfilterURL)
    
    session.auth = (SNUserName,SNPassWord)
    first_response = session.get(CRDSNTicketsURL)
    first_response.raise_for_status()

    # Checking the return result before processing
    if first_response.status_code != 200:
        print('ERROR: Status is', first_response.status_code, "The request is failed")
        exit()
    elif first_response.content.__str__() == "b''":
        print('ERROR: Status is', first_response.status_code, "GRC issues request is succeed, but has no content")
        exit()

    rpt_excel= pd.read_excel(BytesIO(first_response.content))
    
    
    for row in rpt_excel.iterrows():
        servicenow_ticke=''
        for col in row:
            #snticketshtml=snticketshtml + '''['''+str(row[1][0])+''']&nbsp;&nbsp;'''+str(row[1][1])+'''&nbsp;&nbsp;('''+str(row[1][3])+''')<br/>'''
            servicenow_ticke+=str(col)+'''  |  '''
        servicenow_tickes.append(servicenow_ticke)
    
    return servicenow_tickes
    



def CreateTableHtml():
    trlist = CreateTrList()
    tablehtml = ''' <table border="1" cellspacing="0" cellpadding="0"> '''
    for i in range(len(trlist)):
        if i == 0:
            tablehtml += '''\n <tr><b>'''
        else:
            tablehtml += '''\n <tr>'''
        for td in trlist[i]:
            tablehtml += str(td)
        if i == 0:
            tablehtml += '''</b></tr>\n'''
        else:
            tablehtml += '''</tr>\n'''
    tablehtml += '''</table>'''
    # print(tablehtml)
    return tablehtml


def CreateTrList():
    trlist = list()
    rowspan = 1
    excelrows = ReadExcelRows2()
    # print(len(issues))
    for currow in excelrows:
        trlist.append(CreateTdList(currow))
    colnum = len(trlist[0])
    rownum = len(trlist)
    for i in range(2):
        rowspan = 1
        # spantr=trlist[0]
        for j in range(rownum):
            if j == 0:
                spantr = trlist[j]
            if str(trlist[j][i]).strip() != '':
                spantr[i] = spantr[i].replace('''rowspan="1"''', '''rowspan="''' + str(rowspan) + '''"''')
                spantr = trlist[j]
                rowspan = 1
            else:
                rowspan += 1
    # print(trlist)
    return trlist


def ReadExcelRows():
    excelrows = list()
    try:
        TemplateExcel = xlrd.open_workbook(basedir + 'templates\\ComplianceReportForm.xlsm')
        sheet = TemplateExcel.sheet_by_name("TLASchedules")
    except Exception as err:
        return err

    rnum = sheet.nrows
    for i in range(2, rnum):
        tmprow = sheet.row_values(i)[0:6]
        excelrows.append(tmprow)

    return excelrows


def CreateTdList(excelrow):
    tdlist = list()

    # print(range(len(excelrow)))
    for i in range(len(excelrow)):
        # print(i)
        # print(excelrow[i])
        column_value = str(excelrow[i]).strip()
        column_value=column_value.replace("{{","{{form.").replace("_principal","").replace("_assistant","")
        if column_value == '' and (i == 0 or i == 1):
            tdflagbeg = ''
            tdflagend = ''
        else:
            if '}' in column_value and 'status' in column_value:
                status = column_value.replace('''{{''', '')
                status = status.replace('''}}''', '')
                tdflagbeg = '''\n <td rowspan="1" {% if ''' + status + ''' =="Running" %} color="lime"  {% elif ''' + status + '''=="Error" %} color="red" {% endif %} >'''
                # print(tdflagbeg)
            else:
                tdflagbeg = '''<td rowspan="1" >'''

            tdflagend = '''</td>\n'''

        tdlist.append(tdflagbeg + column_value + tdflagend)

    return tdlist




def CreateTableHtml2():
    trlist=CreateTrList2()
    tablehtml=''' <table border="1" cellspacing="0" cellpadding="0" margin="15"> '''
    for i in range(len(trlist)):
        if i == 0:
            tablehtml+='''\n <tr><b>'''
        else:
            tablehtml+='''\n <tr>'''
        for td in trlist[i]:
            tablehtml+=str(td)
        if i==0:
            tablehtml+='''</b></tr>\n'''
        else:
            tablehtml+='''</tr>\n'''
    tablehtml+= '''</table>'''
    #print(tablehtml)
    return tablehtml    
    
def CreateTrList2():
    trlist=list()
    rowspan=1
    excelrows=ReadExcelRows2()
    #print(len(issues))
    for currow in excelrows:
        trlist.append(CreateTdList2(currow))
    colnum=len(trlist[0])
    rownum=len(trlist)
    for i in range(2):
        rowspan=1
        #spantr=trlist[0]
        for j in range(rownum):
            if j==0:
                spantr=trlist[j]
            if str(trlist[j][i]).strip() != '':
                spantr[i]=spantr[i].replace('''rowspan="1"''','''rowspan="'''+str(rowspan)+'''"''')
                spantr=trlist[j]
                rowspan=1
            else:
                rowspan +=1
    #print(trlist)
    return trlist

def ReadExcelRows2():

    excelrows=list()
    try:
        TemplateExcel=xlrd.open_workbook(basedir+'templates\\ComplianceReportForm.xlsm')
        sheet=TemplateExcel.sheet_by_name("TLASchedules")
    except Exception as err:
        return err

    rnum=sheet.nrows 
    for i in range(2,rnum):
        tmprow=sheet.row_values(i)[0:6]
        excelrows.append(tmprow)  
        
    return excelrows
    


def CreateTdList2(excelrow):
    tdlist = list()

    # print(range(len(excelrow)))
    for i in range(len(excelrow)):
        # print(i)
        # print(excelrow[i])
        column_value = str(excelrow[i]).strip()

        if column_value == '' and (i == 0 or i == 1):
            tdflagbeg = ''
            tdflagend = ''
        else:
            tdflagbeg = '''<td rowspan="1" >'''
            tdflagend = '''</td>\n'''


        if '}' in column_value:
            input_field_name=column_value.replace('''{{''','')
            input_field_name=input_field_name.replace('''}}''','')
            tla = input_field_name.split("_")[0]
            deployment_type=input_field_name.split("_")[1]
            tla_key=tla+"_"+deployment_type
            input_field_name="\""+input_field_name+"\""


            is_running_selected="""{% if tlas[[#tla_key#]].status == 'Running' %} selected='selected' {% elif tlas[[#tla_key#]].status == 'status' and tlas[[#tla_key#]].tla in ['AMV', 'CHO', 'ANFSO']  %} selected='selected' {% endif %}"""
            is_done_selected = """{% if tlas[[#tla_key#]].status == 'Done' %} selected='selected' {% elif tlas[[#tla_key#]].status == 'status' and tlas[[#tla_key#]].tla in ['ASK', 'ASM', 'ASU', 'ASV', 'AMM', 'AMU']  %} selected='selected' {% endif %}"""
            is_error_selected = """{% if tlas[[#tla_key#]].status == 'Error' %} selected='selected' {% endif %}"""
            is_notstarted_selected = """{% if tlas[[#tla_key#]].status == 'Not Started' %} selected='selected' {% elif tlas[[#tla_key#]].status == 'status' and tlas[[#tla_key#]].tla in ['ACS', 'AMK', 'BLS', 'CSP']  %} selected='selected' {%endif %}"""
            is_noactivity_selected = """{% if tlas[[#tla_key#]].status == 'No Activity' %} selected='selected' {% endif %}"""
            is_noerror_selected =  """{% if tlas[[#tla_key#]].status == 'No Error' %} selected='selected' {% elif tlas[[#tla_key#]].status == 'status' and tlas[[#tla_key#]].tla in ['BMI', 'ESR', 'WBR', 'WCA', 'WCL', 'WIA', 'WIN', 'WMX', 'WPN', 'WUK', 'WZA', 'NCF', 'NCJ', 'CMA', 'TPB', 'LLY', 'CSE', 'MCD', 'STR', 'UNV', 'UMS', 'HIL', 'HRS', 'DIG']  %} selected='selected' {% endif %}"""

            #print([tla,is_running_selected,is_noerror_selected,is_done_selected,is_notstarted_selected,is_error_selected,is_noactivity_selected])


            if 'status' in column_value:
                column_value=''' <select class="tla_stats" name=[#status#] style="background-color: #e3f2fd;" onChange="this.style.backgroundColor=this.options[this.selectedIndex].style.color">
<option value="Running" style=" color: green;background-color: yellow;" [#is_running_selected#]>Running</option>
<option value="Done" style="background-color: yellow;" [#is_done_selected#] >Done</option>
<option value="Error" style="color: red;background-color: yellow;" [#is_error_selected#] >Error</option>
<option value="No Activity" style="background-color: yellow;" [#is_noactivity_selected#]>No Activity</option>
<option value="Not Started" style="background-color: yellow;" [#is_notstarted_selected#] >Not Started</option>
<option value="No Error" style="background-color: #e3f2fd;" [#is_noerror_selected#] >No Error</option>
</select> '''
                column_value = column_value.replace("[#status#]",input_field_name)
                column_value = column_value.replace("[#is_running_selected#]",is_running_selected)
                column_value = column_value.replace("[#is_done_selected#]",is_done_selected)
                column_value = column_value.replace("[#is_error_selected#]",is_error_selected)
                column_value = column_value.replace("[#is_notstarted_selected#]",is_notstarted_selected)
                column_value = column_value.replace("[#is_noactivity_selected#]",is_noactivity_selected)
                column_value = column_value.replace("[#is_noerror_selected#]",is_noerror_selected)
                column_value = column_value.replace("[#tla_key#]",'"'+tla_key+'"')

            elif "comment" in column_value:
                column_value=''' <input type="text" name=[#comment#] style="background-color: #e3f2fd;" value={{tlas[[#tla_key#]].comment}}>  '''
                column_value = column_value.replace("[#comment#]", input_field_name)

            elif "monitored_by" in column_value:
                input_field_name_mon=input_field_name.replace("_principal",'').replace("_assistant",'')
                input_field_name_rank=input_field_name_mon.replace("_monitored_by",'_duty_rank')
                duty_rank=input_field_name.replace("\"",'').split('_')[-1]

                column_value=''' <input type="text" name=[#monitored_by#] class=[#monitored_by_class#] style="background-color: #e3f2fd;" value={{tlas[[#tla_key#]].monitored_by}}>
     <input type="text" name=[#duty_rank#] hidden="hidden" value={{tlas[[#tla_key#]].duty_rank}}>'''
                column_value = column_value.replace("[#monitored_by#]", input_field_name_mon)
                column_value = column_value.replace("[#duty_rank#]",input_field_name_rank)
                column_value = column_value.replace("[#monitored_by_class#]","\"monitored_by_"+duty_rank+"\"")

            column_value = column_value.replace("[#tla_key#]","\""+tla_key+"\"")

        tdlist.append(tdflagbeg + column_value + tdflagend)

    return tdlist


def create_compliacne_report_template2():
    f = open(basedir + 'templates\\compliance_report_create_frame.html','r')
    compliance_report_frame=f.read()
    f.close()
    tla_status_stub_begin=compliance_report_frame.index("[%")
    #print(f'stubbeg:{tla_status_stub_begin}')
    tla_status_stub_end=compliance_report_frame.index("%]")
    #print(f"stubend:{tla_status_stub_end}")
    tla_status_stub = compliance_report_frame[tla_status_stub_begin:tla_status_stub_end+2]
    #print("status-stub")
    #print(tla_status_stub)
    tla_status  = CreateTableHtml2()
    #print("tla_status")
    #print(tla_status)
    compliance_report=compliance_report_frame.replace(tla_status_stub,tla_status)
    html_file = open(basedir+'templates\\compliance_report_create_template.html','w')
    print(compliance_report,file=html_file, flush=True)
    html_file.close()
   
   
def send_compliance_report2(report_name):
    mailto='CRDSSOOncall@sas.com'
    #mailto='zhiqiang.zhang@sas.com'
    subject = 'AMS STATUS '+ GetReportTimeFlag2()+' EST'
    pythoncom.CoInitialize()    
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = subject
    mail.To = mailto
    #mail.CC = mailcc
    mail.BodyFormat=2
    #print(basedir+report_name)
    html_file_handler=open(basedir+report_name,'r')
    html_file_content=html_file_handler.read()
    mail.HTMLBody = html_file_content
    #mail.Attachments.Add('C:\Users\xxx\Desktop\git_auto_pull_new.py')
    mail.Send()
    