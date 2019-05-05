#!/usr/bin/env python3
import os
import sys
import json
import time
import datetime
import configparser
from twython import Twython
from etnawrapper import EtnaWrapper

def tweet_message(etna_message):
        CONSUMER_KEY = ''
        CONSUMER_SECRET = ''
        ACCESS_KEY = ''
        ACCESS_SECRET = ''

        # tweet
        tweet = "@user " + etna_message

        api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

        api.update_status(status=tweet)

def grab_latests_messages(data):
        message_id = "message_id.txt"
        count = 0
        with open(message_id, 'r') as file :
                current_id = file.readline()

        for i in range(0, 8):
                if current_id != str(data[i]["id"]): # + "\n" :
                        tweet_message(data[i]["message"])
                        time.sleep(1)
                else:
                        break

                count += 1

        if count != 0 :
                with open(message_id, 'w') as f:
                        f.write(str(data[0]["id"]))
        return count

if __name__ == '__main__':
        ini = configparser.ConfigParser()
        ini.read('config.ini')

        etna_id = ini['ETNA']['etna_id']
        etna_passwd = ini['ETNA']['etna_password']

        wrapper = EtnaWrapper(login=etna_id, password=etna_passwd)

        # grab notifications and write to file.json
        with open("file.json", 'w') as file :
                file.write(json.dumps(wrapper.get_notifications(), indent=4))

        with open("file.json") as f:
                json_data = json.load(f)

                cnt = grab_latests_messages(json_data)

        # log part
        now = str(datetime.datetime.now())
        now = now.split('.')[0]

        with open("twitna.log", 'a') as log:
                for i in range(0, cnt) :
                        log.write(now + " : " + str(json_data[i]["message"].encode('utf-8')) + "\n")

        os.remove("file.json")
