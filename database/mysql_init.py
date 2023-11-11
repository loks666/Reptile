import pymysql


class MySQLHandler:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def execute_sql(self, sql, *args):
        if args:
            self.cursor.execute(sql, args)
        else:
            self.cursor.execute(sql)
        self.connection.commit()

    def query_data(self, sql, *args):
        if args:
            self.cursor.execute(sql, args)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def executemany(self, sql, values):
        self.cursor.executemany(sql, values)
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
