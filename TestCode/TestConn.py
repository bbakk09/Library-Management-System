import pymysql

# 用pymysql的connect来连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Mysql135',
    database='library'
)

# 创建一个游标, 来执行SQL
cursor = conn.cursor()

cursor.execute('SELECT * FROM books')

rows = cursor.fetchall()
print(rows)

cursor.close()
conn.close()


def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Mysql135',
        database='library'
    )


def add_book(title):
    conn = get_connection()
    cursor = conn.cursor()

    # 插入数据的SQL
    sql = 'INSERT INTO books (title) VALUES (%s)'
    # 注意: 参数必须是一个元组, 所以单元素要加逗号
    cursor.execute(sql, (title,))

    # 提交事务, 数据才会写入
    conn.commit()
    print(f'《{title}》 添加成功! ')

    cursor.close()
    conn.close()


add_book('MySQL基础')


def list_book():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()


list_book()


def search_books(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    sql = 'SELECT id, title FROM books WHERE title LIKE %s'
    like_pattern = f'%{keyword}%'
    cursor.execute(sql, (like_pattern,))

    results = cursor.fetchall()
    if results:
        print(f'找到{len(results)}本书: ')
        for book_id, title in results:
            print(f'ID: {book_id} - 《{title}》')
    else:
        print("没有找到相关图书")

    cursor.close()
    conn.close()


search_books('Python')
search_books('入门')

def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT title FROM books where id = %s', (book_id,))
    book = cursor.fetchone()

    if not book:
        print(f'错误: ID为{book_id} 的书不存在')
        cursor.close()
        conn.close()
        return

    title = book[0]

    cursor.execute('DELETE FROM books WHERE id = %s', (book_id,))
    conn.commit()

    print(f'《{title}》已成功删除')

    cursor.close()
    conn.close()

delete_book(1)


