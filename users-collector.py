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

	count=0
	n = 1000
	all_data = pd.DataFrame(columns=['UserIndex', 'F_ID', 'Friend_Follower'])
	
	for id_user in users.index: 
		checked = users['Checked'][id_user]
		
		if checked == False and count < 20:
			try:
				users['Checked'][id_user] = True

				followers_list = []
				friends_list   = []
#				followers_list = [follower for follower in tweepy.Cursor(api.followers_ids, screen_name = users['ScreenName'][id_user], wait_on_rate_limit=True).items()]
			
				f = 0
				for follower in tweepy.Cursor(api.followers_ids, screen_name = users['ScreenName'][id_user], wait_on_rate_limit=True).items():
					followers_list.append(follower)
					f += 1
					if f == 5000 :
						f = 0
						print(len(followers_list))
#						pdb.set_trace()
						time.sleep(70)

				f = 0
				for friend in tweepy.Cursor(api.friends_ids, screen_name = users['ScreenName'][id_user], wait_on_rate_limit=True).items():
					friends_list.append(friend)
					f += 1
					if f == 5000 :
						f = 0
						print(len(friends_list))
#						pdb.set_trace()
						time.sleep(70)
#				friends_list = [friend for friend in tweepy.Cursor(api.friends_ids, screen_name = users['ScreenName'][id_user], wait_on_rate_limit=True).items()]
	
				followers_group = [followers_list[i * n:(i + 1) * n] for i in range((len(followers_list) + n - 1) // n )]
				friends_group = [friends_list[i * n:(i + 1) * n] for i in range((len(friends_list) + n - 1) // n )]
				
				data_followers = pd.DataFrame(columns=["F_ID"])
				data_friends = pd.DataFrame(columns=["F_ID"])
				
				for list_follower in followers_group:
					data_followers = data_followers.append({'F_ID': list_follower}, ignore_index=True)
				
				for list_friend in friends_group:
					data_friends = data_friends.append({'F_ID': list_friend}, ignore_index=True)

	#			pdb.set_trace()
				data_followers['Friend_Follower'] = 'Follower'
				data_friends['Friend_Follower'] = 'Friend'
					
				
				data_union = pd.concat([data_friends, data_followers])
				data_union.insert(loc=0, column='UserIndex', value=id_user)

				all_data = pd.concat([all_data, data_union])
				
				data_friends = data_friends[0:0]
				data_followers = data_followers[0:0]
				data_union = data_union[0:0]
				count+=1
				all_data.to_csv('graph_data.csv', mode='a', index=False, header=False)
				users.to_csv('users-temp.csv', mode='w')
			except:
				print("An exception occurred")
#			pdb.set_trace()
		else:
			if count >= 20:
				print('funcionou?')
				all_data.to_csv('graph_data.csv', mode='a', index=False, header=False)
				users.to_csv('users-temp.csv', mode='w')
				break



def read_file():
	df = pd.read_csv('users-temp.csv', index_col = 0)
#	pdb.set_trace()	
#	df['TweetID'] = df['TweetID'].astype(str)
#	df['TweetID'] = " "
#	df['Checked'] = False
#	df = df.drop(columns=['Followers', 'Friends'])
#	df.to_csv('users_info.csv', mode = 'w')


	print('leu arquivo users_info')
	return df


temp_df = read_file()

getFollowersAndFriends(temp_df)



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
