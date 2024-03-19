import pymysql
from flask import Flask, render_template, request, redirect, flash

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

# 主界面
@app.route('/', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        id = request.form.get('keyword')
        sql = "SELECT * FROM `order` WHERE orderid=%s"
        res = execute_query(sql, [id], fetchone=True)
        print(res)
    return render_template('menu.html')

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
            print(username, account, gender, phone, email, role, status)
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
