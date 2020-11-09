import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
#from HandoffHandler import *
from CommonHandler import *
import requests
import base64
import time
import sys
import jira
import configparser


#设置signal文件来控制是否启动/终止刷新DM ticket 列表
#startinitdmticketlistsignal = c:\tmp\StartInitDMTicketList.sig
#stopinitdmticketlistsignal = c:\tmp\StopInitDMTicketList.sig



def getopt():
    #print(sys.argv)
    ArgKeys=("WorkBook","CommentType","MonitorGroup","HandoffTo")
    Args={"WorkBook":'',"CommentType":'',"MonitorGroup":'',"HandoffTo":''}   
    for i in range(len(sys.argv)-1):
        Args[ArgKeys[i]] = sys.argv[i+1].replace('&nbsp;',' ')
    #print(Args)
    
    return Args   


def InitDMTicketCfgSchduler(Fun, ParaList):
    StartTime=time.time()
    StartSignal= Config.get("Default","StartInitDMTicketListSignal")
    StopSignal= Config.get("Default","StopInitDMTicketListSignal")
    
    while True:
        time.sleep(300)        
        CurTime =time.localtime(time.time())
        if os.path.exists(StartSignal):
            Fun(ParaList)
            print('DM Ticket List was updated.')
            os.remove(StartSignal)
        if os.path.exists(StopSignal):
            os.remove(StopSignal)
            break

    
def GetTicketKeyLst():
    TicketKeyLst=[]
    #DMTicketFilterURL = "https://www.ondemand.sas.com/jira/issues/?filter=23310"
    DMTicketFilterURL = Config.get("Authentication","DMTicketFilterURL")
    UserName = Config.get("Authentication","UserName")
    PassWord = Config.get("Authentication","PassWord")
    #Auth=base64.b64encode(b'scnzqz:Oracle-3i')
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
       DMTicketFilterURL,
        data=None,
       headers=Header
    )


    issuetablebeg = '''<issuetable-web-component data-content="issues">'''
    issuetablebeg_len = len(issuetablebeg)
    issuetableend = '''</issuetable-web-component>'''
    issuetablebeg_position = response.text.find(issuetablebeg)
    issuetableend_position = response.text.find(issuetableend)
    print(["beg:",issuetablebeg_position, "     end:", issuetableend_position])
    issuetablexml = response.text[issuetablebeg_position + issuetablebeg_len : issuetableend_position]
    # xmlparser = sax.make_parser()
    # xmlparser.setFeature(sax.handler.feature_namespaces, 0)  # turn off namepsaces
    Handler = JiraFilterHandler()
    # xmlparser.setContentHandler(Handler)
    # xmlparser.parse(xmlfilepath)
    print(issuetablexml)
    sax.parseString(issuetablexml, Handler)
    return Handler.tickets

def InitDMTicketsCfg():
    Ticketlst=GetJiraTickets("DMTicketFilterURL")
    TicketKeyDic={}
    for Ticket in Ticketlst:
        TLA=''.join(Ticket["issuekey"].strip()[0:3])
        TicketKeyDic[TLA]=Ticket["issuekey"].strip()
    Config['ActiveDMTickets'] = TicketKeyDic
    Config.write(open(ConfigFile, mode="w"))
    print(TicketKeyDic)
    print(time.asctime(time.localtime(time.time())))
    
if __name__ == "__main__":
    print(Config.sections())
    print('\n\n'+'''-----Started at:'''+time.asctime(time.localtime(time.time()))+'''-----''')
    print("InitDMTicketCfgSchduler")
    InitDMTicketsCfg()

    print('''-----Ended at:'''+time.asctime(time.localtime(time.time()))+'''-----''')