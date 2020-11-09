from flask_wtf import FlaskForm 
from wtforms import (TextField, SubmitField,IntegerField,
                    BooleanField,RadioField,SelectField,
                     DecimalField,TextAreaField,PasswordField)
class BaseForm(FlaskForm):
    query_text=TextAreaField("Query:")
    query_string=TextField("Qery")
    query_select=SelectField("Qery")
    all=SubmitField("All")
    next=SubmitField("Next")
    done=SubmitField("Done")
    apply=SubmitField("Apply")
    cancel=SubmitField("Cancel")
    create=SubmitField("Create")
    update=SubmitField("Update")
    submit=SubmitField("Submit")
    
    
    
    
class QueryForm(FlaskForm):
    query_text=TextAreaField("Query:")
    query_string=TextField("Qery")
    query_select=SelectField("Qery")
    all=SubmitField("All")
    next=SubmitField("Next")
    done=SubmitField("Done")
   
    
class TlaForm(FlaskForm):
    query_string=TextField("Qery")
    all=SubmitField("All")
    id =TextField("id")
    tla=TextField("TLA")
    customer_name=TextField("Customer Name")
    solution=TextField("Solution")
    runbook_url=TextField("Runbook URL")
    tl=TextField("Teach Lead")
    project_code=TextField("Project Code")
    comment=TextField("Comment")
    enabled=TextField("Enabled")
    apply=SubmitField("Apply")
    cancel=SubmitField("Cancel")

    
class RegulationForm(FlaskForm):
    tla=TextAreaField("tla:")
    reporter=TextAreaField("reporter:")
    begin_time=TextAreaField("begin_time:")
    description=TextAreaField("description:")
    enabled=TextAreaField("enabled:")
    key_words=TextAreaField("key_words:")
    apply=SubmitField("Apply")

    
class IssueForm(FlaskForm):
    tla=TextAreaField("tla:")
    ticket_type=TextAreaField("ticket_type:")
    ticket_number=TextAreaField("ticket_number:")
    begin_time=TextAreaField("begin_time:")
    description=TextAreaField("description:")
    enabled=TextAreaField("enabled:")
    key_words=TextAreaField("key_words:")
    apply=SubmitField("Apply")

class TaskForm(FlaskForm):
    tla=TextAreaField("tla:")
    ticket_type=TextAreaField("ticket_type:")
    ticket_number=TextAreaField("ticket_number:")
    begin_time=TextAreaField("begin_time:")
    description=TextAreaField("description:")
    enabled=TextAreaField("enabled:")
    key_words=TextAreaField("key_words:")
    apply=SubmitField("Apply")

class CrontabForm(FlaskForm):
    tla=TextAreaField("tla:")
    minute=TextAreaField("minute:")
    hour=TextAreaField("hour:")
    day=TextAreaField("day:")
    month=TextAreaField("month:")
    wday=TextAreaField("wday:")
    command=TextAreaField("command:")
    crontab=TextAreaField("crontab:")
    enabled=TextAreaField("enabled:")
    key_words=TextAreaField("key_words:")
    apply=SubmitField("Apply")

