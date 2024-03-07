import pymysql

#1.连接mysql
conn=pymysql.connect(host='127.0.0.1', port=3306,user='root',password='',charset='utf8',db='trip')
cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)

#2.发送指令
cursor.execute("select * from weather")
conn.commit()


#3.关闭连接
cursor.close
conn.close()