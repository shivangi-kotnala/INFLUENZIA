import os, random, numpy as np, pandas as pd, networkx as nx
import plotly.graph_objects as go, plotly.express as px, streamlit as st

st.set_page_config("INFLUENZIA", layout="wide")
SMP, FULL = os.path.exists("data/sample_edges.csv"), os.path.exists("data/large_twitch_edges.csv")
EDGES = "data/sample_edges.csv" if SMP else "data/large_twitch_edges.csv"
FEATS = "data/sample_features.csv" if SMP else "data/large_twitch_features.csv"
REAL = SMP or FULL

@st.cache_data
def load():
    if REAL:  # real Twitch Gamers data
        e = pd.read_csv(EDGES).iloc[:, :2]; e.columns = ["a", "b"]
        return e, pd.read_csv(FEATS).set_index("numeric_id")
    # demo data so the app always runs: 5 communities of 300 creators
    G = nx.stochastic_block_model([300] * 5, np.full((5, 5), .002) + np.eye(5) * .04, seed=1)
    rng = np.random.default_rng(1)
    lang = np.array(["EN", "DE", "FR", "ES", "JA"])[np.repeat(range(5), 300)]
    f = pd.DataFrame({"views": rng.integers(1000, 1_000_000, 1500), "language": lang})
    return pd.DataFrame(G.edges(), columns=["a", "b"]), f

@st.cache_data
def build(top_n):
    e, _ = load()
    deg = pd.concat([e.a, e.b]).value_counts()            # degree of every vertex
    keep = set(deg.head(top_n).index)                      # overload control: top-N only
    G = nx.from_pandas_edgelist(e[e.a.isin(keep) & e.b.isin(keep)], "a", "b")
    G.add_nodes_from(keep)
    cid = {n: i for i, c in enumerate(nx.community.louvain_communities(G, seed=42)) for n in c}
    bt = nx.betweenness_centrality(G, k=min(100, len(G)), seed=1)
    pos = nx.spring_layout(G, seed=42, k=1.5 / np.sqrt(len(G)), iterations=60)
    return G, cid, bt, nx.pagerank(G), pos

st.title("INFLUENZIA")
st.caption("Real data: Twitch Gamers (SNAP)" if REAL else "Demo data (synthetic). Put the Twitch CSVs in data/ for real data.")
top_n = st.sidebar.slider("Creators in sample", 100, 1000, 400, 50)
G, cid, bt, pr, pos = build(top_n)
f = load()[1]
color_by = st.sidebar.radio("Color by", ["Community", "Language"])
size_by = st.sidebar.radio("Size by", ["Degree", "PageRank", "Betweenness"])
min_deg = st.sidebar.slider("Min connections", 0, max(max(d for _, d in G.degree()) // 2, 1), 0)
cs = sorted(set(cid.values()))
comms = st.sidebar.multiselect("Communities", cs, default=cs)   # filter groups
who = st.sidebar.text_input("Search creator ID")

nodes = [n for n in G if G.degree(n) >= min_deg and cid[n] in comms]
if not nodes:
    st.warning("No creators match these filters."); st.stop()
H = G.subgraph(nodes)
focus = None
if who.strip().isdigit() and int(who) in H:                # search -> highlight neighbours
    focus = {int(who)} | set(H[int(who)])
elif who.strip():
    st.sidebar.warning("ID not in the current view.")

c = st.columns(5)
for col, (k, v) in zip(c, [("Vertices", H.number_of_nodes()), ("Edges", H.number_of_edges()),
        ("Density", round(nx.density(H), 4)), ("Components", nx.number_connected_components(H)),
        ("Isolated", nx.number_of_isolates(H))]):
    col.metric(k, v)

E = list(H.edges())
if len(E) > 6000:                                          # overload control: draw a sample of edges
    random.seed(1); E = random.sample(E, 6000) + (list(H.edges(int(who))) if focus else [])
    st.caption("Showing a random sample of 6,000 edges for speed. Metrics use all edges.")
ex, ey = [], []
for a, b in E:
    ex += [pos[a][0], pos[b][0], None]; ey += [pos[a][1], pos[b][1], None]
metric = {"Degree": dict(H.degree()), "PageRank": pr, "Betweenness": bt}[size_by]
vals = np.array([metric[n] for n in nodes], dtype=float)
size = 6 + 30 * vals / (vals.max() or 1)                   # visual variable: size
lang = f["language"].reindex(nodes).fillna("?")
codes = [cid[n] for n in nodes] if color_by == "Community" else pd.Categorical(lang).codes
pal = px.colors.qualitative.Bold
views = f["views"].reindex(nodes).fillna(0) if "views" in f else None
hover = [f"ID {n}<br>Connections: {H.degree(n)}<br>Community: {cid[n]}<br>Language: {lang[n]}"
         + (f"<br>Views: {views[n]:,.0f}" if views is not None else "") for n in nodes]

fig = go.Figure([
    go.Scatter(x=ex, y=ey, mode="lines", line=dict(width=.4, color="#666"), hoverinfo="none", opacity=.35),
    go.Scatter(x=[pos[n][0] for n in nodes], y=[pos[n][1] for n in nodes], mode="markers",
        text=hover, hoverinfo="text",
        marker=dict(size=size, color=[pal[int(x) % len(pal)] for x in codes],
                    opacity=[1 if focus is None or n in focus else .08 for n in nodes]))])
fig.update_layout(template="plotly_dark", height=650, showlegend=False, dragmode="pan",
                  xaxis=dict(visible=False), yaxis=dict(visible=False), margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, width="stretch", config={"scrollZoom": True})

st.subheader("Bridge creators (highest betweenness)")
st.dataframe(pd.DataFrame({"ID": nodes, "Connections": [H.degree(n) for n in nodes],
    "Community": [cid[n] for n in nodes], "Betweenness": [round(bt[n], 4) for n in nodes]}
    ).nlargest(10, "Betweenness"), hide_index=True)
with st.expander("Degree distribution"):
    st.plotly_chart(px.histogram(x=[d for _, d in H.degree()], nbins=30, template="plotly_dark",
        labels={"x": "connections"}), width="stretch")
