import networkx as nx
from flask import Flask, render_template, request, redirect, flash, jsonify

import os,json
import pickle
import pymysql
# from db import execute_query


import queue

# 数据库连接配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '',
    'charset': 'utf8',
    'db': 'tmpsql'
}

# 创建数据库连接池类
class ConnectionPool:
    def __init__(self, size):
        self.size = size
        self.pool = queue.Queue(maxsize=size)

    def get_connection(self):
        if self.pool.qsize() < self.size:
            conn = pymysql.connect(**DB_CONFIG)
            self.pool.put(conn)
        return self.pool.get()

    def return_connection(self, conn):
        self.pool.put(conn)

# 创建全局连接池对象
DB_POOL_SIZE = 10
db_pool = ConnectionPool(DB_POOL_SIZE)

def connect_db():
    return pymysql.connect(**DB_CONFIG)

# 修改execute_query函数以使用连接池
def execute_query(sql, params=None):
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        return result
    except pymysql.Error as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        db_pool.return_connection(conn)



# 假设你有一个函数来查询 linkavg 表中 linkavgtime 的值
def query_linkavgtime_from_database(linkid):
    # 在这里执行查询 linkavg 表中 linkid 对应的 linkavgtime 的操作
    # 返回查询到的 linkavgtime 值，如果未找到，则返回 None
    sql = f"SELECT linkavgtime FROM linkavg WHERE linkid='{linkid}'"
    result = execute_query(sql)
    try:
        linkavgtime = result[0][0]  # 取第一个元素
        return linkavgtime
    except IndexError:
        return None  # 如果未找到数据，则返回 None

# 读取 data2.json 文件
with open('static/data/data2.json', 'r') as f:
    data = json.load(f)

# 初始化图
G = nx.Graph()

# 遍历数据
for edge in data:
    source = edge['source']
    target = edge['target']
    # 查询 source 和 target 对应的 linkavgtime 值
    linkavgtime_source = query_linkavgtime_from_database(source)
    linkavgtime_target = query_linkavgtime_from_database(target)
    if linkavgtime_source is not None and linkavgtime_target is not None:
        weight = (linkavgtime_source + linkavgtime_target) / 2
    else:
        # 如果有一个linkavgtime为None，则将weight设置为正无穷大
        weight = float('inf')

    print(weight)
    # 添加边到图中
    G.add_edge(source, target, weight=weight)

# 定义文件路径
file_path = os.path.join("static", "data", "graph_data.gpickle")

# 将图保存为文件
with open(file_path, 'wb') as f:
    pickle.dump(G, f)
