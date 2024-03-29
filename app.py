from flask import Flask, render_template, request, redirect, flash, jsonify
from db import execute_query
from import_csv import import_csv_to_db1, import_csv_to_db2, import_csv_to_db3


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'


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
            linkid = request.form.get('linkid')
            # 查询数据库获取数据
            sql = "SELECT AVG(linktime) AS average_linktime FROM trajectorylink WHERE linkid = %s"
            data = execute_query(sql, [linkid])
            sql ="SELECT ROUND(AVG((linkcurrentstatus + linkarrivalstatus) / 2)) AS average_status FROM trajectorylink WHERE linkid = %s"
            data1 = execute_query(sql,[linkid])
            sql = "SELECT AVG(linkratio) AS average_ratio FROM trajectorylink WHERE linkid = %s"
            data2 = execute_query(sql, [linkid])
            # 将查询结果封装在一个字典中
            response_data = {
                'linkid': linkid,
                'average_linktime': data[0]['average_linktime'],
                'average_status': data1[0]['average_status'],
                'average_ratio': data2[0]['average_ratio']
            }
            # 返回 JSON 格式的响应数据
            return jsonify(response_data)
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
