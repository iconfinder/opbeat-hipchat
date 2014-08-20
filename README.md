# Opbeat for HipChat

Get Opbeat activity notifications into HipChat using the new Opbeat webhooks.


## Setup

1. Get a hold of a HipChat API v1 token ([Get it here](https://www.hipchat.com/admin/api), requires admin access) and the ID of the room where you want notifications to be posted ([Get it here](https://hipchat.com/rooms), click on a room and look for "API ID")

1. Press this button to create a new Heroku app:

    <a href="https://heroku.com/deploy" target="_blank">
        <img src="https://www.herokucdn.com/deploy/button.png" alt="Deploy">
    </a>

1. Add your token to the `HIPCHAT_AUTH_TOKEN` field and the room ID to the `HIPCHAT_ROOM_ID` field and deploy the app.
	
1. After deployment, click **"View it"** to open the new app and copy the hook url.

1. Go to `https://opbeat.com/<yourorg>/settings/` and enter the hook url.

Hooks are now configured. Post a comment on Opbeat to test it out!
