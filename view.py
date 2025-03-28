import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
from dbHandler import *

def view_chart():
    '''
    Показ графика со статистикой
    '''
    connection = connect_to_db()
    apptimes = fill_dictionary(conn=connection)
    connection.close()
    names = list(apptimes.keys())
    values = list(apptimes.values())
    amount = sum(values)
    # Создание столбчатой диаграммы
    plt.figure(figsize=(8, 6))
    bars = plt.bar(names, values) 

    # Работа с цветами
    num_colors = len(names)

    cmap = cm.get_cmap('viridis', num_colors)
    colors = [cmap(i) for i in range(num_colors)]
    random.shuffle(colors)

    for i, bar in enumerate(bars):  
        bar.set_color(colors[i % len(colors)])
        yval = bar.get_height() 
        plt.text(bar.get_x() + bar.get_width()/2, yval, f"{int(values[i]/amount*100)}%", ha='center', va='bottom')  # Добавление текста над столбцами

    # Настройка графика
    plt.ylabel('Секунды')
    plt.title('Трекер времени активных приложений')
    plt.ylim(0, max(values) + 10) # Задание минимального и максимального значения оси Y, чтобы столбки не слипались
    plt.tight_layout()

    # Отображение графика
    plt.show()

view_chart()
