import config
import pandas as pd
import tweepy
import time
import numpy as np
import pdb
from datetime import datetime
from threading import Thread
from threading import Timer
from time import sleep

start_time = time.perf_counter()
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
api = tweepy.API(auth)
data = api.rate_limit_status()
now = datetime.now()
print(datetime.timestamp(now))

print(data['resources']['followers']['/followers/ids'])
print(data['resources']['friends']['/friends/ids'])

def getFollowersAndFriends(users):
	count = 0
	for id_user in users.index: 
		followers = len(users['Followers'][id_user])
		friends = len(users['Friends'][id_user])

		if (followers == 2 or friends == 2) and count < 2:
			users['Followers'][id_user] = [follower for follower in tweepy.Cursor(api.followers_ids, screen_name = users['ScreenName'][id_user], wait_on_rate_limit=True).items()]
			users['Friends'][id_user] = [friend for friend in tweepy.Cursor(api.friends_ids, screen_name = users['ScreenName'][id_user], wait_on_rate_limit=True).items()]
			count += 1
			print(count)
			print(id_user)
			data = api.rate_limit_status()
			print(data['resources']['followers']['/followers/ids'])
			print(data['resources']['friends']['/friends/ids'])
		else:
			if count >= 2:
				print('funcionou?')
				users.to_csv('new_users.csv', mode ='w')				
				break


#1800s = 30 min

def read_file():
#	df = pd.read_csv('users_data.csv', index_col= 0)
	df = pd.read_csv('new_users.csv', index_col = 0)
#	pdb.set_trace()	
	print('leu arquivo new_users')
	return df

def read_file2():
#	df = pd.read_csv('users_data.csv', index_col= 0)
	df = pd.read_csv('users_info.csv', index_col = 0)
#	pdb.set_trace()	
	print('leu arquivo users_info')
	return df

#t = Timer(1800.0, getFollowersAndFriends(read_file()))
#t.start()

#Search Tweets with query = machine learning
def search_tweets(temp_data):
	max_tweets = 2000
	query = "machine learning"
	searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, wait_on_rate_limit=True).items(max_tweets)]
	
	users_info = {}
	tweets_info = {}

	
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

		tweets_info.update({tweets.user.id_str : { 
													"UserID"	: tweets.user.id_str,
													"TweetInfo" : {
																	"TweetID"	: tweets.id_str,
																	"CreatedAt" : tweets.created_at
																  }												
												 }
						  })



	users_df = pd.DataFrame.from_dict(users_info, orient="index")
	users_df = users_df.set_index('UserID', drop=False)
	users_df.index.names = ['UserIndex']


#	pdb.set_trace()	
	union_df = pd.concat([temp_data, users_df])
	
	union_df = union_df.reset_index(drop=True)
	
#	pdb.set_trace()
	try:
		df_gpby = union_df.groupby(['UserID'])
		
		idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]

#		pdb.set_trace()
		aa = union_df.reindex(idx)
		aa = aa.set_index('UserID', drop=False)
		aa.index.names = ['UserIndex']

		aa.to_csv('users_info.csv', mode ='w')

#		pdb.set_trace()
		return aa
	except:
		print("An exception occurred")

#	pdb.set_trace()	
	return 0



def removeDuplicateRows():
	df = pd.read_csv('users_info.csv', index_col = 0)
	df.drop_duplicates(subset ="UserID", 
                     keep = 'first', inplace = True)
	print(df.shape[0])
	df.to_csv('users_info.csv', mode='w')


temp_df = read_file2() #ler o arquivo temporario

usersdf = search_tweets(temp_df)

removeDuplicateRows()

#getFollowersAndFriends(read_file())




#if usersdf != 0:
#	df2 = pd.read_csv('users_data.csv', index_col = 'UserID')

#	for x in usersdf:
#		df2[x] = usersdf[x]

#	df2.to_csv('users_data.csv')

#df = pd.read_csv('teste.csv', index_col = 'UserID')
#pdb.set_trace()

#getFollowersAndFriends(df2)


print("--- %s seconds ---" % (time.perf_counter() - start_time))
data = api.rate_limit_status()
ts = int(data['resources']['friends']['/friends/ids']['reset'])
ts2 = int(data['resources']['followers']['/followers/ids']['reset'])
ts3 = int(data['resources']['search']['/search/tweets']['reset'])

#reseta a cada 30 min mais ou menos
print(data['resources']['application'])
print(data['resources']['search'])
print(datetime.utcfromtimestamp(ts3).strftime('%Y-%m-%d %H:%M:%S'))
print(data['resources']['followers']['/followers/ids'])
print(datetime.utcfromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S'))
print(data['resources']['friends']['/friends/ids'])
print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))



# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
