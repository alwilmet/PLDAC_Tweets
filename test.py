import twint


c = twint.Config()
c.Username = 'jackbanh'
c.Hide_output = True
c.Pandas = True
c.Limit = 500
twint.run.Followers(c)
followed = twint.storage.panda.Follow_df["followers"].tolist()[0]
