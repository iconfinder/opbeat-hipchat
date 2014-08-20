# Opbeat for HipChat

Get Opbeat activity notifications into HipChat using the new Opbeat webhooks.


## Setup

1. Get a hold of a HipChat API v1 token ([Get it here](https://www.hipchat.com/admin/api), requires admin access) and the ID of the room where you want notifications to be posted ([Get it here](https://hipchat.com/rooms), click on a room and look for "API ID")

1. Create a new Heroku application.
1. Configure the application with your HipChat API key and room ID:

		$ heroku config:set HIPCHAT_AUTH_TOKEN=<auth token> HIPCHAT_ROOM_ID=<room ID>
	
1. Deploy!
1. Set the hook target in your organization settings on Opbeat to:

		http://<your Heroku application's URL>/new-activity
