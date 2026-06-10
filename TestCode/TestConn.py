import pymysql


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


def add_author(author_id, author_name):
    conn = get_connection()
    cursor = conn.cursor()

    sql = 'INSERT INTO author(author_id, author_name) VALUES (%s, %s)'
    cursor.execute(sql, (author_id, author_name,))

    conn.commit()
    print(f'已添加{author_name}的书籍')

    cursor.close()
    conn.close()


def add_isbn(isbn_id):
    conn = get_connection()
    cursor = conn.cursor()

    sql = 'INSERT INTO isbn(isbn_id) VALUES (%s)'
    cursor.execute(sql, (isbn_id,))

    conn.commit()
    print(f'ISBN为{isbn_id}')

    cursor.close()
    conn.close()


def list_book():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()


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


def update_book_title(book_id, new_title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT title FROM books WHERE id = %s', (book_id,))
    old = cursor.fetchone()

    if not old:
        print(f'错误: ID为{book_id}的书不存在')
        cursor.close()
        conn.close()
        return

    old_title = old[0]

    cursor.execute('UPDATE books SET title = %s WHERE id = %s', (new_title, book_id))
    conn.commit()

    print(f'《{old_title}》 的书名已修改为《{new_title}》')

    cursor.close()
    conn.close()


if __name__ == '__main__':
    # add_book('MySQL')
    # add_author(1, 'MySQL')
    # add_isbn(1)
    list_book()
