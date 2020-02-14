from recover import *
import seaborn as sns
import matplotlib.pyplot as plt

# recover users data

hashs = get_dataframe_from_table("hashs_0415_0423")
hash_tweets = get_dataframe_from_table("tweet_hash_0415_0423")

hashs['hash_id'] = hashs['hash_id'].apply(int)
hash_tweets['hash'] = hash_tweets.hash_id.map(pd.Series(index=hashs.hash_id.values, data=hashs.hash.values))

hist = hash_tweets.hash.value_counts()[:20].plot(kind='bar')
hist.set_xticklabels(hist.get_xticklabels(), rotation=45, horizontalalignment='right')
