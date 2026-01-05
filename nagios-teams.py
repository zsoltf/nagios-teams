#!/usr/bin/env python

import argparse
import os
import urllib.request
import urllib.error
from string import Template

host_template_string = """ {
"type": "message",
"attachments": [ {
    "contentType":"application/vnd.microsoft.card.adaptive",
    "contentUrl":null,
    "content":

{
    "$$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "50px",
                    "items": [
                        {
                            "type": "Image",
                            "url": "https://avatars.githubusercontent.com/u/5666660?s=200&v=4",
                            "size": "Small",
                            "spacing": "None"
                        }
                    ],
                    "targetWidth": "AtLeast:Standard",
                    "spacing": "None"
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "spacing": "None",
                    "verticalContentAlignment": "Center",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "**$HOSTNAME** is **$HOSTSTATE**",
                            "spacing": "None",
                            "size": "Medium",
                            "style": "heading",
                            "wrap": true
                        },
                        {
                            "type": "TextBlock",
                            "text": "$HOSTOUTPUT",
                            "wrap": true,
                            "spacing": "None",
                            "targetWidth": "AtLeast:Narrow"
                        },
                        {
                            "type": "Container",
                            "items": [
                                {
                                    "type": "FactSet",
                                    "facts": [
                                        {
                                            "title": "Type",
                                            "value": "$NOTIFICATIONTYPE"
                                        },
                                        {
                                            "title": "Duration",
                                            "value": "$HOSTDURATION"
                                        },
                                        {
                                            "title": "Alias",
                                            "value": "$HOSTALIAS"
                                        },
                                        {
                                            "title": "Notes",
                                            "value": "$HOSTNOTES"
                                        }
                                    ]
                                }
                            ],
                            "id": "hide",
                            "isVisible": false,
                            "spacing": "ExtraSmall",
                            "bleed": true
                        }
                    ],
                    "bleed": true
                },
                {
                    "type": "Column",
                    "width": "32px",
                    "spacing": "None",
                    "items": [
                        {
                            "type": "Icon",
                            "name": "$iconname",
                            "spacing": "None",
                            "style": "Filled",
                            "horizontalAlignment": "Right",
                            "color": "$style"
                        }
                    ],
                    "verticalContentAlignment": "Top",
                    "horizontalAlignment": "Right",
                    "rtl": false,
                    "bleed": true
                }
            ],
            "spacing": "None",
            "style": "$style",
            "bleed": true,
            "selectAction": {
                "type": "Action.ToggleVisibility",
                "targetElements": [
                    "hide"
                ]
            }
        }
    ],
    "speak": "$HOSTNAME is $HOSTSTATE"
}

}]}"""

service_template_string = """ {
"type": "message",
"attachments": [ {
    "contentType":"application/vnd.microsoft.card.adaptive",
    "contentUrl":null,
    "content":

{
    "$$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "50px",
                    "items": [
                        {
                            "type": "Image",
                            "url": "https://avatars.githubusercontent.com/u/5666660?s=200&v=4",
                            "size": "Small",
                            "spacing": "None"
                        }
                    ],
                    "targetWidth": "AtLeast:Standard",
                    "spacing": "None"
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "spacing": "None",
                    "verticalContentAlignment": "Center",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "**$HOSTNAME**",
                            "wrap": true,
                            "spacing": "None",
                        },
                        {
                            "type": "TextBlock",
                            "text": "$SERVICEDESC is **$SERVICESTATE**",
                            "spacing": "None",
                            "size": "Medium",
                            "style": "heading",
                            "wrap": true
                        },
                        {
                            "type": "Container",
                            "items": [
                                {
                                    "type": "FactSet",
                                    "facts": [
                                        {
                                            "title": "Output",
                                            "value": "$SERVICEOUTPUT"
                                        },
                                        {
                                            "title": "Type",
                                            "value": "$NOTIFICATIONTYPE"
                                        },
                                        {
                                            "title": "Duration",
                                            "value": "$SERVICEDURATION"
                                        },
                                        {
                                            "title": "Notes",
                                            "value": "$SERVICENOTES"
                                        }
                                    ]
                                }
                            ],
                            "id": "hide",
                            "isVisible": false,
                            "spacing": "ExtraSmall",
                            "bleed": true
                        }
                    ],
                    "bleed": true
                },
                {
                    "type": "Column",
                    "width": "32px",
                    "spacing": "None",
                    "items": [
                        {
                            "type": "Icon",
                            "name": "$iconname",
                            "spacing": "None",
                            "style": "Filled",
                            "horizontalAlignment": "Right",
                            "color": "$style"
                        }
                    ],
                    "verticalContentAlignment": "Top",
                    "horizontalAlignment": "Right",
                    "rtl": false,
                    "bleed": true
                }
            ],
            "spacing": "None",
            "style": "$style",
            "bleed": true,
            "selectAction": {
                "type": "Action.ToggleVisibility",
                "targetElements": [
                    "hide"
                ]
            }
        }
    ],
    "speak": "$SERVICEDESC is $SERVICESTATE"
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


def send_teams_notification(args):

    # print args

    if args.alerttype == 'host':

        if args.notificationtype == 'ACKNOWLEDGEMENT':
            iconname = "CheckmarkSquare"
            style = "Good"
        elif args.hoststate == 'UP':
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

    elif args.alerttype == 'service':

        if args.notificationtype == 'ACKNOWLEDGEMENT':
            iconname = "CheckmarkSquare"
            style = "Good"
        elif args.servicestate == 'OK':
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

    webhook_url = os.getenv(args.channel, '')
    req = urllib.request.Request(webhook_url, data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')

    try:
        response = urllib.request.urlopen(req)
        print("Teams Response Status:", response.getcode())
    except urllib.error.URLError as e:
        print("Error sending request to Teams:", e.reason)


def render_template(templatetype, args, iconname, style):

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
                "iconname": iconname,
                "style": style
                }
        rendered_output = t.substitute(data)
    return rendered_output


def main():
    parser = argparse.ArgumentParser(description="nagios teams notification script")

    parser.add_argument('alerttype', type=str, help='alert type')
    parser.add_argument('channel', type=str, help='channel name')
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

    args = parser.parse_args()

    #load_env_file(env_path='/usr/local/etc/teams.env')
    load_env_file(env_path='.teams.env')
    send_teams_notification(args)


if __name__ == "__main__":
    main()
