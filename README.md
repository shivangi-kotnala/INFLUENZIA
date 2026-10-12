# INFLUENZIA
Interactive network visualization of creator connections. It identifies influential creators, communities and hidden bridge creators.
Course project: DSE3150 Graph Visualization.

## Dataset
Twitch Gamers (SNAP): https://snap.stanford.edu/data/twitch_gamers.html
B. Rozemberczki and R. Sarkar, "Twitch Gamers: a Dataset for Evaluating Proximity Preserving and Structural Role-based Node Embeddings", 2021.
168,114 users, 6,797,557 mutual-follow edges. Twitch stands in for an influencer network.

## Graph (formal description)
Undirected, unweighted, finite. Vertex = creator, edge = mutual follow.
The app reports vertices, edges, density, connected components and isolated vertices.

## Setup
1. Python 3.11, then: `pip install -r requirements.txt`
2. Put `large_twitch_edges.csv` and `large_twitch_features.csv` in `data/`
3. `python preprocess.py` (keeps the top 1,000 creators by degree)
4. `streamlit run app.py` (opens http://localhost:8501)
Without the CSVs the app runs on built-in synthetic demo data.

## Pipeline
Raw CSV -> Pandas tables -> NetworkX metrics (degree, PageRank, betweenness, Louvain) -> Plotly visual structures -> Streamlit view.

## Visual mapping
| Data | Visual variable | Why |
|---|---|---|
| Graph structure | Position (spring layout) | Connected creators sit close together |
| Community / language | Color | Categorical data suits hue |
| Degree / PageRank / betweenness | Size | Quantitative data suits area |
| Connection | Line | Shows who is linked |

## Design principles
- Gestalt: proximity (layout), similarity (color), connectedness (edges)
- Overload control: top-N sample, min-connections filter, dimming of non-neighbors
- Group technique: Louvain community detection

## Interaction
Zoom/pan, hover details-on-demand, search by creator ID with neighbor highlighting, filters, switchable size and color encodings.
https://influenzia-gsguv7mswtnqtazdutnhf9.streamlit.app/

## Limitations
Top-N sample, approximate betweenness (150 sampled nodes), Twitch used as a stand-in for influencers.

## Deploy (Streamlit Community Cloud)
Push these files to a GitHub repo, then at share.streamlit.io choose the repo, branch `main` and main file `app.py`.
Large CSVs cannot go on GitHub (100 MB limit). Run `preprocess.py` locally and upload only `data/sample_edges.csv` and `data/sample_features.csv`.
Without data files the app runs on synthetic demo data.

## Features added in v2
Community filter, degree-distribution chart, edge sampling for large graphs, dynamic min-connections slider, data-source label, friendly search messages.
