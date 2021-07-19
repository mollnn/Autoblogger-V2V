import pymysql
from sshtunnel import SSHTunnelForwarder
import time

def SSHMysql(DB, SQL, isDict=False):
    flag=0
    data=[]
    for i in range(20):
        print("try")
        try:
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
                database=DB, 
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor if isDict==True else pymysql.cursors.Cursor)
            cursor = db.cursor()
            cursor.execute(SQL.encode('utf8')) 
            data = cursor.fetchall()
            cursor.close()
            db.close()
            server.close()
            break
        except Exception:
            flag=0
        else:
            flag=0
        time.sleep(0.1)
    return data


def query(DB, SQL, isDict=False):
    return SSHMysql(DB, SQL, isDict=isDict)



if __name__ == "__main__":
    SQL = "SELECT * FROM Danmu;"
    SelectResult = SSHMysql('bilibili', SQL)
    print(SelectResult)
