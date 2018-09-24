# EC601-Mini_Project: API Tutorial
2018 Fall - Boston University - EC601 #project_1
API

1. Twitter API: 
   Use twitter API to grab the photos form the twitter account.
   
2. ffmpeg:
   Transfer the photos downloaded from twitter into video.
   
3. Google Visial API:
   Describe each of the photos from the video made in the previous step.

# System Environment 

- Python 3.6.5
- ffmpeg 3.4.4
- Tweepy 3.6.0
- google-cloud-videointelligence 1.3.0
- Ubuntu 18.04.1 LTS

   
# Program Description

There are three functions made in the mini_project_api.py.
- tweet_api
- ffmpeg
- google_analyze

You need to type the twitter account that you wanna grab the photos from.
Then, it will automatically help you to download all the photos from the account and translate each of the photos.




# Note
Google application credentials:
```
export GOOGLE_APPLICATION_CREDENTIALS='google_application_credentials.json'
```
Make sure file 'google_application_credentials.json' has correct path.



