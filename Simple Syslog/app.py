import os
import sys
import simplejson as json
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import getpass
import socket
import time

service = None
event_error = None
event_ok = None
status_healthy = None
status_message = None

email_from = raw_input("\nPlease enter sender email address: ")
password = getpass.getpass("\nPlease enter the password: ")
email_rcpt = raw_input("\nPlease enter recipient email address: ")
mtu_server = raw_input("\nPlease enter smtp server (ex: smtp.gmail.com): ")
mtu_port = raw_input("\nPlease enter smtp port (ex: 587): ")

log_path = raw_input("\nPlease enter the path where to store service total and error events: ")

def alert_email( notification, error_rate = None, total_events = None ):
    
    global email_from, email_rcpt, password, mtu_server, mtu_port

    email_headers = MIMEMultipart()
    email_headers['From'] = email_from
    email_headers['To'] = email_rcpt
    
    if notification == 'onservice':
        
        email_headers['Subject'] = "Service Alert: %s" % service
        email_body = "%sServiceName: %s; ServiceHealth: %s; ServiceMessage: %s" % (time.ctime(), service, status_healthy, status_message)
        
    elif notification == 'onevent':
        
        email_headers['Subject'] = "Event Alert: %s" % service
        email_body = "%s ServiceName: %s; TotalEvents: %s; ErrorRate: %s %%" % (time.ctime(), service, total_events, error_rate)
        
    email_headers.attach(MIMEText(email_body, 'plain'))
    
    smtp = smtplib.SMTP(mtu_server, mtu_port)
    smtp.starttls()  
    smtp.login(email_headers['From'], password)
    
    email = email_headers.as_string()
    
    smtp.sendmail(email_headers['From'], email_headers['To'], email)
    smtp.quit()
    
    email_headers = None
    
    if notification == 'onservice':
        
        print "\nServiceName: %s has sent a service email alert" %(service)

    elif notification == 'onevent':
        
        print "\nServiceName: %s has sent an event email alert" %(service)
        
def json_load():
    
    json_file = raw_input("\nPlease enter the location of json file: ")

    try:
        json_stdin = open(json_file, "r")
        
    except IOError:
        print "I/O Error: Cannot read %s \n" % json_file
        sys.exit()
        
    json_stack = json.loads(json_stdin.read())
    json_stdin.close()

    global service, event_error, event_ok, status_healthy, status_message
    
    
    for content in json_stack:

            status_healthy = json_stack[content]['status']['healthy']
            status_message = json_stack[content]['status']['message']         
            event_error = json_stack[content]['events']['error']
            event_ok = json_stack[content]['events']['ok']
            service = json_stack[content]['service_id']
            
            service_status()
            event_status()
    
def service_status():
    
    if status_healthy == False:
        
        alert_email('onservice')
        
        sendlog('onservice')
        
def event_status():
  
    srv_event_log = os.listdir( log_path )
    
    total_events = event_error + event_ok
    
    if (service not in srv_event_log):
        
        if (total_events >= 1000):
        
            print "\nServiceName: %s 1000 event check is running for the first time and will initialize last log check " % service
        
            error_rate = calc_error_rate(total_events, event_error)
            
            if (error_rate > 10):
                                                                                   
                alert_email('onevent', error_rate, total_events)
                            
                sendlog('onevent', error_rate, total_events)          

            print "\n%s ServiceName: %s; TotalEvents: %s; ErrorRate: %s %%" % (time.ctime(), service, total_events, error_rate)

            save_event_log(total_events, event_error)
            
    elif (service in srv_event_log):
        
        last_log = read_event_log()
            
        last_total_events = int(last_log['TotalEvents'])
        last_event_error = int(last_log['EventError'])
                
        if (total_events > last_total_events):
            
            current_total_events = total_events - last_total_events
            current_event_error = event_error - last_event_error 

            if (current_total_events >= 1000):

                current_error_rate = calc_error_rate(current_total_events, current_event_error)
            
                if (current_error_rate > 10):                  
                                            
                    alert_email('onevent', current_error_rate, current_total_events)
                                        
                    sendlog('onevent', current_error_rate, current_total_events)
                    
                print "\n%s ServiceName: %s; TotalEvents: %s; ErrorRate: %s %%" % (time.ctime(), service, current_total_events, current_error_rate)
                     
                save_event_log(total_events, event_error)                      
                
        elif (total_events < last_total_events):
            
            print "\nServiceName: %s events counters were flushed hence reinitializing the logs" % service
            
            if (total_events >= 1000):
                
                error_rate = calc_error_rate(total_events, event_error)
            
                if (error_rate > 10):
                                            
                    alert_email('onevent', error_rate, total_events)
                                        
                    sendlog('onevent', error_rate, total_events)            
                
                print "\n%s ServiceName: %s; TotalEvents: %s; ErrorRate: %s %%" % (time.ctime(), service, total_events, error_rate)
                
                save_event_log(total_events, event_error)              

def sendlog(sysmsg, error_rate = None, total_events = None):
    
    buffer = 1024
    
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.connect(('127.0.0.1', 5005))
    
    if sysmsg == 'onservice':
        
        message = "%s ServiceName: %s; ServiceHealth: %s; ServiceMessage: %s" % (time.ctime(), service, status_healthy, status_message)
        
    elif sysmsg == 'onevent':
        
        message = "%s ServiceName: %s; TotalEvents: %s; ErrorRate: %s %%" % (time.ctime(), service, total_events, error_rate)
    
    srv.send(message)
    data = srv.recv(buffer)
    
    srv.close()

    if sysmsg == 'onservice':
        
        print "\nServiceName: %s has sent a service log state issue to syslog server: %s" %(service,data)

    elif sysmsg == 'onevent':
        
        print "\nServiceName: %s has sent an event log issue to syslog server: %s" %(service,data)

def save_event_log(total_events, event_error):
    
    os.chdir(log_path)
    
    message = "TotalEvents %s \nEventError %s" % (total_events, event_error)
    event_log = open(service, "w")
    event_log.write(message)
    
    event_log.close()
    
def read_event_log():
    
    os.chdir(log_path)
    
    event_log = open(service, "r")
    event_content = event_log.read()
    event_content_array = event_content.split()
    
    event_key_value = {}
    event_key_value[event_content_array[0]] = event_content_array[1]
    event_key_value[event_content_array[2]] = event_content_array[3]

    return event_key_value

def calc_error_rate(total_events, event_error):
        
    error_rate = ( 100 * event_error ) / total_events
    
    return error_rate

json_load()
