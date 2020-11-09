import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from ComplianceReportHandler2 import *


#from CommonHandler import *
from flask import render_template, url_for, redirect,request
from flaskapp import flask_app
from script.Form.forms import QueryForm,TlaForm

import datetime
#from script.Controler.CommonControler import *
import json


@flask_app.route("/compliance_report_create",methods=["GET","POST"])
def compliance_report_create():
    form_part={}
    tla_part_dic = {}
    form_handled= []
    jira_tickets = []
    #jira_tickets=GetJiraTickets()
    servicenow_tickets = []
    #servicenow_tickets=GetServiceNowTickets()
    smallfile_tickets = []
    other_tasks = []
    if request.method=='GET':
        environments=query_environments2()

        for env in environments:
            #print("env:",env.tla, "detype:",env.deployment_type)
            tla = EnvUIData2()
            tla.tla = env.tla
            tla.deployment_type=env.deployment_type
            tla.comment=env.comment
            tla.duty_rank= env.monitored_by
            tla.monitored_by=env.monitored_by
            tla_part_dic[tla.tla+"_"+tla.deployment_type]=tla

        form_part["principal"]=""
        form_part["assistant"]=""
        form_part["is_respond"]="No"
        form_part["is_warning"]="No"

        create_compliacne_report_template2()
         #return render_template("./compliance_report_create-bak.html",rows=rows)

        all_jsonfiles = [jsonfile for jsonfile in os.listdir("./templates/temp/") if
                             jsonfile.find("tla_history_status") >= 0 and os.path.isdir(jsonfile) is False]
        if len(all_jsonfiles) > 0:
            newest_jsonfile = all_jsonfiles[0]
            for jsonfile in all_jsonfiles[1:]:
                if jsonfile > newest_jsonfile:
                    os.remove("./templates/temp/" + newest_jsonfile)
                    newest_jsonfile = jsonfile
                else:
                    os.remove("./templates/temp/" + jsonfile)
            tla_status_json_handle = open("./templates/temp/" + newest_jsonfile)
            tla_status_json = tla_status_json_handle.read()
            [form_part, tla_part_dic, jira_tickets, servicenow_tickets, smallfile_tickets,other_tasks] = json.loads(tla_status_json)
            tla_status_json_handle.close()
        #print(tla_part_dic["MRFRAS_PROD"])
        return render_template("compliance_report_create_template.html", form=form_part, tlas=tla_part_dic, jira_tickets=jira_tickets, servicenow_tickets=servicenow_tickets, smallfile_tickets=smallfile_tickets, other_tasks=other_tasks)

    else:
        form=request.form
        #return render_template("show_request.html",result=result,method=request.method)
        if "create" in form.keys():
            if form["principal"].strip()=="None" or form["assistant"].strip()=="None":
                return redirect(url_for("compliance_report_create"))

            for key in form.keys():
                if key.find('jiraticketnum')>=0:
                    if form[key].strip() != "" :
                        jira_tickets.append(form[key])
                        form_handled.append(key)

                if key.find('snticketnum')>=0:
                    if form[key].strip() != "":
                        servicenow_tickets.append(form[key])
                        form_handled.append(key)

                if key.find('smallfilenum')>=0:
                    if form[key].strip() != "":
                        smallfile_tickets.append(form[key])
                        form_handled.append(key)

                if key.find('tasknum')>=0:
                    if form[key].strip() != "":
                        other_tasks.append(form[key])
                        form_handled.append(key)

            #print(['Jiratickets \n',jira_tickets])
            #print(['sntickets \n',servicenow_tickets])
            #print(['smalfiletickt \n',smallfile_tickets])
            #print(['tasks \n',other_tasks])

            #jira_tickets = GetJiraTickets()+jira


            #return render_template("show_request.html",result=form,method=request.method)




            for key in form.keys():
                if key in form_handled:
                    #print(['pass:',key])
                    continue
                if key.find("_status")<0 and  key.find("_comment")<0 and key.find("_monitored_by")<0 and key.find("_duty_rank")<0:
                    form_part[key]=form[key]
                    form_handled.append(key)
                    #print(key)
                    continue


                key_heads=key.split("_")
                tla=EnvUIData2()
                tla.tla=key_heads[0]
                tla.deployment_type = key_heads[1]



                key_status=tla.tla+"_"+tla.deployment_type+"_status"
                key_comment=tla.tla+"_"+tla.deployment_type+"_comment"
                key_duty_rank=tla.tla+"_"+tla.deployment_type+"_duty_rank"
                key_monitored_by=tla.tla+"_"+tla.deployment_type+"_monitored_by"
                is_handled=0

                if key_status in form.keys():
                    tla.status=form[key_status]
                    form_handled.append(key_status)
                else:
                    raise MsgException("Not find the key: "+ key_status)

                if key_comment in form.keys():
                    tla.comment=form[key_comment]
                    form_handled.append(key_comment)
                else:
                    raise MsgException("Not find the key: "+ key_comment)

                if key_duty_rank in form.keys():
                    tla.duty_rank=form[key_duty_rank]
                    form_handled.append(key_duty_rank)
                else:
                    raise MsgException("Not find the key: "+ key_duty_rank)

                if key_monitored_by in form.keys():
                    tla.monitored_by=form[key_monitored_by]
                    form_handled.append(key_monitored_by)
                else:
                    raise MsgException("Not find the key: "+ key_monitored_by)

                #print(tla)


                tla_part_dic[tla.tla + "_" + tla.deployment_type] = tla

            #return render_template("show_request.html",result=form,method=request.method)

            #print(['create \n'])
            #print(["form", form_part])
            #print(['jira:', jira_tickets])
            #print(['SN:', servicenow_tickets])
            #print(['sfile:', smallfile_tickets])
            #print(['otask:', other_tasks])

            compliance_report=json.dumps([form_part,tla_part_dic,jira_tickets,servicenow_tickets,smallfile_tickets,other_tasks],cls=MyEncoder2)

            create_compliacne_report_view_template2()
            auto_scan_jiras=GetJiraTickets("amsticketfilterurl")
            for jira in auto_scan_jiras:
                jira_tickets.append(jira["issuekey"]+": "+jira["summary"])
            servicenow_tickets = GetServiceNowTickets("crdsnticketsurl") + servicenow_tickets

            if len(jira_tickets)==0:
                jira_tickets.append("None")
            if len(servicenow_tickets)==0:
                servicenow_tickets.append("None")
            if len(smallfile_tickets)==0:
                smallfile_tickets.append("None")



            html_content= render_template("compliance_report_view_template.html", form=form, jira_tickets=jira_tickets, servicenow_tickets=servicenow_tickets, smallfile_tickets=smallfile_tickets, other_tasks=other_tasks)
            report_name="./templates/temp/compliance_report_"+str(datetime.datetime.now())[0:19].replace(':','-').replace(" ","-")+".html"
            html_file_standerby=open(report_name,"w")
            print(html_content,file=html_file_standerby,flush=True)
            html_file_standerby.close()


            return render_template("compliance_report_view.html",compliance_report=compliance_report,report_name=report_name)

        elif "cancel" in form.keys():
            #return render_template("/home.html")
            #return render_template("show_request.html",result=result,method=request.method)
            #print('cancel')
            return render_template("home.html")
        else:
            return render_template("home.html")
        
@flask_app.route("/compliance_report_view",methods=["GET","POST"])
def compliance_report_view():
    all_reports = [report for report in os.listdir("./templates/temp/") if
                   report.find("compliance_report") >= 0 and os.path.isdir(report) is False]
    if len(all_reports) > 0:
        newest_report = all_reports[0]

        for report in all_reports[1:]:
            if report > newest_report:
                os.remove("./templates/temp/" + newest_report)
                newest_report = report
            else:
                os.remove("./templates/temp/" + report)
        return render_template("./temp/" + newest_report)

    else:
        newest_report = "No Data"
        
@flask_app.route("/compliance_report_send",methods=["GET","POST"])
def compliance_report_send():
    if request.method=='GET':
        form=request.args
        
    else:
        form=request.form
    
    
    if "cancel" in form.keys():
        
        [form_part,tla_part_dic, jira_tickets,servicenow_tickets,smallfile_tickets,other_tasks] = json.loads(form["compliance_report"])
        print(['cancel \n',form["compliance_report"]])
        print(["form_part",form_part])
        #print(['tla_part:', tla_part])
        #print(['jira:',jira_tickets])
        #print(['SN:',servicenow_tickets])
        #print(['sfile:',smallfile_tickets])
        #print(['otask:',other_tasks])
        return render_template("compliance_report_create_template.html",form=form_part, tlas=tla_part_dic,jira_tickets=jira_tickets,servicenow_tickets=servicenow_tickets,smallfile_tickets=smallfile_tickets, other_tasks=other_tasks)
    if "send" in form.keys():
        #return render_template("show_request.html", result=form, method=request.method)
        [form_part, tla_part_dic, jira_tickets, servicenow_tickets, smallfile_tickets,
         other_tasks] = json.loads(form["compliance_report"])

        tla_history_status_jsonfile = "./templates/temp/tla_history_status_" + str(datetime.datetime.now())[0:19].replace(':',
                                                                                                         '-').replace(
            " ", "-") + ".html"
        tla_history_status_jsonfile_handle = open(tla_history_status_jsonfile, "w")

        print(form["compliance_report"], file=tla_history_status_jsonfile_handle, flush=True)
        tla_history_status_jsonfile_handle.close()
        report_name=form["report_name"]
        #print(report_name)
        send_compliance_report2(report_name)
        return render_template("./home.html")