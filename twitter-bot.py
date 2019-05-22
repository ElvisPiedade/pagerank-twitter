import tweepy

CONSUMER_KEY = 'jQRWMxNP3M0X9YJzlyx5w8eRJ'
CONSUMER_SECRET = 'BpOnE9fnAfpMxewiRQND0gQdexqxiW9Yz1EhAr1ciJhminVk4a'
ACCESS_KEY = '2875725285-D0ZBWRuRN5uv5PzSd8ToYriFAwbpb4EUXA4LJf4'
ACCESS_SECRET = 'snqtYsn3p5I69G9UrwtTfkCYfUeuCovtw3KQBhhalF6Nu'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

api.update_status("Python-Test")