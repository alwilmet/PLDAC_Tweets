from graph import *
from recover import *
from follow import *

# recover users data
data_user = get_dataframe_from_table("users_0415_0423",10000)

# select part of user for recover followers
data_user_reduced = data_user[data_user.followers_count < 500]
data_user_reduced = data_user_reduced.reset_index()

# recover username columns
users = data_user_reduced[['screen_name']]
users_tot = data_user[['screen_name']]

# get followers
followers = following_list(users[:300])

# clean users not in base






