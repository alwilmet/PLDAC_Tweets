from function.graph import *
from function.recover import *
from function.follow import *

# recover users data
data_user = get_dataframe_from_table("users_0415_0423",10000)

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


followers, users_tot_cleaned = clean_following(followers,users_tot.screen_name.values)

write_followers_gml(followers,users_tot_cleaned)



