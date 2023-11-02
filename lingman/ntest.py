import pyodbc

# 构建连接字符串
server = 'lz'
port = 1433
database = 'sqlserver_test'
username = 'sa'
password = 'Pass@word'
driver = 'ODBC Driver 17 for SQL Server'  # 根据您的 SQL Server 版本选择正确的驱动程序

if __name__ == '__main__':

    connection_string = f"DRIVER={{{driver}}};SERVER={server},{port};DATABASE={database};UID={username};PWD={password}"

    try:
        # 建立与数据库的连接
        conn = pyodbc.connect(connection_string)

        # 创建游标对象
        cursor = conn.cursor()

        # 执行 SQL 查询
        query = "SELECT * FROM Categories"
        cursor.execute(query)

        # 获取查询结果
        rows = cursor.fetchall()

        # 处理查询结果
        for row in rows:
            print(row)

    except pyodbc.Error as e:
        print("发生错误:", e)

    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()
