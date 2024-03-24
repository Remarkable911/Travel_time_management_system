import pymysql
from flask import Flask, render_template, request, redirect, flash
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

# 数据库连接配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '',
    'charset': 'utf8',
    'db': 'trip'
}
# 数据库连接函数
def connect_db():
    return pymysql.connect(**DB_CONFIG)
# 执行sql语句
def execute_query(sql, params=None, fetchone=False):
    # 连接数据库
    conn = connect_db()
    # 创建游标对象，使用字典格式返回查询结果
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行SQL查询
    cursor.execute(sql, params)
    # 根据fetchone参数选择返回结果的方式
    if fetchone:
        # 返回一条查询结果
        result = cursor.fetchone()
    else:
        # 返回所有查询结果
        result = cursor.fetchall()
    # 提交事务
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭数据库连接
    conn.close()
    # 返回查询结果
    return result

# 导入数据order
def import_csv_to_db1(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # 跳过标题行
            
            for row in csv_reader:
                # 解析 CSV 文件中的每一行数据
                orderid, ata, distance, simpleeta, driverid, sliceid, date = row
                
                # 构造插入数据的 SQL 语句
                sql = "INSERT INTO `order` (orderid, ata, distance, simpleeta, driverid, sliceid, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                # 执行 SQL 插入操作
                execute_query(sql, (orderid, ata, distance, simpleeta, driverid, sliceid, date))
        
        flash('导入成功')
    except Exception as e:
        flash('导入失败，请检查文件格式')
        print('Error:', e)
# 导入数据weather
def import_csv_to_db2(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # 跳过标题行
            
            for row in csv_reader:
                # 解析 CSV 文件中的每一行数据
                date,weather,hightemp,lowtemp = row
                
                # 构造插入数据的 SQL 语句
                sql = "INSERT INTO `order` (date,weather,hightemp,lowtemp) VALUES (%s, %s, %s, %s)"
                # 执行 SQL 插入操作
                execute_query(sql, (date,weather,hightemp,lowtemp))
        
        flash('导入成功')
    except Exception as e:
        flash('导入失败，请检查文件格式')
        print('Error:', e)
# 导入数据intersection
def import_csv_to_db3(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # 跳过标题行
            
            for row in csv_reader:
                # 解析 CSV 文件中的每一行数据
                crossid,crosstime,entranceid,exitid,orderid = row
                
                # 构造插入数据的 SQL 语句
                sql = "INSERT INTO `order` (crossid,crosstime,entranceid,exitid,orderid) VALUES (%s, %s, %s, %s, %s)"
                # 执行 SQL 插入操作
                execute_query(sql, (crossid,crosstime,entranceid,exitid,orderid))
        
        flash('导入成功')
    except Exception as e:
        flash('导入失败，请检查文件格式')
        print('Error:', e)


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
                flash("删除成功")
                
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
            data = (username, account, gender, phone, email, role, status)
            
            if username:
                # 执行 SQL 插入语句
                execute_query(sql, data)
                
                flash("添加用户成功")
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

            return redirect('/processing')
            
        elif action == 'in-two':
            file = request.files['weather_file']
            # 保存上传的文件到服务器
            file_path = 'uploads/' + file.filename
            file.save(file_path)
        
            # 导入 CSV 文件到数据库
            import_csv_to_db2(file_path)

            return redirect('/processing')
        elif action == 'in-three':
            file = request.files['section_file']
            # 保存上传的文件到服务器
            file_path = 'uploads/' + file.filename
            file.save(file_path)
        
            # 导入 CSV 文件到数据库
            import_csv_to_db3(file_path)

            return redirect('/processing')
    else:
        sql1 = "SELECT * FROM `order` ORDER BY create_at DESC LIMIT 10"
        data1 = execute_query(sql1)
        sql2 = "SELECT * FROM `weather` ORDER BY create_at DESC LIMIT 10"
        data2 = execute_query(sql2)
        sql3 = "SELECT * FROM `intersection` ORDER BY create_at DESC LIMIT 10"
        data3 = execute_query(sql3)
        return render_template('processing.html',data1=data1,data2=data2,data3=data3)

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

if __name__ == '__main__':
    app.run()
