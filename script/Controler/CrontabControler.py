import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from CrontabHandler import query_crontab_by_tla,reload_crontab_file
#from CommonHandler import *
from flask import render_template, url_for, redirect,request
from flaskapp import flask_app
import datetime
from script.Handler.CommonHandler import *
import re

@flask_app.route("/crontab_query",methods=["GET","POST"])
def crontab_query():
    tlas=GetTlaList()
    if request.method=='GET':

        return render_template("crontab_query.html" ,tlas=tlas,cur_tla="",env="")
    else:
        result=request.form
    
        if "tla" in result.keys():
            tla=result["tla"].strip().upper()
        else:
            tla=""

        if "env" in result.keys():
            env=result["env"].strip().upper()
        else:
            env=""

        if "period_beg" in result.keys():
            period_beg=result["period_beg"]
        else:
            period_beg=""

        if "period_end" in result.keys():
            period_end=result["period_end"]
        else:
            period_end=""
        period_beg = re.sub("\D", "", period_beg)
        period_end = re.sub("\D", "", period_end)
        if period_beg=="":
            period_beg=0
        else:
            period_beg=int(period_beg)
        if period_end=="":
            period_end=0
        else:
            period_end=int(period_end)
        if "query" in result.keys():
            rows = query_crontab_by_tla(tla, env,period_beg,period_end)

            html_content = render_template("crontab_query_content.html", rows=rows)
            crontab_file="./templates/temp/crontab_"+str(datetime.datetime.now())[0:19].replace(':','-').replace(" ","-")+".html"
            html_file = open(crontab_file, "w")
            print(html_content, file=html_file, flush=True)
            html_file.close()
            return render_template("crontab_query.html", tlas=tlas,cur_tla=tla,env=env)

        elif "reload" in result.keys():

            if "crontab_src" in request.files.keys():
                file_src = request.files["crontab_src"]
            else:
                return render_template("crontab_query.html", tlas=tlas, cur_tla=tla, env=env)

            if file_src is None or tla=="" or env=="":
                    return render_template("crontab_query.html", tlas=tlas, cur_tla=tla, env=env)
            else:
                new_crontab_conent=[]
                for crontab in file_src.stream:# .read().decode("utf-8")  # stream is byte stream
                    new_crontab_conent.append(crontab.decode("utf-8"))

                return render_template("crontab_reload.html", cur_tla=tla,env=env, new_crontab_conent=new_crontab_conent)

            #return render_template("crontab_reload.html", tla=tla, env=env, crontab_query_content="")

        elif "querymail" in result.keys():
            maillist=get_maillist("A110 - SEM")
            mailjsonlist=[]
            for mail in maillist:
                mail["ReceivedTime"]=str(mail["ReceivedTime"])
                mail["Attachments"]="Not supported"
                mailjson=json.dumps(mail)
                mail["json"]=mailjson
                mailjsonlist.append(mail)
            return render_template("crontab_mail_query.html",rows=mailjsonlist)
        else:
            return render_template("show_request.html", result=result, method=request.method,data="")



@flask_app.route("/crontab_query_content",methods=["GET","POST"])    
def crontab_query_content():
    all_reports=[report for report in os.listdir("./templates/temp/") if report.find("crontab") >=0 and os.path.isdir(report) ==False]
    if len(all_reports)>0:
        newest_report=all_reports[0]

        for report in all_reports[1:]:
            if report > newest_report:
                os.remove("./templates/temp/" + newest_report)
                newest_report = report
            else:
                os.remove("./templates/temp/" + report)
        return render_template("./temp/" + newest_report)

    else:
        newest_report="No Data"
        return newest_report



@flask_app.route("/links")
def links():
    links={}
    links["jira"]='''https://www.ondemand.sas.com/jira/secure/Dashboard.jspa?selectPageId=20448'''
    links["jira"]="https://www.ondemand.sas.com"
    links["servicenow"]='''https://sas.service-now.com/nav_to.do?uri=%2Fhome_splash.do%3Fsysparm_direct%3Dtrue'''
    links["confluence"]='''https://www.ondemand.sas.com/confluencedoc/display/SSODMAS/Application+Managed+Services+Home+Page'''
    links["zabbix"]='''https://status.ondemand.sas.com/zabbix/zabbix.php?action=dashboard.view'''
    links["perc"]='''http://perc.na.sas.com/'''
    links["thycotic"]='''https://securevault.sas.com/secretserver/SecretView.aspx?secretid=27914'''
    links["replicon"]="http://baidu.com.cn"
    
    if request.method=='GET':
        result=request.args
    else:
        result=request.form
    if "link" in result.keys():
        url=links[result["link"].strip().lower()]
    #return render_template("show_request.html",result=result,method=url)   
    html=render_template("/links.html",url=url)
    print(html)
    return html


@flask_app.route("/crontab_reload", methods=["GET","POST"])
def crontab_reload():
    tlas=GetTlaList()
    if request.method=='GET':
        result=request.args
    else:
        result=request.form
        if "tla" in result.keys():
            tla=result["tla"].strip().upper()
        else:
            tla=""

        if "env" in result.keys():
            env=result["env"].strip().upper()
        else:
            env=""

        if "reload" in result.keys():
            new_crontab_conent=[]
            for key,value in result.items():
                if key.find("crontab_")>=0:
                    new_crontab_conent.append(value)
                else:
                    continue

            if len(new_crontab_conent)>=0:
                reload_crontab_file(tla,env,new_crontab_conent)
                return render_template("crontab_query.html",tlas=tlas, cur_tla=tla,env=env)
            else:
                pass

        elif "cancel" in result.keys():
            return render_template("crontab_query.html",tlas=tlas, cur_tla=tla,env=env)

        else:
            return render_template("home.html")



@flask_app.route("/crontab_mail_view", methods=["GET", "POST"])
def crontab_mail_view():
    if request.method=='GET':
        result=request.args
        if "json" in result.keys():
            mail = json.loads(result["json"])
            return render_template("crontab_mail_view.html", row=mail)
    else:
        result=request.form
        if "cancel" in result.keys():
            return render_template("crontab_query.html",tlas=[], cur_tla=[],env=[])
        else:
            return "No Data Was Found!"

@flask_app.route("/crontab_mail_download", methods=["GET", "POST"])
def crontab_mail_download():
    if request.method=='GET':
        result=request.args

    else:
        result=request.form
    #return render_template("show_request.html", result=result, data="77777777777777777")

    if "show_attachement" in result.keys() and "EntryID" in result.keys():
        mail_id = result['EntryID'].strip()
        mail_subject=result["Subject"].strip()
        saved_file_list=save_attachment_by_id("A110 - SEM", mail_id)
        print(mail_id,saved_file_list)
        return render_template("crontab_mail_download.html",files=saved_file_list,mail_id=mail_id,mail_subject=mail_subject)
    else:
        return redirect(request.referrer)

