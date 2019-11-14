#!/bin/python3

'''
This python script is called in Jenkins, takes payload as input and
checks if there is a PR merge event
'''
import os
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

JSON_STR = ''

HOOK_URL = "https://hooks.slack.com/services/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"
#HOOK_URL = "https://hooks.slack.com/services/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"


def send_slack_msg(reponame, prlink, prdescription):
    '''
    :param reponame:
    :param prlink:
    :param prdescription:
    :return: none
    '''
    print("sending message...")
    slack_message = {
        "attachments": [
            {
                "color": "#36a64f",
                "pretext": "PR Merge Notification - {}".format(reponame),
                "title": prdescription,
                "text": prlink
            }
        ]
    }

    req = Request(HOOK_URL, json.dumps(slack_message).encode("utf8"))

    try:
        response = urlopen(req)
        response.read()
    except HTTPError as err_obj:
        print("Request failed : %d %s", err_obj.code, err_obj.reason)
    except URLError as err_obj:
        print("Server connection failed: %s", err_obj.reason)


try:
    os.environ['payload']
except KeyError:
    JSON_STR = None

if JSON_STR is None:
    print("No payload available")
else:
    JSON_STR = os.environ['payload']
    JSON_DICT = json.loads(JSON_STR)

    if JSON_DICT['pull_request']['merged']:
        REPO_NAME = JSON_DICT['pull_request']['head']['repo']['full_name']
        FEATURE_BRANCH = JSON_DICT['pull_request']['head']['ref']
        HTML_URL = JSON_DICT['pull_request']['html_url']
        PR_URL = "PR: {}".format(HTML_URL)
        PR_DESCRIPTION = JSON_DICT['pull_request']['title']
        MAIN_BRANCH = JSON_DICT['pull_request']['base']['ref']
        send_slack_msg(REPO_NAME, PR_URL, PR_DESCRIPTION)
