import logging
logging.basicConfig(level=logging.DEBUG)

import os
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

#Get Config from json file
with open("./config.json", "r") as f:
    config = json.load(f)
    slack_token = config.get("slack_token", os.environ.get("SLACK_BOT_TOKEN")) 

channel_ids = ["YOUR_CHANNEL_HERE"]

client = WebClient(token=slack_token)
for i in range(len(channel_ids)):
    conversation_history = []
    channel_id = channel_ids[i]
    try:
        result = client.conversations_history(channel=channel_id, limit=100)
        conversation_history = result["messages"]
        #print("{} messages found in {}".format(len(conversation_history), channel_id))
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'

    with open("./conversation_history.json", "w") as f:
        json.dump(conversation_history, f, indent=4)
    with open("./conversation_history.json", "r") as f:
        conv2dataset = json.load(f)
        dataset = []  
        for x in range(len(conv2dataset)):
            text = conv2dataset[x].get("text", "NOTEXT")
            print(text)
            try:
                data = {
                    "input": text,
                    "output": conv2dataset[x+1].get("text", "NOTEXT"),
                }
                dataset.append(data)
            except IndexError as e:
                data = {
                    "input": text,
                    "output": conv2dataset[0].get("text", "NOTEXT"),
                }
                dataset.append(data)
        
        with open("./dataset.json", "w") as f:
            json.dump(dataset, f, indent=4)
