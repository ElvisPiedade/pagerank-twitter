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

def read_file2():
	df = pd.read_csv('graph_data.csv', index_col = 0)
#	pdb.set_trace()	
#	df['TweetID'] = df['TweetID'].astype(str)
#	df['TweetID'] = " "
#	df['Checked'] = False
#	df = df.drop(columns=['Followers', 'Friends'])
#	df.to_csv('users_info.csv', mode = 'w')


	print('leu arquivo graph_data')
	return df

def read_file():
	df = pd.read_csv('users-info.csv', index_col = 0)
#	pdb.set_trace()	
#	df['TweetID'] = df['TweetID'].astype(str)
#	df['TweetID'] = " "
#	df['Checked'] = False
#	df = df.drop(columns=['Followers', 'Friends'])
#	df.to_csv('users_info.csv', mode = 'w')


	print('leu arquivo users-info')
	return df

#t = Timer(1800.0, getFollowersAndFriends(read_file()))
#t.start()

#Search Tweets with query = machine learning
def search_tweets(temp_data):
	max_tweets = 2300
	query = "machine learning"
	searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, wait_on_rate_limit=True).items(max_tweets)]
	
	users_info = {}
	tweets_info = {}

	
	for tweets in searched_tweets:
		users_info.update({tweets.user.id_str : {
												 "UserID"			: tweets.user.id_str,
												 "CreatedAt"	 	: tweets.created_at,
												 "TweetID"			: tweets.id_str,
												 "UserName" 		: tweets.user.name,
											  	 "ScreenName"		: tweets.user.screen_name,
												 "FollowersCount"	: tweets.user.followers_count,
												 "FriendsCount" 	: tweets.user.friends_count,
												 "Checked"  		: False
						  						}
						  })

#	pdb.set_trace()


	users_df = pd.DataFrame.from_dict(users_info, orient="index")
	users_df = users_df.set_index('UserID', drop=False)
	users_df.index.names = ['UserIndex']


	union_df = pd.concat([temp_data, users_df])
	
	union_df = union_df.reset_index(drop=True)
	
#	pdb.set_trace()
	try:
		df_gpby = union_df.groupby(['UserID'])
		
		idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]


		aa = union_df.reindex(idx)
		aa = aa.set_index('UserID', drop=False)
		aa.index.names = ['UserIndex']
#		pdb.set_trace()
		aa.to_csv('users-info.csv', mode ='w')

#		pdb.set_trace()
		return aa
	except:
		print("An exception occurred")

#	pdb.set_trace()	
	return 0



def removeDuplicateRows():
	df = pd.read_csv('users-info.csv', index_col = 0)
	df.drop_duplicates(subset ="UserID", 
                     keep = 'first', inplace = True)
	print(df.shape[0])
	df.to_csv('users-info.csv', mode='w')


temp_df = read_file() #ler o arquivo temporario

usersdf = search_tweets(temp_df)

removeDuplicateRows()




def removeDuplicateUsers():
	users_info = read_file() 
	graph_data = read_file2() #Todos usuários que estiverem aqui já foram iterados
	pdb.set_trace()
	graph_data['idx'] = graph_data.index
	graph_data.drop_duplicates(subset = "idx", keep= 'first', inplace = True)
	abcd = list(graph_data['idx'])

	for x in abcd:
		if users_info['Checked'][x] == False:
			print(x)
			users_info['Checked'][x] = True

	users_info.to_csv('update_users_info.csv', mode='w')

#removeDuplicateUsers()


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
