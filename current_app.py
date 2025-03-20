from win32gui import GetWindowText, GetForegroundWindow # для получения имени текущего окна
import time # для счёта времени
import psutil # получение имени процесса по id
import win32process # получение id процесса
#from datetime import datetime
import sqlite3


def get_active_window_process_name():
    '''
    Функция для определения имени текущего приложения (процесса)
    '''
    try:
        hwnd = GetForegroundWindow() # Получение имени текущего окна с панели задач
        _, process_id = win32process.GetWindowThreadProcessId(hwnd) # получение id 
        process = psutil.Process(process_id) # получение объекта процесса
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as err: # Обработка на exist, access, процесс завершения
        return err.msg

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

if __name__ == "__main__":
    connection = connect_to_db()
    time_apps = fill_dictionary(connection) # словарь для сохранения данных {"имя": время}
    if connection:
        create_table(connection)
        
        previews_app_name = None
        while True:
            try:
                app_name = get_active_window_process_name() # название процесса
                
                if app_name not in time_apps: # проверка существования в словаре, добавление если нет
                    time_apps[app_name] = 0

                    add_record(connection, (app_name, time_apps[app_name]))    
                time_apps[app_name] += 1 # добавление значения

                if previews_app_name != None and app_name != previews_app_name:
                    update_record(connection, data=(time_apps[previews_app_name], previews_app_name)) # Если было прошлое название и текущее не равно прошлому

                previews_app_name = app_name # фиксируем прошлое

                output_str = f"{app_name}: {time_apps[app_name]} sec." # строка вывода
                print(output_str,(70 - len(output_str))*" ", end="", flush=True) # вывод с возвратом коретки
                print("\r", end="", flush=True),
            except Exception as err:
                print('error:', err)

            time.sleep(1) # задержка в 1 секунду