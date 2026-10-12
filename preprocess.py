# Preprocessing: Twitch Gamers (168k nodes, 6.8M edges) -> top 1000 creators by degree
import pandas as pd
e = pd.read_csv("data/large_twitch_edges.csv").iloc[:, :2]; e.columns = ["a", "b"]
f = pd.read_csv("data/large_twitch_features.csv")
deg = pd.concat([e.a, e.b]).value_counts()          # connections per creator
keep = set(deg.head(1000).index)                     # top 1000 by degree
e[e.a.isin(keep) & e.b.isin(keep)].to_csv("data/sample_edges.csv", index=False)
f[f.numeric_id.isin(keep)].to_csv("data/sample_features.csv", index=False)
print(len(keep), "creators saved")
