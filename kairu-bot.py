# This guide helped me to understand the basics on how to make one: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

import time
import sys
from slackclient import SlackClient
from twitter import *

config = {}
execfile("config.py", config)

#bot's id 
BOT_ID = config["bot_id"]

# instantiate slack
# Note: always secure the api token
slack_client = SlackClient(config["slack_api"])

AT_BOT = "<@" + BOT_ID + ">"

# list of commands
EXAMPLE_COMMANDS = "help, retrieve, autoretrieve"
COMMANDS = ['help', 'retrieve', 'autoretrieve']

#constants
DEFAULT_INTERVAL = 5

def auto_retrieve(channel, start, default_interval):
	n = default_interval;
	response = "Starting...\n"
	time.sleep(3)
	response += "Will retrieve statuses from the infosec list every 1 hour. Auto Retrieve Intervals = "+str(DEFAULT_INTERVAL)+"\n"
	slack_client.api_call("chat.postMessage", channel=channel,
							  	text=response, as_user=True)
	while start and n > 0:
		response = retrieve()
		slack_client.api_call("chat.postMessage", channel=channel,
							  	text=response, as_user=True)
		n-=1
		# 3600 seconds = 1 hour
		time.sleep(3600)
	return "Auto retrieval stopped."

def retrieve():
	# will use this example on retrieving tweets https://github.com/ideoforms/python-twitter-examples/blob/master/twitter-home-timeline.py
	# config.py https://github.com/ideoforms/python-twitter-examples/blob/master/config.py
	response = ""
	response += "Retrieving 50 tweets... \n\n"

	users = [ "kylehalog" ]

	twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

	for user in users:
		result = twitter.lists.list(screen_name = user)
		for list in result:
			list_slug = list["slug"]
			list_str_id = list["id"]
			tweet_count = 50
			statuses = twitter.lists.statuses(slug = list_slug, list_id = list_str_id, count = tweet_count)
			for status in statuses:
				response += "(%s) @%s %s" % (status["created_at"], status["user"]["screen_name"], status["text"]) + "\n"
	return response

def command_handler(command, channel):

	response = "Sorry but I don't get what you mean. I can only understand these commands: " + EXAMPLE_COMMANDS
	if command in COMMANDS:
		if command == 'help':
			response = "\
			List of available commands: \n \
			help - display this message\n \
			retrieve - retrieve and output the latest tweets about infosec\n \
			autoretrieve - automatically retrieve and output tweets about infosec every 1 hour"
		
		elif command == 'retrieve':
			response = retrieve()

		elif command == 'autoretrieve':
			response = auto_retrieve(channel, True, DEFAULT_INTERVAL)
			
				
	slack_client.api_call("chat.postMessage", channel=channel,
						  text=response, as_user=True)
def slack_output_parser(rtm_output):
	
	output_list = rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			if output and 'text' in output and AT_BOT in output['text']:
				# return text after the @ mention, whitespace removed
				return output['text'].split(AT_BOT)[1].strip().lower(), \
					   output['channel']
	return None, None

if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1
	if slack_client.rtm_connect():
		print("Kairu Bot is connected and running!")
		while True:
			command, channel = slack_output_parser(slack_client.rtm_read())
			if command and channel:
				command_handler(command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection Failed. Invalid Slack token or Bot ID")


