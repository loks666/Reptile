import pymysql
import jieba.analyse
from matplotlib import pyplot as plt
from stylecloud import gen_stylecloud


def analysis_data():
    # 读取文件
    # pd_data = pd.read_excel('鸿星尔克.xlsx')
    # exist_col = pd_data.dropna()  # 删除空行

    # 读取内容
    values = []
    for key in joblist[0].keys():
        for job in joblist:
            print(values.append(job[key]))
        print(len(values))
        wordlist = jieba.cut_for_search(''.join(values))
        result = ' '.join(wordlist)
        generate_img(result, key + '.jpg')
        values = []
        print('绘制 ' + key + ' 图成功！')
    print('绘图完毕！')


def generate_img(text, img_name):
    gen_stylecloud(text=text,
                   icon_name='fab fa-qq',
                   size=1024,
                   font_path='msyh.ttc',
                   background_color='white',
                   output_name=img_name,
                   custom_stopwords=['有限公司', '万', '月', '经验', '公司', '工程师', '新区', '山区', '区', '人', '科技', '股份', '有限', '信息',
                                     '技术', '科技股份', '信息技术', '公司', '招'])


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


def column():
    plt.hist(df['月工资'], bins=24)
    plt.xlabel('工资(万元)')
    plt.ylabel('次数')
    plt.title('薪资直方图')
    plt.savefig('histogram.jpg')
    plt.show()


def get_joblist():
    con = create_connector()
    # cur = con.cursor()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('Select com_name,com_type,com_count,salary,job_name,job_benefits,job_req,area from 51job')
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


joblist = get_joblist()
# for i in joblist:
#     print(i)
if __name__ == '__main__':
    analysis_data()
    # print()
    # print(joblist[0])
    # for job in joblist:
    #     print(job[0])
