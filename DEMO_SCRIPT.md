# INFLUENZIA demo script (about 6 minutes)
Before class: run `streamlit run app.py`, note one bridge ID from the table, keep the terminal open.

1. (0:30) Question: who is influential, which communities exist, who bridges them?
2. (0:45) Stat cards: vertices, edges, density, components, isolated. This is the graph in formal terms.
3. (1:00) Color = Community. Louvain groups creators who are densely connected. Proximity and similarity (Gestalt) make groups visible.
4. (1:30) Size = Degree, then Betweenness. Hubs are popular; bridges connect communities. Compare the two.
5. (1:00) Search a bridge ID from the table. Its neighbors are highlighted and everyone else is dimmed.
6. (0:30) Min connections slider and sample-size slider: overload control.
7. (0:30) Color = Language: do communities match language?
8. (0:30) Evaluation: 3 classmates found the top creator and a bridge creator. Close with limitations.

Q&A: why top 1000 (readability and speed); degree vs betweenness; what Louvain does (maximizes modularity); why spring layout (attraction makes clusters); betweenness approximate (150 sampled nodes); why Twitch (public mutual-follow network).
