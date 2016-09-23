"""[logger] Logs all messages. Requires SLACK_LOGDIR and SLACK_BOTNAME env vars to be set"""

import json
import os
import requests
import time

LAST_CHANNEL = None

def on_text(msg, server):
    handle_message(msg, server)

def on_message(msg, server):
    handle_message(msg, server)

def handle_message(msg, server):
    global LAST_CHANNEL

    print "Logging: %s" % (msg,)

    token = os.environ["SLACK_TOKEN"]
    logdir = os.environ["SLACK_LOGDIR"]
    botname = os.environ["SLACK_BOTNAME"]

    r = requests.get("https://slack.com/api/users.list?token=%s" % (token,))
    j = json.loads(r.text)
    users = {x['id']: x['name'] for x in j['members']}
    try:
        user = users[msg['user']]
    except KeyError:
        user = "*%s*" % (botname,)

    r = requests.get("https://slack.com/api/im.list?token=%s" % (token,))
    j = json.loads(r.text)
    ims = {x['id']: users[x['user']] for x in j['ims']}

    r = requests.get("https://slack.com/api/channels.list?token=%s" % (token,))
    j = json.loads(r.text)
    channels = {x['id']: x['name'] for x in j['channels']}
    try:
        channel = "#%s" % (channels[msg['channel']],)
        LAST_CHANNEL = channel
    except KeyError:
        try:
            channel = ims[msg['channel']]
            LAST_CHANNEL = channel
        except KeyError:
            channel = LAST_CHANNEL

    with open("%s/%s" % (logdir, channel), 'a') as logfile:
        logfile.write("[%s] %s: %s\n" % (time.ctime(int(float((msg['ts'])))), user, msg['text']))
    return
