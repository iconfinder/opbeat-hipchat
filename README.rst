Opbeat for HipChat
==================

Get Opbeat activity notifications into HipChat using the new Opbeat webhooks.


Setup
-----

1. Get a hold of your HipChat API v1 auth token (your group administrator needs to do this - see `Your API Access in HipChat <https://iconfinder.hipchat.com/account/api>`_) and the room ID where you want activity notifications to appear.
2. Create a new Heroku application.
3. Configure the application with your HipChat API key and room ID:

   ::

      $ heroku config:set HIPCHAT_AUTH_TOKEN=<auth token> HIPCHAT_ROOM_ID=<room ID>
4. Deploy!
5. ... wait for Opbeat to release so you can add the webhook.
