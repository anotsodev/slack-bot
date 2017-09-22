############################################################
# api-token - 
# (before publishing this bot, please remove the api token)
############################################################
# slack bot features:
# 1. list all articles about infosec every 1 hour
# 2. available list of helpful commands
# for now, i will do the first feature of the slack bot.
############################################################

from slackclient import SlackClient

BOT_NAME = 'kairu-bot'

slack_client = SlackClient('')

if __name__ == "__main__":
	api_call = slack_client.api_call("users.list")
	if api_call.get('ok'):
		# retrieve all users so we can find our bot
		users = api_call.get('members')
		for user in users:
			if 'name' in user and user.get('name') == BOT_NAME:
				print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
	else:
		print("Could not find user " + BOT_NAME)