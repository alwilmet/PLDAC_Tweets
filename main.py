from function.graph import *
from function.recover import *
from function.follow import *

part_following = False
part_retweets = False
part_histogram = False
part_hashtags = True

dict_candidat = {'macron': ['macron', 'EnMarche', 'MacronBercy', 'JeVoteMacron', 'Macron2017'],
                 'fillon': ['fillon', 'Fillon2017', 'JeVoteFillon', 'FillonPresident'],
                 'jlm': ['JLM2017', 'Mélenchon', 'LaForcedupeuple', 'JLMToulouse', 'AuNomDuPeuple', 'FranceInsoumise'],
                 'lepen': ['Marine2017', 'LePen', 'MarineLePen', 'MarineÀParis'],
                 'hamon': ['Hamon2017', 'Hamon']}
index_cand = np.concatenate(list(dict_candidat.values()))
data_cand = ['macron']*5 + ['fillon']*4 + ['jlm']*6 + ['lepen']*4 + ['hamon']*2
# recover data
users = get_dataframe_from_table("users_0415_0423")

# media = get_dataframe_from_table("medias_0415_0423",10000) # PHOTOS

if part_hashtags:
    # recover users data
    hashs = get_dataframe_from_table("hashs_0415_0423")
    hash_tweets = get_dataframe_from_table("tweet_hash_0415_0423")
    tweets = get_dataframe_from_table("tweets_0415_0423",columns = ['tweet_id','user_id'])

    # add column containing hashtag content in hash_tweets
    hashs['hash_id'] = hashs['hash_id'].apply(int)
    hash_tweets['hash'] = hash_tweets.hash_id.map(pd.Series(index=hashs.hash_id.values, data=hashs.hash.values))

    hash_tweets = hash_tweets[hash_tweets.hash.isin(np.concatenate(list(dict_candidat.values())))]

    hash_tweets['user_id'] = hash_tweets.tweet_id.map(pd.Series(index = tweets.tweet_id.values, data = tweets.user_id.values))

    hash_tweets['hash_simplified'] = hash_tweets.hash.map(pd.Series(index=index_cand, data=data_cand))
    hash_tweets = hash_tweets[hash_tweets.user_id.isin(users.user_id.values[:100])]
    tmp = hash_tweets[['user_id','hash_simplified']].groupby('user_id').aggregate(lambda x: list(x.hash_simplified.values))






if part_following:
    # select part of user for recover followers
    data_user_reduced = data_user[data_user.followers_count < 500]
    data_user_reduced = data_user_reduced.reset_index()

    # recover username columns
    users = data_user_reduced[['screen_name']]
    users_tot = data_user[['screen_name']]

    # get followers
    followers = following_list(users[:200])

    # clean users not in base

    followers = read_pkl('users')

    followers, users_tot_cleaned = clean_following(followers, users_tot.screen_name.values)

    write_followers_gml(followers, users_tot_cleaned)

if part_retweets:
    tweets = get_dataframe_from_table("tweets_0415_0423", number = 100000,
                                    columns=['tweet_id', 'user_id', 'retweeted_status_id', 'retweeted_user_id'])
    users_reduced = users[users.followers_count > 5000]
    write_retweets_gml(tweets, users_reduced)

if part_histogram:
    tweets = get_dataframe_from_table("tweets_0415_0423",columns = ['tweet_id','user_id'])
    tweets['nb_tweets'] = pd.Series(np.ones(tweets.shape[0])).values
    tweets_count = tweets[['user_id', 'nb_tweets']].groupby('user_id').count()
    users['nb_tweets'] = users.user_id.map(pd.Series(index=tweets_count.index, data=tweets_count.nb_tweets))

    #hist_user_tweet(users)
    hist_followers_tweet(users)
