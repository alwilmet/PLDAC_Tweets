
def write_followers_gml(followers ,users):
    with open('./following2.gml', 'w') as f:
        f.write("Creator \"Following\"\n")
        f.write("graph\n[\n")
        for user in users:
            f.write("  node\n  [\n")
            f.write("   id %s\n" %user)
            f.write("  ]\n")
        for row in followers.itertuples():
            fols = row.following.values
            for fol in fols:
                f.write("  edge\n  [\n")
                f.write("   source %s\n" % row.screen_name)
                f.write("   target %s\n" % fol)
                f.write("   weight 1\n")
                f.write("  ]\n")
        f.write("]\n")


"""
from igraph import *
g = Graph.Read_GML("following.gml")
p = g.community_multilevel()
q = g.modularity(p)
print(q)"""
