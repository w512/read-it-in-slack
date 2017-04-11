# Read it in slack

With this bot you can get and read all useful information in the one place – **Slack**.

Now it can:
1. Search for information in Twitter, and post the result to the chosen Slack channel.
2. Monitor the RSS feeds, and post the updates to the channel.
3. To look for the interesting photos at Flickr (by tag) and post it to the Slack.

### Installation

```console
$ git clone <github_clone_project_url>
$ cd <project_folder>
$ virtualenv --python=python3 --no-site-packages env
$ source ./env/bin/activate
$ pip install -r requirements.txt
```

### Run

1) put your keys and info to the local_settings.py
2) run bot:
```console
$ python bot.py
```

