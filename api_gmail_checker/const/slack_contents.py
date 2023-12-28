def get_mail_arrive_slack_block(TIKTOK_URL, AUTHOR_UNIQUE_ID, EMAIL):
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

def get_mail_reply_slack_block(gmail_label_id, contents):
	return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*MAIL STATUS: {gmail_label_id}*"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*・ contents* : <{contents}>"
			}
		}
	]
