#!/usr/bin/env python

import argparse
import os
import sys
import urllib2
from string import Template

host_template_string = """ {
"type": "message",
"attachments": [ {
    "contentType":"application/vnd.microsoft.card.adaptive",
    "contentUrl":null,
    "content":

{
    "type": "AdaptiveCard",
    "speak": "Host $HOSTNAME is $HOSTSTATE",
    "$$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
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
                                    "text": "$HOSTNAME is $HOSTSTATE",
                                    "wrap": true,
                                    "weight": "Bolder"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "$HOSTOUTPUT",
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
                                    "name": "$iconname",
                                    "color": "$style",
                                    "style": "Filled",
                                    "size": "Medium",
                                    "horizontalAlignment": "Center",
                                    "selectAction": {
                                        "type": "Action.ToggleVisibility"
                                    }
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "$NOTIFICATIONTYPE",
                                    "wrap": true,
                                    "size": "Small",
                                    "fontType": "Monospace",
                                    "weight": "Bolder",
                                    "color": "Dark",
                                    "horizontalAlignment": "Center",
                                    "maxLines": 0
                                }
                            ],
                            "horizontalAlignment": "Center",
                            "targetWidth": "AtLeast:Narrow"
                        }
                    ],
                    "style": "$style",
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
                    "url": "$ACKURL"
                },
                {
                    "type": "Action.OpenUrl",
                    "iconUrl": "icon:Eye",
                    "url": "$DETAILURL"
                },
                {
                    "type": "Action.ShowCard",
                    "card": {
                        "type": "AdaptiveCard",
                        "$$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                        "body": [
                            {
                                "type": "FactSet",
                                "facts": [
                                    {
                                        "title": "Output",
                                        "value": "$HOSTOUTPUT"
                                    },
                                    {
                                        "title": "Duration",
                                        "value": "$HOSTDURATION"
                                    },
                                    {
                                        "title": "Notes",
                                        "value": "$HOSTNOTES"
                                    },
                                    {
                                        "title": "Alias",
                                        "value": "$HOSTALIAS"
                                    },
                                    {
                                        "title": "Type",
                                        "value": "$NOTIFICATIONTYPE"
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

service_template_string = """ {
"type": "message",
"attachments": [ {
    "contentType":"application/vnd.microsoft.card.adaptive",
    "contentUrl":null,
    "content":

{
    "type": "AdaptiveCard",
    "speak": "Service $HOSTNAME/$SERVICEDESC is $SERVICESTATE",
    "$$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
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
                                    "text": "$HOSTNAME/$SERVICEDESC is $SERVICESTATE",
                                    "wrap": true,
                                    "weight": "Bolder"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "$SERVICEOUTPUT",
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
                                    "name": "$iconname",
                                    "color": "$style",
                                    "style": "Filled",
                                    "size": "Medium",
                                    "horizontalAlignment": "Center",
                                    "selectAction": {
                                        "type": "Action.ToggleVisibility"
                                    }
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "$NOTIFICATIONTYPE",
                                    "wrap": true,
                                    "size": "Small",
                                    "fontType": "Monospace",
                                    "weight": "Bolder",
                                    "color": "Dark",
                                    "horizontalAlignment": "Center",
                                    "maxLines": 0
                                }
                            ],
                            "horizontalAlignment": "Center",
                            "targetWidth": "AtLeast:Narrow"
                        }
                    ],
                    "style": "$style",
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
                    "url": "$ACKURL"
                },
                {
                    "type": "Action.OpenUrl",
                    "iconUrl": "icon:Eye",
                    "url": "$DETAILURL"
                },
                {
                    "type": "Action.ShowCard",
                    "card": {
                        "type": "AdaptiveCard",
                        "$$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                        "body": [
                            {
                                "type": "FactSet",
                                "facts": [
                                    {
                                        "title": "Output",
                                        "value": "$SERVICEOUTPUT"
                                    },
                                    {
                                        "title": "Duration",
                                        "value": "$SERVICEDURATION"
                                    },
                                    {
                                        "title": "Notes",
                                        "value": "$SERVICENOTES"
                                    },
                                    {
                                        "title": "Type",
                                        "value": "$NOTIFICATIONTYPE"
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


def load_env_file(env_path=".env"):
    """
    Loads environment variables from a .env file into os.environ.
    """
    if not os.path.exists(env_path):
        print("Warning: .env file not found at %s" % env_path)
        return

    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Handle lines like KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
            else:
                pass


def send_teams_notification(webhook_url, alerttype, args):

    print args
    if alerttype == 'host':

        if args.hoststate == 'UP':
            iconname = "CheckmarkSquare"
            style = "Good"
        elif args.hoststate == 'DOWN':
            iconname = "Warning"
            style = "Attention"
        elif args.hoststate == 'UNREACHABLE':
            iconname = "QuestionCircle"
            style = "Warning"
        else:
            iconname = "QuestionCircle"
            style = "Accent"

        data = render_template(
                templatetype=args.alerttype,
                args=args,
                iconname=iconname,
                style=style
                )

    elif alerttype == 'service':

        if args.servicestate == 'OK':
            iconname = "CheckmarkSquare"
            style = "Good"
        elif args.servicestate == 'CRITICAL':
            iconname = "Warning"
            style = "Attention"
        elif args.servicestate == 'WARNING':
            iconname = "QuestionCircle"
            style = "Warning"
        elif args.servicestate == 'UNKNOWN':
            iconname = "QuestionCircle"
            style = "Emphasis"
        else:
            iconname = "QuestionCircle"
            style = "Accent"

        data = render_template(
                templatetype=args.alerttype,
                args=args,
                iconname=iconname,
                style=style
                )

    req = urllib2.Request(webhook_url, data)
    req.add_header('Content-Type', 'application/json')

    try:
        response = urllib2.urlopen(req)
        print "Teams Response Status:", response.getcode()
    except urllib2.URLError as e:
        print "Error sending request to Teams:", e.reason


def render_template(
        templatetype,
        args,
        iconname,
        style
        ):

    if templatetype == 'host':
        t = Template(host_template_string)
        data = {
                "HOSTNAME": args.hostname,
                "HOSTSTATE": args.hoststate,
                "NOTIFICATIONTYPE": args.notificationtype,
                "HOSTOUTPUT": args.hostoutput,
                "HOSTDURATION": args.hostduration,
                "HOSTNOTES": args.hostnotes,
                "HOSTALIAS": args.hostalias,
                "ACKURL": args.ackurl,
                "DETAILURL": args.detailurl,
                "iconname": iconname,
                "style": style
                }
        rendered_output = t.substitute(data)
    elif templatetype == 'service':
        t = Template(service_template_string)
        data = {
                "HOSTNAME": args.hostname,
                "SERVICEDESC": args.servicedesc,
                "SERVICESTATE": args.servicestate,
                "SERVICEOUTPUT": args.serviceoutput,
                "NOTIFICATIONTYPE": args.notificationtype,
                "SERVICEDURATION": args.serviceduration,
                "SERVICENOTES": args.servicenotes,
                "ACKURL": args.ackurl,
                "DETAILURL": args.detailurl,
                "iconname": iconname,
                "style": style
                }
        rendered_output = t.substitute(data)
    return rendered_output


def main():
    parser = argparse.ArgumentParser(description="nagios teams notification script")

    parser.add_argument('-c', '--channel', type=str, help='channel name')
    parser.add_argument('-t', '--alerttype', type=str, default='host', help='alert type')
    parser.add_argument('--hostname', type=str, help='hostname')
    parser.add_argument('--hoststate', type=str, help='hoststate')
    parser.add_argument('--notificationtype', type=str, help='notificationtype')
    parser.add_argument('--hostoutput', type=str, help='hostoutput')
    parser.add_argument('--hostduration', type=str, help='hostduration')
    parser.add_argument('--hostnotes', type=str, help='hostnotes')
    parser.add_argument('--hostalias', type=str, help='hostalias')
    parser.add_argument('--servicedesc', type=str, help='servicedesc')
    parser.add_argument('--servicestate', type=str, help='servicestate')
    parser.add_argument('--serviceoutput', type=str, help='serviceoutput')
    parser.add_argument('--serviceduration', type=str, help='serviceduration')
    parser.add_argument('--servicenotes', type=str, help='servicenotes')
    parser.add_argument('--ackurl', type=str, help='ackurl')
    parser.add_argument('--detailurl', type=str, help='detailurl')

    args = parser.parse_args()

    load_env_file(env_path='.teams.env')
    webhook_url = os.getenv(args.channel)
    send_teams_notification(webhook_url, args.alerttype, args)


if __name__ == "__main__":
    main()
