# 对数据文件进行处理
import csv
import os


# 数据分离
def data_segment(filename):
    # 文件路径
    filepath = os.path.join("D:\\", "文档", "学习", "毕设", "giscup_2021", "train", filename)
    date = filename.split('.')[0]
    date = date[:4] + '-' + date[4:6] + '-' + date[6:]
    # csv文件名称
    csv_order = os.path.splitext(filepath)[0] + '_order.csv'
    csv_link = os.path.splitext(filepath)[0] + '_link.csv'
    csv_cross = os.path.splitext(filepath)[0] + '_cross.csv'
    # csv文件首行
    order_title = 'orderid,ata,distance,simpleeta,driverid,sliceid,date,startlink,endlink'
    link_title = 'linkid,linktime,linkratio,linkcurrentstatus,linkarrivalstatus,orderid'
    cross_title = 'crossid,entranceid,exitid,crosstime,orderid'
    # 对文件进行读取和写入
    with open(filepath, 'r') as txtfile, open(csv_order, 'w') as csvorder, open(csv_link, 'w') as csvlink, open(
            csv_cross, 'w') as csvcross:
        # 给每个csv文件加首行
        csvorder.write(order_title + '\n')
        csvlink.write(link_title + '\n')
        csvcross.write(cross_title + '\n')
        # 逐行处理txt文件
        for line in txtfile:
            # 去除行尾的换行符
            line.strip()

            # 根据";;"分割字符串
            data = line.split(";;")
            # order_text:['1073372', '494', '1831.3472', '427', '31472', '114']
            order_text = data[0].split(" ")
            orderid = order_text[0]
            # link_text_one:['614232:7.4838,0.8809,1,0', '538518:1.4087,1.0000,0,0']
            link_text_one = data[1].split(" ")
            # cross_text_one:['41341_118906:30', '118906_472430:30']
            cross_text_one = data[2].strip().split(" ")
            order_text.append(date)
            order_text.append(link_text_one[0].split(':')[0])
            # cross数据格式
            if cross_text_one[0] != '':
                for cross in cross_text_one:
                    cross_text_two = cross.split(':')
                    entanceid = cross_text_two[0].split('_')[0]
                    exitid = cross_text_two[0].split('_')[1]
                    cross_text_two.insert(1, entanceid)
                    cross_text_two.insert(2, exitid)
                    cross_text_two.append(orderid)
                    cross_text_str = ','.join(cross_text_two)
                    csvcross.write(cross_text_str + '\n')
            # link数据格式
            for link in link_text_one:
                link_text_two = link.split(':')
                link_text_three = []
                for part in link_text_two:
                    link_text_three.extend(part.split(','))
                # link_text_three:['93457', '0.7200', '0.2480', '1', '0', '1073372']
                link_text_three.append(orderid)
                link_text_str = ','.join(link_text_three)
                csvlink.write(link_text_str + '\n')
            # order_text:['1073372', '494', '1831.3472', '427', '31472', '114', '600156', '93457']
            order_text.append(link_text_two[0])
            order_text_str = ','.join(order_text)
            csvorder.write(order_text_str + '\n')
    print('数据分割结束，生成三个文件')


if __name__ == '__main__':
    data_segment("20200801.txt")
