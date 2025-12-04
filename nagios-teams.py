#!/usr/bin/env python

import requests
import json
import sys
import os

def send_teams_notification(webhook_url, title, message):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": title,
                            "weight": "bolder",
                            "size": "medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": message,
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }

    # In Python 2, json.dumps() returns a str, which is what requests.post() expects for the 'data' argument.
    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

    if response.status_code != 202:
        # Python 2 print statement and using old-style string formatting
        print "Failed to send notification: %s, %s" % (response.status_code, response.text)
    else:
        # Python 2 print statement
        print "Notification sent successfully"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        # Python 2 print statement
        print "Usage: notify_teams.py <webhook_url> <title> <message>"
        sys.exit(1)

    webhook_url = 'https://defaultdbf7134bdfd84ceebeef8efc28559e.fa.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/f0e4c35569434129a35d4e4d373c1a33/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=VhyvrKsk4m4eWMlcKuOG1FfdhUmpOFcBBPoXKQboi3g'
    title = sys.argv[1]
    message = ' '.join(sys.argv)

    send_teams_notification(webhook_url, title, message)
