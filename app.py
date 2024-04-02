from flask import Flask, render_template, request, redirect, flash, jsonify
from db import execute_query
from import_csv import import_csv_to_db1, import_csv_to_db2, import_csv_to_db3
import os,json
import networkx as nx
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

# 结点信息
@app.route('/handle_node_click', methods=['GET','POST'])
def handle_node_click():
    if request.method == 'POST':
        linkid=request.form['nodeName']
        pass

# 如果link数据有变化时，更新linkavg表
@app.route('/avglinks', methods=['GET'])
def avglinks():
    sql ="""
    INSERT INTO linkavg (linkid, linkavgtime, avgstatus)
    SELECT linkid, AVG(linktime) AS avg_linktime, ROUND(AVG((linkcurrentstatus + linkarrivalstatus) / 2)) AS avg_status
    FROM trajectorylink
    GROUP BY linkid
    ON DUPLICATE KEY UPDATE linkavgtime = VALUES(linkavgtime), avgstatus = VALUES(avgstatus);
    """
    execute_query(sql)



# 路网数据
@app.route('/get_links_data', methods=['GET'])
def get_links_data():
    sql = "SELECT * FROM nextlinks ORDER BY RAND() LIMIT 2000"
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
    filename = os.path.join(static_dir, 'data.json')
    # 返回构造好的数据
    data={'nodes': nodes, 'edges': edges}
    # 保存数据到文件
    with open(filename, 'w') as f:
        json.dump(data, f)
    return {'success': True}

    

# 主界面
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():    
    return render_template('index.html')

# 用户管理界面
@app.route('/manage',methods=['GET', 'POST'])
def manage():
    if request.method == 'POST':
        # 获取按钮的名称或值
        action = request.form.get('action')
        if action == 'delete':
            id = request.form.get('id')
            
            if id:
                # 执行删除数据库中数据的操作
                sql = "DELETE FROM member WHERE username=%s"
                execute_query(sql, [id])
                print("删除成功")
                
                return 'OK'
            else:
                print("ID 参数缺失")
                return 'ID 参数缺失', 400  # 返回错误状态码和信息
        elif action == 'add':
            # 获取表单数据
            username = request.form.get('username')
            account = request.form.get('id')
            gender = request.form.get('sex')
            phone = request.form.get('phone')
            email = request.form.get('email')
            role = request.form.get('role')
            status = request.form.get('state')
            # 构造 SQL 插入语句
            sql = "INSERT INTO member (username, account, gender, phone, email, role, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data = execute_query(sql, [username, account, gender, phone, email, role, status])
            
            if username:
                # 执行 SQL 插入语句
                execute_query(sql, data)
                
                print("添加用户成功")
                return 'OK'  # 返回成功响应
            else:
                
                return '添加用户失败', 500  # 返回失败响应和适当的状态码
        else:
            # 处理原有的功能
            # 查询数据库获取数据
            sql = "SELECT * FROM member"
            data = execute_query(sql)
            return render_template('manage.html', data=data)
            
    else:
        # 处理原有的功能
        # 查询数据库获取数据
        sql = "SELECT * FROM member"
        data = execute_query(sql)
        return render_template('manage.html', data=data)
    
# 数据处理界面
@app.route('/processing', methods=['GET', 'POST'])
def processing():
    
    if request.method == 'POST':
        # 获取按钮的名称或值
        action = request.form.get('action')
        if action == 'in-one':
            
            file = request.files['order_file']
            # 保存上传的文件到服务器
            file_path = 'uploads/' + file.filename
            file.save(file_path)
            # 导入 CSV 文件到数据库
            import_csv_to_db1(file_path)
            return 'OK'
            
        elif action == 'in-two':
            file = request.files['weather_file']
            # 保存上传的文件到服务器
            file_path = 'uploads/' + file.filename
            file.save(file_path)
        
            # 导入 CSV 文件到数据库
            import_csv_to_db2(file_path)

            return 'OK'
        elif action == 'in-three':
            file = request.files['section_file']
            # 保存上传的文件到服务器
            file_path = 'uploads/' + file.filename
            file.save(file_path)
            print(file_path)
            # 导入 CSV 文件到数据库
            import_csv_to_db3(file_path)

            return 'OK'
        
        # 这个查询功能还不完善
        elif action == 'query-order':
            year=request.form.get('year')
            month=request.form.get('month')
            day=request.form.get('day')
            if day:
                sql = "SELECT * FROM `order` WHERE YEAR(date) = %s AND MONTH(date) = %s AND DAY(date) = %s"
                data1 = execute_query(sql, [year,month,day])
                sql2 = "SELECT * FROM `weather` ORDER BY create_at LIMIT 10"
                data2 = execute_query(sql2)
                sql3 = "SELECT * FROM `intersection` ORDER BY create_at LIMIT 10"
                data3 = execute_query(sql3)
                return render_template('processing.html',data1=data1,data2=data2,data3=data3)
            else:
                sql = "SELECT * FROM `order` WHERE YEAR(date) = %s AND MONTH(date) = %s"
                data1 = execute_query(sql, [year,month])
                sql2 = "SELECT * FROM `weather` ORDER BY create_at LIMIT 10"
                data2 = execute_query(sql2)
                sql3 = "SELECT * FROM `intersection` ORDER BY create_at LIMIT 10"
                data3 = execute_query(sql3)
                return render_template('processing.html',data1=data1,data2=data2,data3=data3)

        else:
            sql1 = "SELECT * FROM `order` ORDER BY create_at DESC LIMIT 10"
            data1 = execute_query(sql1)
            sql2 = "SELECT * FROM `weather` ORDER BY create_at DESC LIMIT 10"
            data2 = execute_query(sql2)
            sql3 = "SELECT * FROM `intersection` ORDER BY create_at DESC LIMIT 10"
            data3 = execute_query(sql3)
            return render_template('processing.html',data1=data1,data2=data2,data3=data3)
    else:
        sql1 = "SELECT * FROM `order` ORDER BY create_at DESC LIMIT 10"
        data1 = execute_query(sql1)
        sql2 = "SELECT * FROM `weather` ORDER BY create_at DESC LIMIT 10"
        data2 = execute_query(sql2)
        sql3 = "SELECT * FROM `intersection` ORDER BY create_at DESC LIMIT 10"
        data3 = execute_query(sql3)
        return render_template('processing.html',data1=data1,data2=data2,data3=data3)




# 预测界面
@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'query-link':
            startlinkid = request.form.get('startlinkid')
            endlinkid = request.form.get('endlinkid')
            # 定义图数据文件路径
            file_path = os.path.join("static", "data", "graph_data.gpickle")
            # 加载图数据
            with open(file_path, 'rb') as f:
                G = pickle.load(f)
            # 计算节点 1 到节点 4 的最短路径和最短距离
            shortest_path = nx.shortest_path(G, source=startlinkid , target=endlinkid, weight='weight')
            shortest_distance = nx.shortest_path_length(G, source=startlinkid, target=endlinkid, weight='weight')
            distance = shortest_distance
            if distance == float('inf'):
                distance='Infinity'
            print("Shortest Path:", shortest_path)
            print("Shortest Distance:", distance)
            response_data_1 = {
                'startlinkid': startlinkid,
                'endlinkid': endlinkid,
                'average_linktime': distance,
                'path': shortest_path,
            }
            # 返回 JSON 格式的响应数据
            return jsonify(response_data_1)
        elif action == 'query-link-2':
            startlinkid = request.form.get('startlinkid')
            endlinkid = request.form.get('endlinkid')
            slice = int(request.form.get('slice'))
            hour=int(request.form.get('hour'))
            min=int(request.form.get('min'))
            min_slice=int(((hour+16)%24*60+min)/5)
            max_slice=min_slice+slice*3
            sql="""
                SELECT AVG(ata) AS average_ata
                FROM `order`
                WHERE startlink = %s
                AND endlink = %s
                AND sliceid BETWEEN %s AND %s;
                """
            data=execute_query(sql,[startlinkid,endlinkid,min_slice,max_slice])
            response_data_2={
                'startlinkid': startlinkid,
                'endlinkid': endlinkid,
                'average_ata':data[0]
            }
            return jsonify(response_data_2)
    else:
        
        return render_template('forecast.html')

# 登录界面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        sql = "SELECT * FROM `user` WHERE id=%s AND pwd=%s"
        res = execute_query(sql, [username, password], fetchone=True)
        if res:
            return redirect('/menu')
        else:
            flash("账号或密码填写错误")

    return render_template('login.html')


# 注册界面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if username and password == password2:
            sql1 = "SELECT * FROM `user` WHERE id=%s"
            res = execute_query(sql1, [username], fetchone=True)
            if not res:
                sql2 = "INSERT INTO user(id, pwd) VALUES(%s, %s)"
                execute_query(sql2, [username, password])
                flash("注册成功")
                return redirect('/login')
            else:
                flash("账号已存在")

    return render_template('register.html')

if __name__ == "__main__":
    app.run()
