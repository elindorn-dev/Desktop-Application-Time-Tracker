from win32gui import GetWindowText, GetForegroundWindow # для получения имени текущего окна
import time # для счёта времени
import psutil # получение имени процесса по id
import win32process # получение id процесса
#from datetime import datetime
from dbHandler import *


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

if __name__ == "__main__":
    connection = connect_to_db()
    if connection:
        create_table_apptime(connection)
        time_apps = fill_dictionary(connection) # словарь для сохранения данных {"имя": время}
        while True:
            try:
                app_name = get_active_window_process_name() # название процесса
                
                if app_name not in time_apps: # проверка существования в словаре, добавление если нет
                    time_apps[app_name] = 0

                    if not add_record(connection, (app_name, time_apps[app_name])):
                        break    
                time_apps[app_name] += 1 # добавление значения
                if not update_record(connection, data=(time_apps[app_name], app_name)):
                    break

                output_str = f"{app_name}: {time_apps[app_name]} sec." # строка вывода
                print(output_str,(70 - len(output_str))*" ", end="", flush=True) # вывод с возвратом коретки
                print("\r", end="", flush=True),
            except Exception as err:
                print('error:', err)

            time.sleep(1) # задержка в 1 секунду