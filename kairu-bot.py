#
# This is my first time to write a slack bot in python. This guide helped me to
# understand the basics on making one: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
#

import time
from slackclient import SlackClient

#bot's id 
BOT_ID = ''

# instantiate slack
# always secure the api token
slack_client = SlackClient('')

AT_BOT = "<@" + BOT_ID + ">"

# list of commands
EXAMPLE_COMMANDS = "help, retrieve, autoretrieve"
COMMANDS = ['help', 'retrieve', 'autoretrieve']


def command_handler(command, channel):

	response = "Sorry but I don't get what you mean. I can only understand these commands: " + EXAMPLE_COMMANDS
	if command in COMMANDS:
		#response = "Sure...write some more code then I can do that!"
		if command == 'help':
			response = "\
			List of available commands: \n \
			help - display this message\n \
			retrieve - retrieve and output the latest tweets about infosec\n \
			autoretrieve - automatically retrieve and output tweets about infosec every after 1 hour"
	
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


