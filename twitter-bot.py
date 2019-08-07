import config
import pandas as pd
import tweepy
import time
import numpy as np
import pdb

start_time = time.perf_counter()
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
api = tweepy.API(auth)

#Search Tweets with query = machine learning
def search_tweets(temp_data):
	print(temp_data)
	max_tweets = 5
	query = "machine learning"
	searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, wait_on_rate_limit=True).items(max_tweets)]
	
	users_info = {}

	
	for tweets in searched_tweets:
		users_info.update({tweets.user.id_str : {
												 "UserID"			: tweets.user.id_str,
												 "CreatedAt"	 	: tweets.created_at,
												 "UserName" 		: tweets.user.name,
											  	 "ScreenName"		: tweets.user.screen_name,
												 "FollowersCount"	: tweets.user.followers_count,
												 "FriendsCount" 	: tweets.user.friends_count,
												 "Followers" 		: [],
												 "Friends" 			: []
						  						}
						  })
	


	users_df = pd.DataFrame.from_dict(users_info, orient="index")
	users_df = users_df.set_index('UserID', drop=False)
	print(users_df)

	temp_data = temp_data.set_index('UserID')
	temp_data.rename(columns={'Unnamed: 0':'UserID'}, inplace=True)
	print(temp_data)
	
	union_df = pd.concat([temp_data, users_df])
	
	union_df['UserID'] = pd.to_numeric(union_df['UserID'])

	union_df = union_df.reset_index(drop=True)
#	temp_data = temp_data.reset_index(drop=True)	
	
	try:
		df_gpby = union_df.groupby(['UserID'])
		
		idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]

		new_idx = [x[0] for x in union_df.values]

		aa = union_df.reindex(idx)
		aa = aa.set_index('UserID', drop=False)

		aa.to_csv('temp_data.csv')
		pdb.set_trace()
		return aa
	except:
		print("An exception occurred")
#	users_df.to_csv('temp_data.csv')
	pdb.set_trace()	
	return 0

def read_file():
#	df = pd.read_csv('users_data.csv', index_col= 0)
	df = pd.read_csv('temp_data.csv')
	return df

def getFollowersAndFriends(users):
#	for follower in tweepy.Cursor(api.followers_ids, screen_name=users[id_user]['ScreenName'], wait_on_rate_limit=True).items():
#		print(follower)
	for id_user in users:
		users[id_user]['Followers'] = [follower for follower in tweepy.Cursor(api.followers_ids, screen_name=users[id_user]['ScreenName'], wait_on_rate_limit=True).items(10)]
		users[id_user]['Friends'] = [friend for friend in tweepy.Cursor(api.friends_ids, screen_name=users[id_user]['ScreenName'], wait_on_rate_limit=True).items(10)]



temp_df = read_file() #ler o arquivo temporario

usersdf = search_tweets(temp_df)

if usersdf != 0 :
	df2 = pd.read_csv('users_data.csv', index_col = 'UserID')

	for x in usersdf:
		df2[x] = usersdf[x]

	df2.to_csv('users_data.csv')



#getFollowersAndFriends(df2)


print("--- %s seconds ---" % (time.perf_counter() - start_time))
data = api.rate_limit_status()

#reseta a cada 30 min mais ou menos
print(data['resources']['application'])
print(data['resources']['search'])
print(data['resources']['followers']['/followers/ids'])
print(data['resources']['friends']['/friends/ids'])