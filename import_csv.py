import csv
from db import execute_query
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
                sql = "INSERT INTO `order` (orderid, ata, distance, simpleeta, driverid, sliceid, date, create_at) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())"
                # 执行 SQL 插入操作
                execute_query(sql, (orderid, ata, distance, simpleeta, driverid, sliceid, date))
        
        print('导入成功')
    except Exception as e:
        
        print('导入失败,Error:', e)
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
                sql = "INSERT INTO `weather` (date,weather,hightemp,lowtemp,create_at) VALUES (%s, %s, %s, %s,NOW())"
                # 执行 SQL 插入操作
                execute_query(sql, (date,weather,hightemp,lowtemp))
        
        print('导入成功')
    except Exception as e:
        print('导入失败,Error:', e)
        
# 导入数据intersection
def import_csv_to_db3(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            print(csv_reader)
            next(csv_reader)  # 跳过标题行
            
            for row in csv_reader:
                # 解析 CSV 文件中的每一行数据
                crossid,entranceid,exitid,crosstime,orderid = row
                print(row)
                # 构造插入数据的 SQL 语句
                sql = "INSERT INTO `intersection` (crossid,entranceid,exitid,crosstime,orderid,create_at) VALUES (%s, %s, %s, %s, %s,NOW())"
                # 执行 SQL 插入操作
                execute_query(sql, (crossid,entranceid,exitid,crosstime,orderid))
        print('导入成功')
    except Exception as e:
        print('导入失败,Error:', e)
