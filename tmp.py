import pymysql
from flask import Flask, render_template, request, redirect, flash
from pymysql import Connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ADJL'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 1.连接mysql
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset='utf8', db='trip')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 2.发送指令
        sql = "select * from `user` where id=%s and pwd=%s"
        cursor.execute(sql, [username, password])
        res = cursor.fetchone()

        if res is not None:
            return redirect('/menu')
        else:
            flash("账号或密码填写错误")

    return render_template('login.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        id = request.form.get('keyword')
        # 1.连接mysql
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset='utf8', db='trip')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 2.发送指令
        sql = "select * from `order` where orderid=%s"
        cursor.execute(sql, [id, ])
        res = cursor.fetchone()
        print(res)

    return render_template('menu.html')


@app.route('/manage')
def manage():
    return render_template('manage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if username is not None and password == password2:
            # 1.连接mysql
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset='utf8', db='trip')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            # 2.发送指令
            sql1 = "select * from `user` where id=%s"
            cursor.execute(sql1, [username])
            res = cursor.fetchone()
            if res is None:

                sql2 = "insert into user(id,pwd) VALUES(%s,%s)"
                cursor.execute(sql2, [username, password])
                conn.commit()
                flash("注册成功")
                return render_template('login.html')
            else:
                flash("账号已存在")

    return render_template('register.html')


if __name__ == '__main__':
    app.run()
