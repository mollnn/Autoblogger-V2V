import pymysql
from sshtunnel import SSHTunnelForwarder


def SSHMysql(DB, SQL, isDict=False, argu=tuple()):
    server = SSHTunnelForwarder(
        ssh_address_or_host=('131.mollnn.com', 22),  # 指定ssh登录的跳转机的address
        ssh_username='wzc',  # 跳转机的用户
        ssh_password='123456',  # 跳转机的密码
        local_bind_address=('127.0.0.1', 1268),  # 映射到本机的地址和端口
        remote_bind_address=('localhost', 3306))  # 数据库的地址和端口
    server.start()  # 启用SSH
    db = pymysql.connect(
        host="127.0.0.1",  # 映射地址local_bind_address IP
        port=1268,  # 映射地址local_bind_address端口
        user="root",
        passwd="123456",
        database=DB,  # 需要连接的实例名
        charset='utf8',
                cursorclass=pymysql.cursors.DictCursor if isDict == True else pymysql.cursors.Cursor)
    cursor = db.cursor()
    if argu == tuple():
        cursor.execute(SQL.encode('utf8'))  # 执行SQL
    else:
        cursor.execute(SQL.encode('utf8'), argu)  # 执行SQL
    data = cursor.fetchall()  # 获取查询结果
    cursor.close()
    db.commit()
    db.close()
    server.close()
    return data


def query(DB, SQL, isDict=False, argu=tuple()):
    return SSHMysql(DB, SQL, isDict, argu)


if __name__ == "__main__":
    SQL = "SELECT * FROM Danmu;"
    SelectResult = SSHMysql('bilibili', SQL)
    print(SelectResult)
