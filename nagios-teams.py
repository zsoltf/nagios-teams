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
    "content":

{
    "type": "AdaptiveCard",
    "speak": "Host {{ HOSTNAME }} is {{ HOSTSTATE }}",
    "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.5",
    "body": [
        {
            "type": "Container",
            "items": [
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "50px",
                            "verticalContentAlignment": "Center",
                            "items": [
                                {
                                    "type": "Image",
                                    "url": "https://avatars.githubusercontent.com/u/5666660?s=200&v=4"
                                }
                            ],
                            "targetWidth": "AtLeast:Standard"
                        },
                        {
                            "type": "Column",
                            "width": "stretch",
                            "rtl": false,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "{{ HOSTNAME }} is {{ HOSTSTATE }}",
                                    "wrap": true,
                                    "weight": "Bolder"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "{{ HOSTOUTPUT }}",
                                    "wrap": true,
                                    "targetWidth": "AtLeast:Narrow"
                                }
                            ]
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
                                    "horizontalAlignment": "Center",
                                    "selectAction": {
                                        "type": "Action.ToggleVisibility"
                                    }
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "{{ NOTIFICATIONTYPE }}",
                                    "wrap": true,
                                    "size": "Small",
                                    "fontType": "Monospace",
                                    "weight": "Bolder",
                                    "color": "Dark",
                                    "horizontalAlignment": "Center",
                                    "maxLines": 0
                                }
                            ],
                            "horizontalAlignment": "Center"
                        }
                    ],
                    "style": "attention",
                    "spacing": "None"
                }
            ],
            "horizontalAlignment": "Center",
            "style": "default"
        },
        {
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.OpenUrl",
                    "iconUrl": "icon:CheckmarkCircle",
                    "style": "destructive",
                    "url": "{{ ACKURL }}"
                },
                {
                    "type": "Action.OpenUrl",
                    "iconUrl": "icon:Eye",
                    "url": "{{ DETAILURL }}"
                },
                {
                    "type": "Action.ShowCard",
                    "card": {
                        "type": "AdaptiveCard",
                        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                        "body": [
                            {
                                "type": "FactSet",
                                "facts": [
                                    {
                                        "title": "Output",
                                        "value": "{{ HOSTOUTPUT }}"
                                    },
                                    {
                                        "title": "Duration",
                                        "value": "{{ HOSTDURATION }}"
                                    },
                                    {
                                        "title": "Notes",
                                        "value": "{{ HOSTNOTES }}"
                                    },
                                    {
                                        "title": "Alias",
                                        "value": "{{ HOSTALIAS }}"
                                    },
                                    {
                                        "title": "Type",
                                        "value": "{{ NOTIFICATIONTYPE }}"
                                    }
                                ]
                            }
                        ],
                        "speak": "Details"
                    },
                    "iconUrl": "icon:ChevronDown"
                }
            ],
            "horizontalAlignment": "Left",
            "targetWidth": "AtLeast:Narrow"
        }
    ],
    "verticalContentAlignment": "Center",
    "minHeight": "0px"
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
