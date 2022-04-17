import pandas as pd
import pymysql


def get_data(sql):
    try:
        con = pymysql.connect(
            host='localhost',
            user='root',
            password='Lx284190056',
            database='post',
            charset='utf8',
            # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
        )
        cur = con.cursor()  # 获取操作游标，也就是开始操作
        cur.execute(sql)  # 输入要查询的SQL
        col_result = cur.description  # 获取查询结果的字段描述
        rel = cur.fetchall()

        # 获取字段名，以列表形式保存
        column_names = []
        for i in range(0, len(col_result)):
            column_names.append(col_result[i][0])
        cur.close()
        con.close()
        return rel, column_names
    except Exception as e:
        print(e)
        print("!!!!!!!!!!!!!!请检查数据库连接信息!!!!!!!!!!!!!!")
        exit(-1)


if __name__ == '__main__':
    sql = 'Select com_name,com_type,com_count,salary,job_name,job_benefits,job_req,area from 51job'
    rel, columns = get_data(sql)
    data1 = list(map(list, rel))
    df = pd.DataFrame(data=data1, columns=columns)  # mysql查询的结果为元组，需要转换为列表
    df.to_csv('51job.csv', index=None)
