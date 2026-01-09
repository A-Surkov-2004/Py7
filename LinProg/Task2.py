"""
x_11 — количество МТО (тонн), перевозимое со Склада 1 на Базу Альфа

x_12 — количество МТО со Склада 1 на Базу Бета

x_13 — количество МТО со Склада 1 на Базу Гамма

x_21 — количество МТО со Склада 2 на Базу Альфа

x_22 — количество МТО со Склада 2 на Базу Бета

x_23 — количество МТО со Склада 2 на Базу Гамма


Z(x) = 8*x_11 + 6*x_12 + 10*x_13 + 9*x_21 + 7*x_22 + 5*x_23


Ограничения:
Склад 1: x_11 + x_12 + x_13 = 150
Склад 2: x_21 + x_22 + x_23 = 250

База Альфа: x_11 + x_21 = 120
База Бета: x_12 + x_22 = 180
База Гамма: x_13 + x_23 = 100


Проверка сбалансированности задачи:
    Общий запас МТО на складах: 150 + 250 = 400 тонн
    Общая потребность баз: 120 + 180 + 100 = 400 тонн
Задача сбалансированная (закрытая)
"""

from scipy.optimize import linprog
c = [8, 6, 10, 9, 7, 5]
A_eq = [
    [1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1]
]
b_eq = [150, 250, 120, 180, 100]


bounds = [(0, None), (0, None), (0, None), (0, None), (0, None), (0, None)]
result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')



print("\n План по которому все идет:")
print(f"x_11 (Склад 1 → Альфа): {result.x[0]:.1f} тонн")
print(f"x_12 (Склад 1 → Бета): {result.x[1]:.1f} тонн")
print(f"x_13 (Склад 1 → Гамма): {result.x[2]:.1f} тонн")
print(f"x_21 (Склад 2 → Альфа): {result.x[3]:.1f} тонн")
print(f"x_22 (Склад 2 → Бета): {result.x[4]:.1f} тонн")
print(f"x_23 (Склад 2 → Гамма): {result.x[5]:.1f} тонн")
print(f"\nМинимальная стоимость транспортировки: {result.fun:.0f} усл. ед.")


print("\nПроверка")
print(f"Склад 1 отгружено: {result.x[0] + result.x[1] + result.x[2]:.0f} / 150 тонн")
print(f"Склад 2 отгружено: {result.x[3] + result.x[4] + result.x[5]:.0f} / 250 тонн")
print(f"База Альфа получено: {result.x[0] + result.x[3]:.0f} / 120 тонн")
print(f"База Бета получено: {result.x[1] + result.x[4]:.0f} / 180 тонн")
print(f"База Гамма получено: {result.x[2] + result.x[5]:.0f} / 100 тонн")


import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(14, 10))


warehouses = {'Склад 1': (2, 8), 'Склад 2': (2, 3)}
bases = {'Альфа': (10, 10), 'Бета': (10, 5.5), 'Гамма': (10, 1)}


for name, (x, y) in warehouses.items():
    stock = 150 if name == 'Склад 1' else 250
    rect = patches.Rectangle((x - 1.5, y - 0.8), 3, 1.6, linewidth=2,
                             edgecolor='darkblue', facecolor='lightblue', alpha=0.7)
    ax.add_patch(rect)
    ax.text(x, y, f'{name}\n{stock} тонн', ha='center', va='center',
            fontsize=12, fontweight='bold')


for name, (x, y) in bases.items():
    demand = 120 if name == 'Альфа' else (180 if name == 'Бета' else 100)
    rect = patches.Rectangle((x - 1.5, y - 0.8), 3, 1.6, linewidth=2,
                             edgecolor='darkred', facecolor='lightcoral', alpha=0.7)
    ax.add_patch(rect)
    ax.text(x, y, f'База {name}\n{demand} тонн', ha='center', va='center',
            fontsize=12, fontweight='bold')


flows = [
    ('Склад 1', 'Альфа', result.x[0], 8),
    ('Склад 1', 'Бета', result.x[1], 6),
    ('Склад 1', 'Гамма', result.x[2], 10),
    ('Склад 2', 'Альфа', result.x[3], 9),
    ('Склад 2', 'Бета', result.x[4], 7),
    ('Склад 2', 'Гамма', result.x[5], 5)
]


for flow in flows:
    from_node, to_node, volume, cost = flow
    if volume > 0:
        start = warehouses[from_node]
        end = bases[to_node.split()[-1]]
        linewidth = 0.5 + volume / 50

        if cost <= 6:
            color = 'green'
        elif cost <= 8:
            color = 'orange'
        else:
            color = 'red'

        arrow = patches.FancyArrowPatch(start, end,
                                        arrowstyle='->',
                                        linewidth=linewidth,
                                        color=color,
                                        alpha=0.7,
                                        connectionstyle="arc3,rad=0.1")
        ax.add_patch(arrow)
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y, f'{volume:.0f}т\n({cost} у.е.)',
                ha='center', va='center',
                fontsize=9, bbox=dict(boxstyle="round,pad=0.3",
                                      facecolor="white", alpha=0.8))

ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Оптимальный план снабжения военных баз', fontsize=16, fontweight='bold')

# Миф
legend_elements = [
    patches.Patch(facecolor='lightblue', edgecolor='darkblue', label='Склады'),
    patches.Patch(facecolor='lightcoral', edgecolor='darkred', label='Базы'),
    patches.FancyArrowPatch((0, 0), (0, 0), color='green', linewidth=2, label='Низкая стоимость (≤6)'),
    patches.FancyArrowPatch((0, 0), (0, 0), color='orange', linewidth=2, label='Средняя стоимость (7-8)'),
    patches.FancyArrowPatch((0, 0), (0, 0), color='red', linewidth=2, label='Высокая стоимость (≥9)')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

plt.tight_layout()
plt.show()