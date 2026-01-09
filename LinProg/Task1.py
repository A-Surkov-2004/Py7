"""
A - смартфоны
B - планшеты

P = 8000A+12000B

время
2A +3B <= 240

память
4A + 6B <= 480

акумы
1A + 2B <= 150

A >= 0
B >= 0

L(x, μ) = -8000*x1 - 12000*x2 + μ1(2x1 + 3*x2 - 240) + μ2*(4*x1 + 6*x2 - 480) + μ3*(x1 + 2*x2 - 150) + μ4*(-x1) + μ5*(-x2)

μi - ценность дополнительной еденицы конкретного ресурса. Насколько увеличится прибыль если этого ресурса станет на 1 больше.

"""

import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

# Целевая функция (коэффициенты для минимизации -P)
c = [-8000, -12000]

# Ограничения: A_ub @ x <= b_ub
A_ub = [
    [2, 3],    # процессорное время
    [4, 6],    # память
    [1, 2]     # аккумуляторы
]
b_ub = [240, 480, 150]

# Границы переменных
bounds = [(0, None), (0, None)]

# Решение
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

# Вывод
print(f"Оптимальное количество смартфонов (x₁): {result.x[0]:.0f}")
print(f"Оптимальное количество планшетов (x₂): {result.x[1]:.0f}")
print(f"Максимальная прибыль: {-result.fun:.2f} руб.")

print("\n")
print(f"Процессорное время: {2*result.x[0] + 3*result.x[1]:.1f} / 240 часов")
print(f"Оперативная память: {4*result.x[0] + 6*result.x[1]:.1f} / 480 ГБ")
print(f"Аккумуляторы: {result.x[0] + 2*result.x[1]:.1f} / 150 шт.")




# Визуализация
fig, ax = plt.subplots(figsize=(10, 8))
x1 = np.linspace(0, 150, 400)

x2_cpu = (240 - 2*x1) / 3
x2_ram = (480 - 4*x1) / 6
x2_bat = (150 - x1) / 2


ax.plot(x1, x2_cpu, label=r'Процессорное время: $2x_1 + 3x_2 \leq 240$', color='blue', linewidth=2)
ax.plot(x1, x2_ram, label=r'Память: $4x_1 + 6x_2 \leq 480$', color='green', linewidth=2)
ax.plot(x1, x2_bat, label=r'Аккумуляторы: $x_1 + 2x_2 \leq 150$', color='red', linewidth=2)

vertices = [
    (0, 0),
    (120, 0),
    (0, 75),
    (0, 80),
]

vertices.append((30, 60))

poly_vertices = [(0,0), (120,0), (30,60), (0,75)]

from matplotlib.patches import Polygon
polygon = Polygon(poly_vertices, alpha=0.2, color='gray', label='Допустимая область')
ax.add_patch(polygon)

x1_opt, x2_opt = result.x
ax.plot(x1_opt, x2_opt, 'ro', markersize=10, label=f'Оптимум: ({x1_opt:.0f}, {x2_opt:.0f})')

for profit in [600000, 800000, 1000000, 1200000]:
    x2_profit = (profit - 8000*x1) / 12000
    ax.plot(x1, x2_profit, 'k--', alpha=0.3, linewidth=0.8)
    idx = len(x1)//2
    ax.text(x1[idx], x2_profit[idx]+3, f'{profit/1000:.0f} тыс.', fontsize=9, alpha=0.7)

ax.set_xlim(0, 150)
ax.set_ylim(0, 100)
ax.set_xlabel('$x_1$ (смартфоны)', fontsize=12)
ax.set_ylabel('$x_2$ (планшеты)', fontsize=12)
ax.set_title('Задача оптимизации производства: Геометрическое представление', fontsize=14)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
plt.show()