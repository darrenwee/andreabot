# andreabot

Every FOP director's favorite assistant! A Telegram bot to assist announcement and news dissemination to all important people like COGLs and VOGLs.

## Requirements
`telepot`

`python3`

`pymongo` and MongoDB

## Deployment
1. Ensure that your Telegram bot API token is inside `settings_secret.py`. Use `settings_secret_example.py` to insert the token.

2. Ensure that the `mongod` daemon is listening. The DB connection settings are stored in `manager.py`.

3. Start the bot by running
```
python3 andreabot.py
```

## Supported Commands
(This is a list of Telegram commands)

| Command         | Description                                                                  |
|-----------------|------------------------------------------------------------------------------|
| /yell `message` | Sends `message` to all users on the mailing list.                            |
| /time           | Returns the bot server's current time and date.                              |
| /log            | Returns at most the 5 most recent announcements made in chronological order. |
| /vlog `n`       | Returns the `n` most recent announcements made in chronological order.       |
| /name `name`    | Tells me that you are `name`.                                                |
| /who            | Returns a list of people who are currently listening to /yell and list of groups |
