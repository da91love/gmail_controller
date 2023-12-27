def get_formatted_block(TIKTOK_URL, AUTHOR_UNIQUE_ID, EMAIL):
	return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Coversation with <{TIKTOK_URL}|{AUTHOR_UNIQUE_ID}> is started!*"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*・ Influence name* : <{TIKTOK_URL}|{AUTHOR_UNIQUE_ID}>"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*・ Mail address* : {EMAIL}"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*・ Status* : *CONTACT NECESSARY* 🔴"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*・ Person In Charge* : "
			}
		}
	]
