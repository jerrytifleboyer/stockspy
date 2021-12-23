import requests
import json

with open('config/pw.json') as f:
    data = json.load(f)
    channel = data["discord"]["channel"]
    auth = data["discord"]["auth"]

def ping_me_on_discord(content):

     requests.post(channel, data={"content":content}, headers={"authorization":auth})

if __name__=="__main__":
    ping_me_on_discord()