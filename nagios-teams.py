#!/usr/bin/env python

import requests
import json
import sys
import os
import jinja2

template_string = """ {
"type": "message",
"attachments": [ {
    "contentType":"application/vnd.microsoft.card.adaptive",
    "contentUrl":null,
    "content":{
        "type": "AdaptiveCard",
        "speak": "Host {{ name }} is DOWN",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "width": "auto",
                        "items": [
                            {
                                "type": "Image",
                                "url": "https://avatars.githubusercontent.com/u/5666660?s=200&v=4",
                                "width": "42px",
                                "height": "42px",
                                "altText": "Logo",
                                "targetWidth": "AtLeast:Standard",
                                "style": "RoundedCorners"
                                }
                            ],
                        "verticalContentAlignment": "Center"
                        },
                    {
                        "type": "Column",
                        "width": "stretch",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Host derp is DOWN",
                                "wrap": true,
                                "weight": "Bolder"
                                },
                            {
                                "type": "TextBlock",
                                "text": "Host derp",
                                "wrap": true
                                }
                            ],
                        "rtl": false
                        },
                    {
                        "type": "Column",
                        "width": "auto",
                        "items": [
                            {
                                "type": "Icon",
                                "name": "Warning",
                                "color": "Attention",
                                "style": "Filled",
                                "size": "Medium",
                                "horizontalAlignment": "Center"
                                }
                            ]
                        }
                    ],
    "style": "attention"
},
{
        "type": "ActionSet",
        "actions": [
            {
                "type": "Action.OpenUrl",
                "url": "https://adaptivecards.io/",
                "iconUrl": "icon:CheckmarkCircle",
                "style": "destructive"
                },
            {
                "type": "Action.Submit",
                "iconUrl": "icon:BookGlobe"
                },
            {
                "type": "Action.OpenUrl",
                "iconUrl": "icon:Eye"
                }
            ],
        "horizontalAlignment": "Left",
        "targetWidth": "AtLeast:Narrow"
        }
    ]
}
}]}"""


def send_teams_notification(webhook_url, title, message):
    headers = {
            "Content-Type": "application/json"
            }
    payload = {
            "type": "message",
            "attachments": [
                render_template("host")
                ]
            }

    # In Python 2, json.dumps() returns a str, which is what requests.post() expects for the 'data' argument.
    #response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
    response = requests.post(webhook_url, headers=headers, data=render_template(notificationtype="host"))

    if response.status_code != 202:
        # Python 2 print statement and using old-style string formatting
        print "Failed to send notification: %s, %s" % (response.status_code, response.text)
    else:
        # Python 2 print statement
        print "Notification sent successfully"


def render_template(notificationtype):

    # Create a Jinja2 environment
    env = jinja2.Environment()

    # Load a template from a string
    template = env.from_string(template_string)

    if notificationtype == "service":
        rendered_output = template.render(name="SERVICE")
    else:
        rendered_output = template.render(name="HOST")

    return rendered_output


if __name__ == "__main__":
    if len(sys.argv) != 4:
        # Python 2 print statement
        print "Usage: notify_teams.py <webhook_url> <title> <message>"
        sys.exit(1)

    webhook_url = 'https://defaultdbf7134bdfd84ceebeef8efc28559e.fa.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/f0e4c35569434129a35d4e4d373c1a33/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=VhyvrKsk4m4eWMlcKuOG1FfdhUmpOFcBBPoXKQboi3g'
    title = sys.argv[1]
    message = ' '.join(sys.argv)

    send_teams_notification(webhook_url, title, message)
