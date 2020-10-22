# install praw, tweepy, flask, flask_pymongo, and dns python
# eg: pip install praw

# importing the libraries
import praw
import tweepy
from flask import Flask, request, redirect
from flask import render_template
from flask_pymongo import PyMongo

# defining our app
app = Flask(__name__)
# configuring our app with database named SocialMedia
app.config['MONGO_DBNAME'] = "SocialMedia"
# providing the uri of the mongodb database
app.config['MONGO_URI'] = "mongodb+srv://admin:admin@cluster0.hyop8.mongodb.net/SocialMedia?retryWrites=true&w=majority"
# creating mongo instance to initialize connectio
mongo = PyMongo(app)

# this is our main page of the website. There are two buttons which take user to two different webpages
@app.route('/', methods=['GET','POST'])
def showHome():
    return render_template('index.html')

@app.route('/twitter', methods=['GET','POST'])
def twitter():
    if request.method == 'POST':
        message = request.form['message']
        twitter = tweepy.OAuthHandler("nt2GwMJE4sr9OfQi27lnx8PK4", "q2Q4Lnz2btFWrskC4DmFZ7wKpA8F5WHMiFgPATcJgiGhTRnwNp")
        twitter.set_access_token("1318043042843140099-zEjxmIcnDfHCxhkGRm1T43ojIaDMna",
                                 "4k9fESfsu6PbpJaX88s8n1tZjblR91jeR59cGd4d6E6NY")
        api = tweepy.API(twitter)
        api.update_status(message)
        return redirect("/")
    return render_template('tweet.html')

@app.route('/reddit', methods=['GET','POST'])
def reddit():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        reddit = praw.Reddit(client_id="Alp04H02rA1JMg", client_secret="RMn4Cp4-Id0y-c7x35cUZvSXJQI", password="Shona1107", user_agent="webapp", username="sonalijain96")
        sub = reddit.subreddit("u_sonalijain96")
        sub.submit(title, message)
        return redirect("/")
    return render_template('reddit.html')

# This function will first get reddit credentials, fetches all the posts and stores in to mongodb db under reddit table
def fetchandPostToRedditPosts():
    reddit = praw.Reddit(client_id="Alp04H02rA1JMg", client_secret="RMn4Cp4-Id0y-c7x35cUZvSXJQI", password="Shona1107", user_agent="webapp", username="sonalijain96")
    array = []
    collection = mongo.db.reddit
    collection.remove({})
    for submission in reddit.redditor("sonalijain96").submissions.new():
        array.append({'id': submission.id, 'Title': submission.title, 'Name': submission.author.name, 'Text': submission.selftext })
    collection.insert_many(array)
    return array

# This function will first get twitter credentials, fetches all the posts and stores in to mongodb db under twitter table
def fetchandPostToTwitterPosts():
    twitter = tweepy.OAuthHandler("nt2GwMJE4sr9OfQi27lnx8PK4", "q2Q4Lnz2btFWrskC4DmFZ7wKpA8F5WHMiFgPATcJgiGhTRnwNp")
    twitter.set_access_token("1318043042843140099-zEjxmIcnDfHCxhkGRm1T43ojIaDMna", "4k9fESfsu6PbpJaX88s8n1tZjblR91jeR59cGd4d6E6NY")
    api = tweepy.API(twitter)
    array = []
    collection = mongo.db.twitter
    collection.remove({})

    response = api.user_timeline(screen_name="SonaliJ51170872", count=100, include_rts=True)
    for tweet in response:
        array.append({'id': tweet.id, 'Text': tweet.text, 'Name': tweet.user.name, 'screenName': tweet.user.screen_name })
    collection.insert_many(array)
    print(array)
    return array

if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
