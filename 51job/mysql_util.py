import pymysql


def init_connector():
    # 创建链接数据库
    config = {'host': '127.0.0.1',  # 默认127.0.0.1
              'user': 'root',
              'password': 'Lx284190056',
              'port': 3306,  # 默认即为3306
              'database': 'post',
              'charset': 'utf8'  # 默认即为utf8
              }
    try:
        return pymysql.connector.connect(**config)  # connect方法加载config的配置进行数据库的连接，完成后用一个变量进行接收
    except pymysql.connector.Error as e:
        print('数据库链接失败！', str(e))
    else:  # try没有异常的时候才会执行
        print("successfully!")


connector = init_connector()


def create_connector():
    # 连接数据库
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Lx284190056',
        database='post',
        charset='utf8',
        # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
    )
    return conn


def create_table(cnn):
    # 建表
    sql_create_table = 'CREATE TABLE`student`\
    (`id`int(10)NOT NULL AUTO_INCREMENT,\
    `name`varchar(10) DEFAULT NULL,\
    `age`int(3) DEFAULT NULL,\
    PRIMARY KEY(`id`))\
    ENGINE=MyISAM DEFAULT CHARSET = utf8'

    # 获取执行的权限，利用数据库连接的返回，调用cursor方法获取一个标记位，再去操作数据库
    # 再通过标记位，去操作数据库
    cursor = cnn.cursor(buffered=True)  # buffered=True会把结果集保存到本地并一次性返回，这样可以提高性能
    try:
        cursor.execute(sql_create_table)  # 执行sql语句
    except pymysql.connector.Error as e:
        print('创建表失败！', str(e))


def insert():
    # 插入数据库
    cursor = cnn.cursor(buffered=True)  # 获取插入的标记位
    try:
        # 第一种：直接字符串插入方式
        # 表中的id是自增长,所以不用传id
        # sql_insert1="insert into student(name,age) values ('orange',20)"
        # cursor.execute(sql_insert1)

        # 第二种：元组连接插入方式
        sql_insert2 = "insert into student(name,age) values (%s,%s)"
        # 此处的%s为占位符，而不是格式化字符串，所以age用%s
        data = ('xiongrun', 18)  # 元组的形式传入两个值
        cursor.execute(sql_insert2, data)  # 执行插入

        # 数据库的存储一类引擎为Innodb，执行完成后需执行commit进行事务提交
        # cnn.commit()
        # cursor.execute('commit')

        # 当前的练习用的存储引擎为MyISAM，不用执行commit
        # 执行execute时就已经执行事务提交

        # 第三种：可以一次插入多条，效率比一条条插高,用的方法是executemany
        stmt = 'insert into student(name,age) values (%s,%s)'
        data = [
            ('xiongrun1', 21),
            ('xiongrun2', 22),
            ('xiongrun3', 21)]
        cursor.executemany(stmt, data)


    except pymysql.connector.Error as e:
        print('插入数据报错！', str(e))
    finally:  # 无论如何都会执行下面的语句
        cursor.close()  # 关闭标记位
        cnn.close()  # 关闭数据库链接


def select(cnn):
    # 查询
    cursor = cnn.cursor(buffered=True)  # 获取查询的标记位
    # noinspection PyBroadException
    try:
        # 第一种
        sql_query1 = 'select * from student'
        cursor.execute(sql_query1)  # 固定格式,记住
        values = cursor.fetchall()  # 符合条件的所有数据，全部赋值给values
        print('所有数据：', values[0][0])
    except pymysql.connector.Error as e:
        print('查询数据报错！', str(e))
    finally:
        cursor.close()  # 关闭标记位
        connector.close()  # 关闭数据库链接


if __name__ == '__main__':
    cnn = init_connector()
    # create_table(cnn)
    select(cnn)
