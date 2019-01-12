#!/usr/bin/env python

import requests, json, datetime

def logThis(path,message):
    with open(path,"ab") as logFile:
        logFile.write(message + '\n')

def getCreds(path):
    values = []
    keys = []
    count = 0
    creds = {}

    with open(path,"rb") as raw_creds:
        for x in raw_creds:
            pair = x.split("=")

            keys.append(pair[0].strip())
            values.append(pair[1].strip())

    for y in keys:
        creds[y] = values[count]
        count = count + 1

    return creds

cred_path = "/home/ddns/credentials"
logPath = "/var/log/ddns-cron.log"

timeStamp = datetime.datetime.now().strftime("%m-%w-%YT%H:%M")
domain_auth = getCreds(cred_path)

auth = "sso-key " + domain_auth['id'] + ":" + domain_auth['secret']

headers = {"Authorization": auth}

reg_ip = requests.get(domain_auth['uri'], headers=headers).json()[0]['data']

current_ip = requests.get("http://ip.42.pl/raw").text

if reg_ip != current_ip:
    data = [
        {
            "data" : current_ip,
            "ttl" : 3600
        }
    ]

    requests.put( domain_auth['uri'], headers=headers, json=data)
    
    logThis(logPath, "[" + timeStamp + "] " + reg_ip + " --> " + current_ip)
    exit("[" + timeStamp + "] " + reg_ip + " --> " + current_ip)

logThis(logPath, "[" + timeStamp + "] " + current_ip)
exit("[" + timeStamp + "] " + current_ip)
