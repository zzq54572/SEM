import os

log_dir='''C:\WorkSpace\PythonProgram\SSOETLMonitor\logs'''
log_file=__name__
def logging(information):
    messages=[]
    log=open(os.path.join(log_dir,log_file),"a")
    if type(information)!=list:
        messages.append(information)
    else:
        messages=information
    for message in messages:
        print(message,file=log, flush=True)
    log.close()

def log_stub():
    pass
    
    
def add_log_at_begin_and_end(decorated_func):
    def wrapper(*args,**kw):
        logging(f"<{decorated_func.__name__}>")
        result = decorated_func(*args,**kw)
        logging(f"</{decorated_func.__name__}>")
        return(result)
    return wrapper
    

def add_log_at_begin_and_end_stub(decorated_func):
    def wrapper(*args,**kw):        
        result = decorated_func(*args,**kw)
        return(result)
    return wrapper
    

class MsgException(Exception):
    "this is user's Exception for check the length of name "
    message=""
    def __init__(self,message):
        self.message = message
    def __str__(self):
        try:
            return(self.message) 
        except Exception as e:
            print (e)