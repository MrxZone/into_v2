# Install the Python Requests library:
# `pip install requests`

import json
import time

import requests


def send_request(msg):
    # Request (7)
    # POST https://a1.easemob.com/1119230224168508/demo/messages/chatgroups

    try:
        response = requests.post(
            url="https://a1.easemob.com/1119230224168508/demo/messages/chatgroups",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer YWMtp92LhNd2Ee2pAEv6eFNHRwBWFZH0izWrhUh0KF416BU_f9Rq_X5EzIbAMVEh--hkAgMAAAGHajQhfjeeSAAeCmA7TBY6MjIu96H-qqat1dx81QD0lTZJuiy1hpSCYg",
                "Cookie": "SERVERID=24a574e15eb2f57eee1ce475fd6cd454|1681645331|1681645331",
            },
            data=json.dumps({
                "body": {
                    "msg": msg,
                    "type": "txt",
                    "sync_device": True
                },
                "to": [
                    "211518964695044"
                ],
                "type": "txt",
                "from": "8618710032776"
            })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


if __name__ == "__main__":
    for i in range(30):
        time.sleep(2)
        send_request(f"两秒一句话-{i}")
