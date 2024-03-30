import os
import pickle
import networkx as nx

# 定义图数据文件路径
file_path = os.path.join("static", "data", "graph_data.gpickle")
# 加载图数据
with open(file_path, 'rb') as f:
    G = pickle.load(f)
print(G.nodes())