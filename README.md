[![Build Status](https://travis-ci.org/edonosotti/wechat-bot-skeleton-python.svg?branch=master)](https://travis-ci.org/edonosotti/wechat-bot-skeleton-python)
[![Code Climate](https://codeclimate.com/github/edonosotti/wechat-bot-skeleton-python/badges/gpa.svg)](https://codeclimate.com/github/edonosotti/wechat-bot-skeleton-python)

# WeChat Bot Skeleton - Python version

## Introduction

A WeChat (and Weixin) chatbot skeleton in Python with queue/delayed messages support.

This application was written following up on the [**Building Chatbots For WeChat — Part #1**](https://chatbotsmagazine.com/building-chatbots-for-wechat-part-1-dba8f160349) article and in anticipation of Part #2.

## Configuration

In order to successfully run this application, the following environment variables must be set:

| Variable name      | Description                                                                      |
|--------------------|----------------------------------------------------------------------------------|
| `REDIS_URL`        | A Redis connection string.                                                       |
| `WECHAT_TOKEN`     | See: [WeChat docs](http://admin.wechat.com/wiki/index.php?title=Getting_Started) |
| `WECHAT_APPID`     | Provided by the WeChat admin console.                                            |
| `WECHAT_APPSECRET` | Provided by the WeChat admin console.                                            |

When running the application on the local machine for testing, a `.env` can be used instead of environment variables. See **Running locally** for details.

## Running locally

Ensure that a working instance of Redis is available, either on the local machine or on a remote server.

Clone the repository and enter the directory:

Install the required dependencies running the following command from the project root:

```
$ pip install -r requirements.txt
```

Rename the `.env.template` file to `.env`, edit it and set the required parameters.
Alternatively, set the environment variables listed in `.env.template`.
The `.gitignore` file is already configured to ignore the `.env` file upon commits and pushes.

Run the bot:

```
$ gunicorn -b 127.0.0.1:8000 src.bot
```

then configure WeChat to forward messages to it. The [**Building Chatbots For WeChat — Part #1**](https://chatbotsmagazine.com/building-chatbots-for-wechat-part-1-dba8f160349) article contains information on how to setup the bot on WeChat and use tunneling tools such as [`ngrok`](https://ngrok.com) in case a public IP address to connect the server to the local machine is not available.

Set up a cron job to run the queue worker automatically, or do it manually when needed during development and testing:

```
$ python src/worker.py
```

## Deploying to Heroku

*In case you are not familiar with the Heroku platform, please read the [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python) article first.*

Ensure that the [`Heroku CLI`](https://devcenter.heroku.com/articles/heroku-cli) is installed and configured with the proper credentials, then create a new app on Heroku to host the bot code.

Provision the required [`Heroku Redis`](https://elements.heroku.com/addons/heroku-redis) and [`Heroku Scheduler`](https://elements.heroku.com/addons/scheduler) add-on elements:

```
$ heroku addons:create heroku-redis:hobby-dev -a {HEROKU_APP_NAME}
$ heroku addons:create scheduler:standard -a {HEROKU_APP_NAME}
```

This applications has been also tested with [`Redis Cloud`](https://elements.heroku.com/addons/rediscloud).

Set all the required environment variables:

```
$ heroku config:set REDIS_URL="redis://{USERNAME}:{PASSWORD}@{HOST}:{PORT"" -a {HEROKU_APP_NAME}
$ heroku config:set WECHAT_TOKEN={WECHAT_SHARED_TOKEN} -a {HEROKU_APP_NAME}
$ heroku config:set WECHAT_APPID={WECHAT_APP_ID} -a {HEROKU_APP_NAME}
$ heroku config:set WECHAT_APPSECRET={WECHAT_APP_SECRET} -a {HEROKU_APP_NAME}
```

`Heroku Redis` automatically sets the `REDIS_URL` variable, it might be necessary to set it when using different Redis add-ons.

Enter the project root and add a new `git` remote pointing to the Heroku repository (see also: [Creating a Heroku remote](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote)):

```
$ heroku git:remote -r heroku -a {HEROKU_APP_NAME}
```

Push the code repository to Heroku:

```
$ git push heroku master
```

*For more information about deplyoing to Heroku with Git, see: [Deploying with Git](https://devcenter.heroku.com/articles/git)*

Get the app URL:

```
$ heroku info -a {HEROKU_APP_NAME}
```

then configure WeChat to forward messages to it as described in **Running locally**.

## Tests

This application uses [`pytest`](https://pytest.org). Run:

```
$ pytest
```

from the project root to run tests.

**WARNING**

The Queue Manager implements the FIFO pattern, so in order for tests to succeed, they MUST be ran against a private Redis instance where no other processes are running I/O operations. Otherwise, another process could alter the queue by pushing and pulling other messages, thus making the test fail.

You can specify a different Redis connection string at runtime:

```
$ REDIS_URL={test_redis_instance_URL} pytest
```
