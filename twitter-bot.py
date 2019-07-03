import config
import pandas as pd
import tweepy
import json

auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
api = tweepy.API(auth)

#Search Tweets with query = machine learning
def search_tweets():
	max_tweets = 2
	query = "machine learning"
	searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
	
	users_info = {}
	
	for tweets in searched_tweets:
		users_info.update({tweets.user.id_str : {	"UserName" : tweets.user.name,
													"ScreenName" : tweets.user.screen_name,
													"FollowersCount" : tweets.user.followers_count,
													"FriendsCount" : tweets.user.friends_count,
													"Followers" : [follower for follower in tweepy.Cursor(api.followers_ids, screen_name=tweets.user.screen_name, wait_on_rate_limit=True).items(10)],
													"Friends" : [friend for friend in tweepy.Cursor(api.friends_ids, screen_name=tweets.user.screen_name, wait_on_rate_limit=True).items(5)]
												}
							})

	users_df = pd.DataFrame(users_info)

	return users_df

def read_file():
	df = pd.read_csv('my_csv.csv', index_col= 0)
	return df


df2 = read_file()
usersdf = search_tweets()
for x in usersdf:
	df2[x] = usersdf[x]

df2.to_csv('my_csv.csv')

