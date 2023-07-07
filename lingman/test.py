import pyodbc

# 构建连接字符串
server = 'lz'
port = 1433
database = 'sqlserver_test'
username = 'sa'
password = 'Pass@word'
driver = 'ODBC Driver 17 for SQL Server'
connection_string = f"DRIVER={{{driver}}};SERVER={server},{port};DATABASE={database};UID={username};PWD={password}"
# 建立与数据库的连接
conn = pyodbc.connect(connection_string)

# 创建游标对象
cursor = conn.cursor()

if __name__ == '__main__':
    # Sample select query
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()
