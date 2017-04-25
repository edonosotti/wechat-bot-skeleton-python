# WeChat Bot Skeleton - Python version

## Introduction

A WeChat (and Weixin) chatbot skeleton in Python with queue/delayed messages support.

This application was written following up on the [**Building Chatbots For WeChat — Part #1**](https://chatbotsmagazine.com/building-chatbots-for-wechat-part-1-dba8f160349) article and in anticipation of Part #2.

## Running locally

Clone the repository and enter the directory:

Install the required dependencies running the following command from the project root:

```
$ pip install -r requirements.txt
```

Run the bot:

```
$ gunicorn -b 127.0.0.1:8000 src.bot
```

Read the [**Building Chatbots For WeChat — Part #1**](https://chatbotsmagazine.com/building-chatbots-for-wechat-part-1-dba8f160349) article to learn how to setup the bot on WeChat and use tunneling tools such as [`ngrok`](https://ngrok.com) in case you don't have a public IP address.

Run the queue worker:

```
$ python src/worker.py
```

## Deploying on Heroku

In case you are not familiar with the Heroku platform, please read the [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python) article first.

Add a new `git` remote pointing to the Heroku repository:

```
$ heroku git:remote -r heroku -a {HEROKU_APP_NAME}
```

Push the code repository to Heroku:

```
$ git push heroku master
```

Get the app URL:

```
$ heroku info -a {HEROKU_APP_NAME}
```
