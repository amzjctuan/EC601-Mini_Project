#!/usr/bin/env python
# encoding: utf-8
#Author - Jessie Tuan

# Twitter API
import tweepy
import json
import csv
import urllib.request
import io
import os
# ffmpeg
import ffmpeg
# Google API
import argparse
import sys
from google.cloud import videointelligence
import io

## Twitter API credentials
consumer_key = 'Enter consumer key' 
consumer_secret = 'Enter consumer secret'
access_token = 'Enter access token'
access_token_secret = 'Enter access token secret'

class mini_project_1:
	
	# Step 1: Tweet API
	def tweet_api(self):

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)

		# #print all the tweets from twitter
		# public_tweets = api.home_timeline()
		# for tweet in public_tweets:
		#     print (tweet.text)
		
		#initialize a list to hold all the tweepy Tweets
		alltweets = []
		
		#make initial request for most recent tweets (200 is the maximum allowed count)
		new_tweets = api.user_timeline(screen_name = self.name,count=1)

		#save most recent tweets
		alltweets.extend(new_tweets)

		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		#keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:

		        print("getting tweets before %s" % (oldest))

		        #all subsequent requests use the max_id param to prevent duplicates
		        new_tweets = api.user_timeline(screen_name = self.name,count=200,max_id=oldest)

		        #save most recent tweets
		        alltweets.extend(new_tweets)

		        #update the id of the oldest tweet less one
		        oldest = alltweets[-1].id - 1

		        print("...%s tweets downloaded so far" % (len(alltweets)))

		#go through all found tweets and remove the ones with no images 
		outtweets = [] #initialize master list to hold our ready tweets
		for tweet in alltweets:
		        #not all tweets will have media url, so lets skip them
		        try:
		                print(tweet.entities['media'][0]['media_url']) 
		        except (NameError, KeyError):
		                #we dont want to have any entries without the media_url so lets do nothing
		                pass
		        else:
		                #got media_url - means add it to the output
		                outtweets.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.entities['media'][0]['media_url']])
		                
						
		#write the csv  
		with open('%s_tweets.csv' % self.name, 'w') as f:
			writer = csv.writer(f)
			# writer.writerow(["id","created_at","text","media_url"])
			writer.writerows(outtweets)

		pass

		with open('%s_tweets.csv' % self.name) as csvfile:
			readCSV = csv.reader(csvfile,delimiter=',')

			url_mem = []

			for row in readCSV:
				url = row[3]
				url_mem.append(url)

	# download image from url		
		x = 0
		for index in url_mem:
			file_name = "image_"+ str(x)
			full_path = file_name + '.jpg'
			urllib.request.urlretrieve(url_mem[x], full_path)
			x = x+1


	# Step 2: ffmpeg assemble images to video
	def ffmpeg(self):
		(
		    ffmpeg
		    .input('/Users/jessietuan/Desktop/IMG/*.jpg', pattern_type='glob', framerate=1)
		    .output(self.name+'.mp4')
		    .run()
		)

    # Step 3: Google API
	def google_analyze(self):
	    video_client = videointelligence.VideoIntelligenceServiceClient()
	    features = [videointelligence.enums.Feature.LABEL_DETECTION]

	    with io.open(self.name+'.mp4', 'rb') as movie:
	        input_content = movie.read()
	    try:
	        operation = video_client.annotate_video(features=features, input_content=input_content)
	        print('\nProcessing video for label annotations:')
	        result = operation.result(timeout=90)
	    except Exception as e:
	        print("Video Intelligence error")
	        exit()  
	    
	    print('\nFinished processing.')

	    # Process video/segment level label annotations
	    segment_labels = result.annotation_results[0].segment_label_annotations
	    for i, segment_label in enumerate(segment_labels):
	        print('Video label description: {}'.format(segment_label.entity.description))
	        for category_entity in segment_label.category_entities:
	            print ("Label category description: " +category_entity.description)   

	        for i, segment in enumerate(segment_label.segments):
	            confidence = segment.confidence
	            print ("The accuracy of the identification in this case is " +str(confidence) + "\n")


	    # analyze(self.name+'.mp4')
	    

if __name__ == '__main__':

	user = mini_project_1()
	user.name = input('Enter a twitter account:')

	user.tweet_api()
	user.ffmpeg()
	user.google_analyze()


	    



		
	    
	

			






