from db import execute_query
import os
import json

def get_links_data():
    sql = "SELECT * FROM nextlinks "
    links_data = execute_query(sql)
    # 构造节点和边的数据
    nodes_set = set()
    edges = []
    # 获取所有nextlink列的字段名
    nextlink_columns = ['nextlink1', 'nextlink2', 'nextlink3', 'nextlink4', 'nextlink5', 'nextlink6', 'nextlink7']
    for row in links_data:
        linkid = row['linkid']
        # 获取该行所有nextlink的值
        nextlinks = [row[col] for col in nextlink_columns if row[col] is not None]
        # 将 linkid 和 nextlink 添加到集合中
        nodes_set.add(str(linkid))
        nodes_set.update(map(str, nextlinks))
        # 将 linkid 和 nextlink 组合成边
        edges.extend({'source': str(linkid), 'target': str(nextlink)} for nextlink in nextlinks)
    # 将集合中的元素转换为节点列表
    nodes = [{'name': node} for node in nodes_set]
    # 静态目录的路径
    static_dir = os.path.join('static', 'data')
    # 文件路径
    filename = os.path.join(static_dir, 'data2.json')
    # 返回构造好的数据
    data=edges
    # 保存数据到文件
    with open(filename, 'w') as f:
        json.dump(data, f)
    return {'success': True}

get_links_data()