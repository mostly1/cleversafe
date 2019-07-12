#!/usr/bin/env python
#Author: Jeff Mazzone
#Script to grab warning and critical messages from Console in cleversafe.

import requests
import json
import argparse
import time

#initialize arguments
parser = argparse.ArgumentParser(description ='Icinga2 plugin to monitor pull warning and critical messages from the event console in IBM/Cleversafes manager', usage='use "%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-H', action="store", dest="host", help="ip address or hostname", required=True)
parser.add_argument('-c', action="store", dest="command", help='''Use one of the following commands at a time. At least one is required.
                   get_events             gets events from manager event console''', required=True)

args = parser.parse_args()
host = args.host
command = args.command

#set credentials
with open("creds.json", "r") as file:
    auth = json.load(file)
user=auth['creds']['username']
pwd=auth['creds']['password']


#set timestamps
now = int(round(time.time()*1000))
day_in_miliseconds = 86400000
week_in_miliseconds = 604800000
then = now - day_in_miliseconds
then_week = now - week_in_miliseconds

#build URL and load response
url = "https://"+host+":443/manager/api/json/1.0/eventConsole.adm"


def output(msg_type,message,tstamp):
    if msg_type == "crit":
        print "**** Critical Message "+tstamp+" ****\n"
        print message+ "\n"
    if msg_type == "warn":
        print "**** Warning Message "+tstamp+" ****\n"
        print message+ "\n"
    if msg_type == "info":
        print "**** Info Message "+tstamp+" ****\n"
        print message+ "\n"
    if msg_type == "err":
        print "**** Error Message "+tstamp+" ****\n"
        print message+ "\n"
    if msg_type == "clr":
        print "**** Cleared Message "+tstamp+" ****\n"
        print message+ "\n"



def process_results(data,tstamp):
    for event_crit in data['responseData']['streamElements']:
        if event_crit['eventLevel'] == "critical":
            message = event_crit['message']
            msg_type = "crit"
            output(msg_type,message,tstamp)
    for event_warn in data['responseData']['streamElements']:
        if event_warn['eventLevel'] == "warning":
            message = event_warn['message']
            msg_type = "warn"
            output(msg_type,message,tstamp)
    for event_info in data['responseData']['streamElements']:
        if event_info['eventLevel'] == "info":
            message = event_info['message']
            msg_type = "info"
            output(msg_type,message,tstamp)
    for event_error in data['responseData']['streamElements']:
        if event_error['eventLevel'] == "error":
            message = event_error['message']
            msg_type = "err"
            output(msg_type,message,tstamp)
    for event_cleared in data['responseData']['streamElements']:
        if event_cleared['eventLevel'] == "cleared":
            message = event_cleared['message']
            msg_type = "clr"
            output(msg_type,message,tstamp)


#Pulls all console messages from last 24 hours.
def get_events_24h():
    #set payload with timestamp params
    tstamp = "24h"
    payload = {'startTimestamp':then,"endTimestamp":now}
    r = requests.get(url, auth=(user,pwd), params=payload, verify=False)
    data = json.loads(r.text)
    process_results(data,tstamp)

#pulls all console messages from last 7 days.
def get_events_7d():
    #set payload with timestamp params
    tstamp = "7d"
    payload = {'startTimestamp':then_week,"endTimestamp":now}
    r = requests.get(url, auth=(user,pwd), params=payload, verify=False)
    data = json.loads(r.text)
    process_results(data,tstamp)

#Pulls all console messages from open incidents section in GUI
def get_events():
    #set payload with stream type. No time stamp needed.
    payload = {'streamTypes':'openIncidentStates'}
    r = requests.get(url, auth=(user,pwd), params=payload, verify=False)
    data = json.loads(r.text)
    status=0
    for event in data['responseData']['streamElements']:
        if event['eventLevel'] == "critical":
            status=2
            message = event['message']
        elif event['eventLevel'] == 'error':
            status =3
            message = event['message']
        elif event['eventLevel'] == "warning":
            status=1
            message = event['message']
    if status == 3:
        print "CRITICAL - " + message + " - Check manager GUI"
        exit(2)
    if status == 2:
        print "CRITICAL - " + message + " - Check manager GUI"
        exit(2)
    elif status == 1:
        print "WARNING - " + message + "  - Check manager GUI"
        exit(1)
    print "No Current events to report..."
    exit(0)

#main
if command == "get_events":
    get_events()
elif command == "get_events_24h":
    get_events_24h()
elif command == "get_events_7d":
    get_events_7d()
