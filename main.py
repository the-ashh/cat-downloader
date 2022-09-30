import secrets
import tweepy
import wget
import os
import re
import telebot

output_dir = "cat"

twitter_auth = tweepy.OAuth1UserHandler(
    secrets.twitter_api_key, secrets.twitter_secret_key, secrets.twitter_access_key, secrets.twitter_access_secret
)

twitter_api = tweepy.API(twitter_auth)

bot = telebot.TeleBot(secrets.telegram_secret_key, parse_mode=None)

def get_media_link(id):
    tweet = twitter_api.get_status(id)._json
    
    return(tweet['entities']['media'][0]['media_url'])

def download_and_sort_cat(url, output):
    download_name = wget.download(url, output)
    file_extension = os.path.splitext(download_name)[1]
    files = os.listdir(output)
    count = 0
    for i in files:
        count += 1
    os.rename(download_name, output + "/" + output + "_" + str(count) + file_extension)
    return(output + "_" + str(count) + file_extension)

def get_tweet_id(url):
    return re.findall(r"https:\/\/twitter\.com\/[\w\d_]+\/status\/(\d+)", url)[0]

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "hi!! if ur not me, you're not gonna get any use outta this. have a wonderful day :D")

@bot.message_handler(commands=['help'])
def help(message):
	bot.reply_to(message, "if u need to type /help, this bot is not for u, srry bestie <3")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if not message.from_user.id == 316283832:
        bot.reply_to(message, "srry bestie, this bot is not for you <3")
        return
    
    if "https://twitter.com" in message.text:
        tweet_id = get_tweet_id(message.text)
        tweet_media_link = get_media_link(tweet_id)
        cat_name = download_and_sort_cat(tweet_media_link, output_dir)
        bot.reply_to(message, "downloaded the cat as " + cat_name + ". enjoy :D")
    else:
        bot.reply_to(message, "not a twitter link, sorry D:")

bot.infinity_polling()