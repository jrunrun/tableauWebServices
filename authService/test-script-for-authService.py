
# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseForbidden, HttpResponseBadRequest
# from django.template import loader, RequestContext
# from django.shortcuts import redirect

from datetime import datetime, timedelta
import time

# from django.conf import settings
# from .models import *

import jwt  # https://github.com/jpadilla/pyjwt/
import requests

# from django.db import models
# from django.db.models import ObjectDoesNotExist
# from django.forms.models import model_to_dict
# from django.core.cache import cache
# from  django.utils import translation
# from django.contrib.admin.views.decorators import staff_member_required

# import functools
# from collections import OrderedDict
# from typing import List, Dict, Optional

import json


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

# JWT Secret for HMAC

JWT_SECRET='wanna-be-a-baller-shot-caller-20inch-blades-on-an-impala'
# TRUSTED_TICKET_BROKER_URL='http://54.184.21.61/ticket/api/'
TRUSTED_TICKET_BROKER_URL='http://localhost:8000/authService/ticket/api/'

# Test values for username, site_content_url
username = 'jcraycraft'
site_content_url = 'retail'

# Ticket Broker Location
# TRUSTED_TICKET_BROKER_URL = os.getenv('TRUSTED_TICKET_BROKER_URL')
# JWT_SECRET = os.getenv('JWT_SECRET')
# JWT_COOKIE_ALIAS = 'nrwl'
# JWT_ENTITLEMENT_COOKIE_ALIAS = 'abac'

def request_trusted_ticket(username, site_content_url):
    # Create JWT token for the session
    iat = time.time()
    jwt_payload = {'username': username,
                   'iat': iat,
                   'vertical': site_content_url
                   }
    # encoded_value = jwt.encode(jwt_payload, settings.JWT_SECRET, algorithm='HS256')
    encoded_value = jwt.encode(jwt_payload, JWT_SECRET, algorithm='HS256')
    log.log("JWT Payload is: {}".format(jwt_payload))
    log.log("Encoded JWT being sent: {}".format(encoded_value))
    # Make request to the ticket broker
    # broker_url = settings.TRUSTED_TICKET_BROKER_URL
    broker_url = TRUSTED_TICKET_BROKER_URL
    log.log("Requesting trusted ticket for {} on {} ".format(username, site_content_url))
    print("Requesting trusted ticket for {} on {} ".format(username, site_content_url))
    try:
        response = requests.post(url=broker_url, data=encoded_value)
        print(response)
        # print(response.content)
        # print(response.data)
        # print(response.json())

        log.log("Received ticket response without error")

    except ConnectionError as e:
        log.log("Post request to ticket broker failed", type='error')
        raise e

    try:
        ticket = response.json()
        log.log("Ticket is : {}".format(ticket))
        return ticket
    except Exception as e:
        log.log("Error in trusted ticket response from broker: {}".format(e), type='error')
        log.log("Response from broker was: {}".format(response))
        # Return -1 as if it were just a bad ticket request
        return "-1"


request_trusted_ticket(username, site_content_url)