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
    return HttpResponse("Hello, world. You're at the contentService index.")





# def getViews(request):
#     return HttpResponse("Hello, world. You're at the contentService index.")
