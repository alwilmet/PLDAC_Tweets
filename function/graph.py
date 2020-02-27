###### fichier qui regroupe les fonctions pour faire les graphes

import numpy as np
import matplotlib.pyplot as plt


# def louvain_community():


def write_retweets_gml(tweets, users, affinity = True):
    # on réduit la table des tweets: on garde les users qui ont une affinité
    if affinity:
        users = users[~users.politic_affinity.isin(['None'])]
    # on nettoie les tweets, on ne garde que les tweets retweeters/retweeteurs par la table des users
    tweets = tweets[tweets.retweeted_user_id.isin(users.user_id.values)]
    tweets = tweets[tweets.user_id.isin(users.user_id.values)]
    tweets = tweets[~tweets.retweeted_user_id.isin([None])]

    with open('./data/retweets2.gml', 'w') as f:
        f.write("Creator \"Retweets\"\n")
        f.write("graph\n[\n")
        for user in users.itertuples():
            # on écrit les noeuds du graphe
            f.write("  node\n  [\n")
            f.write("   id %s\n" % user.user_id)
            # f.write("   category %s\n" %user.category)
            f.write("   politic_affinity %s\n" % user.politic_affinity)
            f.write("  ]\n")
        for retweet in tweets.itertuples():
            # on écrit les liaisons
            f.write("  edge\n  [\n")
            f.write("   source %s\n" % retweet.retweeted_user_id)
            f.write("   target %s\n" % retweet.user_id)
            f.write("   weight 1\n")
            f.write("  ]\n")
        f.write("]\n")

#inutile pour le moment
def write_mentions_gml(tweets_mentions, users):
    users_unique = np.unique(
        np.concatenate((tweets_mentions.source_user_id.unique(), tweets_mentions.target_user_id.unique())))
    users = users[users.user_id.isin(users_unique)]

    with open('./data/retweets.gml', 'w') as f:
        f.write("Creator \"Retweets\"\n")
        f.write("graph\n[\n")
        for user in users.itertuples():
            f.write("  node\n  [\n")
            f.write("   id %s\n" % user.user_id)
            # f.write("   category %s\n" %user.category)
            # f.write("   politic_affinity %s\n" %user.affinity)
            f.write("  ]\n")
        for retweet in tweets_mentions.itertuples():
            f.write("  edge\n  [\n")
            f.write("   source %s\n" % retweet.source_user_id)
            f.write("   target %s\n" % retweet.target_user_id)
            f.write("   weight 1\n")
            f.write("  ]\n")
        f.write("]\n")

# fonctionnel, mais le contenu: la table de followers ne l'est pas
def write_followers_gml(followers, users):
    with open('./following3.gml', 'w') as f:
        f.write("Creator \"Following\"\n")
        f.write("graph\n[\n")
        for user in users:
            f.write("  node\n  [\n")
            f.write("   id %s\n" % user)
            f.write("  ]\n")
        for row in followers.itertuples():
            fols = row.following
            for fol in fols:
                f.write("  edge\n  [\n")
                f.write("   source %s\n" % row.screen_name)
                f.write("   target %s\n" % fol)
                f.write("   weight 1\n")


def hist_user_tweet(users):
    text_box = []
    paliers = [0, 10, 30, 50, 100, 200]
    # pour faire le résumé de l'histogramme: on compte le nb de user dans chaque tranche définie dans paliers
    for i in range(len(paliers) - 1):
        num_of_tweets = users[users.nb_tweets <= paliers[i + 1]]
        num_of_tweets = num_of_tweets[users.nb_tweets >= paliers[i]].shape[0]
        pc_of_tweets = 100.0 * num_of_tweets / users.shape[0]
        text_box.append(
            'Users with %d <= tweets <= %d: %d  (%f )' % (paliers[i], paliers[i + 1], num_of_tweets, pc_of_tweets))

    num_of_tweets = users[users.nb_tweets >= paliers[-1]].shape[0]
    pc_of_tweets = 100.0 * num_of_tweets / users.shape[0]
    text_box.append('Users with tweets >= %d: %d  (%f )' % (paliers[-1], num_of_tweets, pc_of_tweets))

    # mise en forme de l'histogramme
    min_value = users.nb_tweets.values.min()
    max_value = users.nb_tweets.values.max()
    fig, ax = plt.subplots()
    bincuts = np.linspace(start=min_value - 0.5, stop=max_value + 0.5, num=(max_value - min_value + 2), endpoint=True)
    ax.grid()
    ax.hist(users.nb_tweets.values, bins=bincuts, edgecolor='black', linewidth=0.8, zorder=3)
    ax.set_xscale("log", nonposx='clip')
    ax.set_yscale("log", nonposy='clip')
    props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
    ax.text(0.35, 0.9, '\n'.join(text_box), transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    plt.xlabel('Number of Tweets')
    plt.ylabel('Number of Users')
    plt.show()
    plt.savefig('./figures/hist_user_nb_tweets.pdf')
    plt.clf()
    plt.close()


# pareil que l'autre, mais pour toutes les donénes c'est trop long car il y a trop de bins sur l'histogramme
def hist_followers_tweet(users):
    text_box = []
    paliers = [0, 100, 500, 1000, 2000]
    for i in range(len(paliers) - 1):
        num_of_tweets = users[users.followers_count <= paliers[i + 1]]
        num_of_tweets = num_of_tweets[users.followers_count >= paliers[i]].shape[0]
        pc_of_tweets = 100.0 * num_of_tweets / users.shape[0]
        text_box.append(
            'Users with %d <= tweets <= %d: %d  (%f )' % (paliers[i], paliers[i + 1], num_of_tweets, pc_of_tweets))

    num_of_tweets = users[users.followers_count >= paliers[-1]].shape[0]
    pc_of_tweets = 100.0 * num_of_tweets / users.shape[0]
    text_box.append('Users with tweets >= %d: %d  (%f )' % (paliers[-1], num_of_tweets, pc_of_tweets))
    min_value = users.followers_count.values.min()
    max_value = users.followers_count.values.max()
    fig, ax = plt.subplots()
    bincuts = np.linspace(start=min_value - 0.5, stop=max_value + 0.5, num=(max_value - min_value + 2), endpoint=True)
    ax.grid()
    users['followers_count'] = users.followers_count.apply(lambda x: round(x, -4))
    print(users.followers_count.values)
    ax.hist(users.followers_count.values, bins=bincuts, edgecolor='black', linewidth=0.8, zorder=3)
    ax.set_xscale("log", nonposx='clip')
    ax.set_yscale("log", nonposy='clip')
    props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
    ax.text(0.35, 0.9, '\n'.join(text_box), transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    plt.xlabel('Number of Followers')
    plt.ylabel('Number of Users')
    plt.show()
    plt.savefig('./figures/hist_user_nb_followers.pdf')
    plt.clf()
    plt.close()
