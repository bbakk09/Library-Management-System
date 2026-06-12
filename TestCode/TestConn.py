import pymysql


def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Mysql135',
        database='library'
    )


def add_book(title, total_copies=1):
    conn = get_connection()
    cursor = conn.cursor()

    sql = 'INSERT INTO books (title, total_copies, available_copies) VALUES (%s, %s, %s)'
    cursor.execute(sql, (title, total_copies, total_copies))

    conn.commit()
    print(f'《{title}》添加成功，总册数：{total_copies}，可借：{total_copies}')

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


def borrow_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()

    # 查询当前可借册数
    cursor.execute("SELECT title, available_copies FROM books WHERE id = %s", (book_id,))
    result = cursor.fetchone()

    if not result:
        print("图书不存在")
        cursor.close()
        conn.close()
        return

    title, available = result
    if available <= 0:
        print(f"《{title}》已经没有可借的册数了")
        cursor.close()
        conn.close()
        return

    # 可借，则减少1
    cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE id = %s", (book_id,))
    conn.commit()
    print(f"《{title}》借阅成功！剩余可借：{available - 1}册")

    cursor.close()
    conn.close()


def return_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT title, available_copies, total_copies FROM books WHERE id = %s", (book_id,))
    result = cursor.fetchone()

    if not result:
        print("图书不存在")
        cursor.close()
        conn.close()
        return

    title, available, total = result
    if available >= total:
        print(f"《{title}》所有册数都在库，无需归还")
        cursor.close()
        conn.close()
        return

    cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE id = %s", (book_id,))
    conn.commit()
    print(f"《{title}》归还成功！当前可借：{available + 1}册")

    cursor.close()
    conn.close()


if __name__ == '__main__':
    # 先添加一本有3册的书（假设id自动生成）
    add_book("Python编程", 3)

    # 查看所有图书，确认可借册数
    list_book()

    # 借书（假设该书id为1，请根据实际id修改）
    borrow_book(1)
    list_book()

    # 还书
    return_book(1)
    list_book()
