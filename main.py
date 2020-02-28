from function.graph import * # fichier qui regroupe les fonctions pour faire les graphes
from function.follow import *  # fichier qui regroupe les fonctions sur les follows
from function.hashtags import * # fichier qui regoupe les fonctions pour analyser les hashtags
from function.figure import *


# sélectionner les parties de l'analyse que l'on veut effectuer
from function.recover import get_dataframe_from_table

part_following = False
part_retweets = True
part_figure = False
part_hashtags = True


# définition à la main du dictionnaire pour rassembler les hashtags sur un hashtag commun
dict_candidat = {'macron': ['macron', 'EnMarche', 'MacronBercy', 'JeVoteMacron', 'Macron2017'],
                 'fillon': ['fillon', 'Fillon2017', 'JeVoteFillon', 'FillonPresident'],
                 'jlm': ['JLM2017', 'Mélenchon', 'LaForcedupeuple', 'JLMToulouse', 'AuNomDuPeuple', 'FranceInsoumise'],
                 'lepen': ['Marine2017', 'LePen', 'MarineLePen', 'MarineÀParis'],
                 'hamon': ['Hamon2017', 'Hamon']}
index_cand = np.concatenate(list(dict_candidat.values()))
data_cand = ['macron']*5 + ['fillon']*4 + ['jlm']*6 + ['lepen']*4 + ['hamon']*2

# recover data
users = get_dataframe_from_table("users_0415_0423")

# compute number of tweet per user
tweets = get_dataframe_from_table("tweets_0415_0423",columns = ['tweet_id','user_id'])
tweets['nb_tweets'] = pd.Series(np.ones(tweets.shape[0])).values
tweets_count = tweets[['user_id', 'nb_tweets']].groupby('user_id').count()
users['nb_tweets'] = users.user_id.map(pd.Series(index=tweets_count.index, data=tweets_count.nb_tweets))

# select users with more than 100 tweets
users_reduced = users[users.nb_tweets > 100]

# recover data about media
media = get_dataframe_from_table("medias_0415_0423")

if part_hashtags:
    # recover tweets and hashtags data
    hashs = get_dataframe_from_table("hashs_0415_0423")
    hash_tweets = get_dataframe_from_table("tweet_hash_0415_0423")
    tweets = get_dataframe_from_table("tweets_0415_0423",columns = ['tweet_id','user_id'])

    # add column containing hashtag content in hash_tweets
    hashs['hash_id'] = hashs['hash_id'].apply(int)
    hash_tweets['hash'] = hash_tweets.hash_id.map(pd.Series(index=hashs.hash_id.values, data=hashs.hash.values))

    # on garde les hashtags qui sont dans le dictionnaire défini au début
    hash_tweets = hash_tweets[hash_tweets.hash.isin(np.concatenate(list(dict_candidat.values())))]
    # ajout d'une colonne pour le user qui a écrit le hashtag
    hash_tweets['user_id'] = hash_tweets.tweet_id.map(pd.Series(index = tweets.tweet_id.values, data = tweets.user_id.values))

    # on regroupe les hashtags ( jlm,jlm2017,jlmToulouse ---> jlm)
    hash_tweets['hash_simplified'] = hash_tweets.hash.map(pd.Series(index=index_cand, data=data_cand))

    #on sélectionne les hashtags des users qui ont au moins 100 tweets
    hash_tweets = hash_tweets[hash_tweets.user_id.isin(users_reduced.user_id.values)]
    tmp = hash_tweets[['user_id','hash_simplified']].groupby('user_id').hash_simplified.apply(list)

    #on ajoute une colonne dans la table des users, contenant les hashtags qu'ils ont écrit
    users_reduced['hashtags'] = users_reduced.user_id.map(tmp)
    # calcul de l'entropie
    users_reduced = entropy_hashtags(users_reduced)
    # définition de l'affinité politique
    users_reduced = politic_affinity((users_reduced))



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
    # on récupere la table des tweets avec les informations sur les retweets
    tweets = get_dataframe_from_table("tweets_0415_0423",
                                    columns=['tweet_id', 'user_id', 'retweeted_status_id', 'retweeted_user_id'])
    #calcul de nombre de fois qu'une personne est retweetée
    retweeted_count = tweets[['user_id','retweeted_user_id']].groupby('retweeted_user_id').count()
    users['retweeted_count'] = users.user_id.map(pd.Series(index=retweeted_count.index, data=retweeted_count.user_id.values))

    #calcul du nombre de fois qu'un user retweet
    retweeter_count = tweets[~tweets.retweeted_user_id.isin([None])][['user_id','retweeted_user_id']].groupby('user_id').count()
    users['retweeter_count'] = users.user_id.map(pd.Series(index=retweeter_count.index, data=retweeter_count.retweeted_user_id.values))

    users = users.astype(object).replace('None',0) # on remplace les np.nan par des None

    # partitionnement par rapport aux nb tweets, retweeted/retweeter count en utilisant KMeans
    users2['cluster_id'] = supervised(users2,['nb_tweets','retweeter_count','retweeted_count'])


if part_figure:
    hist_user_tweet(users)
    scatterplot(users2,'followers_count','nb_tweets',title='scatterplot',filename='nb_foll_nb_tweets_scatter')
    scatterplot_cluster(users2,'nb_tweets','retweeted_count',title='scatterplot_cluster',filename='cluster_nb_tweets_retweeted_scatter')
    # on écrit le fichier de graphe des retweets
    write_retweets_gml(tweets, users_reduced)
