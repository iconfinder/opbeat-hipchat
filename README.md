# Opbeat for HipChat

[![Build status](https://travis-ci.org/iconfinder/opbeat-hipchat.svg?branch=master)](https://travis-ci.org/iconfinder/opbeat-hipchat)

Get Opbeat activity notifications into HipChat using the new Opbeat webhooks.


## Setup

1. Get a hold of a HipChat API v2 token ([if you don't have one, you can create it under your API access settings](https://hipchat.com/account/api)) and the ID of the room where you want notifications to be posted ([get it here](https://hipchat.com/rooms), click on a room and look for "API ID")

1. Press this button to create a new Heroku app:

    <a href="https://heroku.com/deploy" target="_blank">
        <img src="https://www.herokucdn.com/deploy/button.png" alt="Deploy">
    </a>

1. Add your token to the `HIPCHAT_AUTH_TOKEN` field and the room ID to the `HIPCHAT_ROOM` field and deploy the app.
	
1. After deployment, click **"View it"** to open the new app and copy the hook URL.

1. Go to `https://opbeat.com/<yourorg>/settings/` and enter the hook url.

Hooks are now configured. Post a comment on Opbeat to test it out!
