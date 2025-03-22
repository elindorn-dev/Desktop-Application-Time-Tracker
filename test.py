import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random

names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']  # Пример с большим количеством баров
values = [10, 15, 7, 12, 9, 14, 11, 8, 13, 6, 16, 5]

num_bars = len(names)
num_colors = num_bars * 2  # Генерируем в два раза больше цветов, чем баров

cmap = cm.get_cmap('viridis', num_colors)  # или другая цветовая карта
colors = [cmap(i) for i in range(num_colors)]
random.shuffle(colors)

bars = plt.bar(names, values)

for i, bar in enumerate(bars):
    bar.set_color(colors[i % len(colors)])  # Используем modulo, чтобы не выйти за пределы списка цветов

plt.show()