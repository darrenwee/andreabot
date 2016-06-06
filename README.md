# andreabot

Every FOP director's favorite assistant! A Telegram bot to assist announcement and news dissemination to all important people like COGLs and VOGLs.

## Requirements
`pyTelegramBotAPI`
`python3`

## Deployment
Ensure that your Telegram bot API token is inside `settings_secret.py`. Use `settings_secret_example.py` to insert the token.

```python
    python3 andreabot.py
```

## Supported Functions
| Command         | Description                                                                  |
|-----------------|------------------------------------------------------------------------------|
| /yell `message` | Sends `message` to all users on the mailing list.                            |
| /time           | Returns the bot server's current time and date.                              |
| /log            | Returns at most the 5 most recent announcements made in chronological order. |
|                 |                                                                              |
