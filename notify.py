#!/usr/bin/env python3
import os
import sys
import json
import time
import configparser
import notify2
import datetime
from etnawrapper import EtnaWrapper

def grab_latests_messages(data):
	message_id = "message_id.txt"
	count = 0

	exists = os.path.isfile(message_id)

	if exists :
		with open(message_id, 'r') as f :
			current_id = f.readline()
	else:
		with open(message_id, 'w') as f :
			current_id = str(data[0]["id"]) + "\n"
			f.write(str(current_id) + "\n")
		return 0

	notify2.init('ETNA')
	for i in range(0, len(data)):
		if current_id != str(data[i]["id"]) + "\n" :
			# tweet message and time from json file
			n = notify2.Notification('ETNA', data[i]["message"])
			n.show()
			time.sleep(1)
		else:
			break

		count += 1

	if count != 0 :
		with open(message_id, 'w') as f:
			f.write(str(data[0]["id"]) + "\n")
	return count

if __name__ == '__main__':

	if len(sys.argv) == 2:
		if sys.argv[1] == "test" :
			notify2.init('ETNA')
			n = notify2.Notification('ETNA', "this is a test")
			n.show()
			sys.exit(0)

	ini = configparser.ConfigParser()
	ini.read('config.ini')

	etna_id = ini['ETNA']['etna_id']
	etna_passwd = ini['ETNA']['etna_password']
	
	wrapper = EtnaWrapper(login=etna_id, password=etna_passwd)
	
	json_file = "/tmp/etna_notif.json"

	# grab notifications and write to file	.json
	with open(json_file, 'w') as file :
		file.write(json.dumps(wrapper.get_notifications(), indent=4))

	with open(json_file, 'r') as f:
		json_data = json.load(f)

		cnt = grab_latests_messages(json_data)

	# log part
	now = str(datetime.datetime.now())
	now = now.split('.')[0]

	with open("notify.log", 'a') as log:
		for i in range(0, cnt) :
			log.write(now + " : " + str(json_data[i]["message"].encode('utf-8')) + "\n")

	os.remove(json_file)

