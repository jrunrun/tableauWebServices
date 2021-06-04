# from django.http import HttpResponse



from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt, datetime
import time

# APP_LOG_FILE = os.getenv('APP_LOG_FILE')
APP_LOG_FILE = 'app.log'

# Simple logging object with hardcoded log file from the settings
class LogFile():
    def __init__(self, debug_logs=False):
        # Little helper method for making logs consistent and clean
        # log_file = settings.APP_LOG_FILE
        log_file = APP_LOG_FILE
        self.debug_logs = debug_logs
        try:
            self.log_file_obj = open(log_file, 'ab', buffering=0)
        except IOError:
            print("Error: File '{}' cannot be opened to write for logging".format(log_file))
            raise

    def log(self, message, type="status"):
        # Don't log status level if debug mode is turned off
        if self.debug_logs is False:
            if type=="status":
                return
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        log_line = "{} : [{}] {} \n".format(cur_time, type.upper(), message)
        try:
            self.log_file_obj.write(log_line.encode('utf8'))
        except UnicodeDecodeError as e:
            self.log_file_obj.write(bytes(log_line))


# Create a logger
log = LogFile()
log.debug_logs = True

def index(request):
    return HttpResponse("Hello, world. You're at the authService index.")


#http://localhost:8081/ticket/api/?svr=http://localhost:8000&u=rdugger&s=agency

class GetTicket(APIView):
    def post(self, request):
        #server = request.GET['svr']
        #user = request.GET['u']
        #site = request.GET['s']
        print(datetime.datetime.now())
        print("Begin encode body")
        encoded_json = request.body
        print(datetime.datetime.now())
        print("End encode body")
        print(encoded_json)
        
        #Need to replace with settings.py ENV VAR
        #TEDS Test TS
        server = 'https://44.228.110.16/trusted/'
        log.log("tableau server url is {}".format(server))

        #TEDS Prod TS

        #server = 'https://demo.tservertrust.tableau.com/trusted/'
        print(datetime.datetime.now())
        secret = 'wanna-be-a-baller-shot-caller-20inch-blades-on-an-impala'
        try:
            print(datetime.datetime.now())
            print("decode start")
            decoded = jwt.decode(encoded_json, secret, algorithms=['HS256', ])
            print(datetime.datetime.now())
            print("decode end")
        except Exception as e:
            print(e)
            print(datetime.datetime.now())
            return HttpResponseForbidden()
            print(datetime.datetime.now())
        print(decoded)
        
        #server = decoded['server']
        user = decoded['username']
        site = decoded['vertical']
        
        #verify = False <-- ignore ssl check
        r = requests.post(server, data={'username': user, 'target_site': site}, verify=False)
        print('testing')
        print(r)

        if r.status_code == 200:
            if r.text != '-1':

                return Response(r.text)
            else:
                return('Error getting ticket: -1')
        else:
            return ('Could not get trusted ticket with status code', str(r.status_code))

        #r = requests.post(ts_url, data={'username': user, 'target_site': site})

        #if r.status_code == 200:
        #    if r.text != '-1':
        #        ticketID = r.text
        #        return Response(r)
        #    else:
        #        return('Error getting ticket: -1')
        #else:
        #    return ('Could not get trusted ticket with status code', str(r.status_code))


