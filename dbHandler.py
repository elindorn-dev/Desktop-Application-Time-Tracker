import sqlite3

def connect_to_db():
    '''
    Подключение к бд 
    '''
    db_name="apptime_tracker.db" 
    try:
        conn = sqlite3.connect(db_name)
        print(f"Успешное подключение к базе данных: {db_name}")
        return conn
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None

def create_table(conn):
    '''
    Создание таблицы в базе данных или создание ее, если она не существует
    '''
    if conn is None:
        return False

    cursor = conn.cursor()
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS apptime (
        apptime_id INTEGER PRIMARY KEY AUTOINCREMENT,
        apptime_name TEXT,
        apptime_time INTEGER
    )
    """

    try:
        cursor.execute(create_table_sql) 
        conn.commit()
        print(f"Таблица создана/обновлена успешно.")
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")
        return False

def fill_dictionary(conn):
    '''
    Заполнение словаря существующими записями
    '''
    cur = conn.cursor()
    try:
        cur.execute("SELECT apptime_name, apptime_time FROM apptime")
    except sqlite3.Error as e:
        print(f"Ошибка при выборе записей: {e}")
        return False
    rows = cur.fetchall() # берём строки с полученной таблицы

    data_dict = {}  # Создаем пустой словарь
    if len(rows) > 0:
        for row in rows:
            apptime_name, apptime_time = row  # Распаковываем кортеж
            data_dict[apptime_name] = apptime_time  # Добавляем в словарь
        return data_dict
    return {}

def add_record(conn, data=("none", 0)):
    '''
    Добавление записи в таблицу
    '''
    if conn is None or data[0] == "none":
        return False

    cursor = conn.cursor()
    insert_sql = f"""
    INSERT INTO apptime (apptime_name, apptime_time) VALUES (?, ?)
    """
    try:
        cursor.execute(insert_sql, data)
        conn.commit()
        print(f"Добавлено новое приложение")
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении записи: {e}")
        return False

def update_record(conn, data):
    '''
    Редактирование времени в приложении
    '''
    if conn is None:
        return False

    cursor = conn.cursor()
    update_sql = f"""
    UPDATE apptime
    SET apptime_time = ?
    WHERE apptime_name = ?
    """
    try:
        cursor.execute(update_sql, data)
        conn.commit()
        print(f"Изменение времени {data[1]}")
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при изменения времени: {e}")
        return False