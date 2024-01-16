import praw
import tweepy
import pyimgur
import urllib.request
import os
from time import sleep
import datetime
import requests
import json
from redvid import Downloader

reddit = praw.Reddit(user_agent,
                     client_id,
                     client_secret)

auth = tweepy.OAuthHandler(password, password)
auth.set_access_token(another password, another password)
twitter = tweepy.API(auth)
twitter2 = tweepy.Client(more_passwords,
                         more_passwords,
                         more_passswords,
                         more_passwords,
                         more_passwords
                         )

imgur = pyimgur.Imgur(so_many_passwords,  so_many_passwords)

#hmmm or maybemaybemaybe
subreddit = reddit.subreddit("BlackPeopleTwitter")
posts = 0
loops = 0
with open("previous_posts.txt", "r") as f:
    contents = f.readlines()
while True:
    for submission in subreddit.new(limit=1):
        title = submission.title

        if submission.id + "\n" not in contents:
            medias_ids = []
            if submission.is_video:
                link = submission.secure_media["reddit_video"]["hls_url"]
                downloader = Downloader(max_q=True, filename="video")
                downloader.url = submission.url
                downloader.download()

                media = twitter.media_upload(r"C:\Users\Owner\PycharmProjects\Black_People_Twitter_Bot\video.mp4")
                medias_ids.append(media.media_id_string)

                with open("previous_posts.txt", "a") as f:
                    f.write(submission.id + "\n")
                with open("previous_posts.txt", "r") as f:
                    contents = f.readlines()

                twitter2.create_tweet(text=submission.title, media_ids=medias_ids)
                print("new post")
                posts += 1
                os.remove("video.mp4")
            else:
                media_links = []
                if "gallery_data" in vars(submission):
                    for item in submission.gallery_data["items"]:
                        media_links.append(submission.media_metadata[item["media_id"]]["p"][-1]["u"])
                else:
                    media_links.append(submission.url)

                for i, link in enumerate(media_links):
                    media_bytes = urllib.request.urlopen(link)
                    with open(str(i), "wb") as f:
                        f.write(media_bytes.read())

                    media = twitter.media_upload(os.path.join("C:", os.path.sep, "Users", "Owner", "PycharmProjects", "Black_People_Twitter_Bot", str(i)))
                    medias_ids.append(media.media_id_string)

                with open("previous_posts.txt", "a") as f:
                    f.write(submission.id + "\n")
                with open("previous_posts.txt", "r") as f:
                    contents = f.readlines()

                if len(medias_ids) > 4:
                    album = imgur.create_album(title=submission.title)
                    print(vars(album))
                    for i in range(len(medias_ids)):
                        image = imgur.upload_image(path=os.path.join("C:", os.path.sep, "Users", "Owner", "PycharmProjects", "Black_People_Twitter_Bot", str(i)),album=album.deletehash)
                        sleep(5)
                    twitter2.create_tweet(text=submission.title + " " + album.link)
                    dir(imgur)
                else:
                    twitter2.create_tweet(text=submission.title, media_ids=medias_ids)

                print("new post")
                posts += 1

        print(f"{posts} post(s) posted over {loops} loops at {datetime.datetime.now()}")
        loops += 1
        sleep(30)