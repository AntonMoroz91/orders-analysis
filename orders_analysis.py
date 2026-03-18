import json

# Чтение файла
with open('orders_july_2023.json', 'r', encoding='utf-8') as f:
    orders = json.load(f)

# Переменные для подсчета
max_price_order = None
max_price_val = 0

max_quantity_order = None
max_quantity_val = 0

day_stats = {}
user_orders_count = {}
user_total_spent = {}

total_revenue = 0
total_items = 0
total_orders = 0

# Обработка каждого заказа
for order_id, data in orders.items():
    # Нормализуем ключи
    date = data.get('date') or data.get('дата')
    if not date:
        continue

    # Разбираем дату в формате ГГГГ-ДД-ММ
    parts = date.split('-')
    if len(parts) != 3:
        continue
    year, day, month = parts

    # Оставляем только июль 2023 года
    if year != '2023' or month != '07':
        continue

    user_id = data.get('user_id') or data.get('идентификатор_пользователя')
    quantity = data.get('quantity') or data.get('количество')
    price = data.get('price') or data.get('цена')

    # Проверяем наличие данных
    if None in (user_id, quantity, price):
        continue

    # Приводим к числам
    user_id = int(user_id)
    quantity = int(quantity)
    price = int(price)

    # Самый дорогой заказ
    if price > max_price_val:
        max_price_val = price
        max_price_order = order_id

    # Заказ с наибольшим количеством товаров
    if quantity > max_quantity_val:
        max_quantity_val = quantity
        max_quantity_order = order_id

    # Статистика по дням (используем исходную дату как ключ)
    day_stats[date] = day_stats.get(date, 0) + 1

    # Статистика по пользователям
    user_orders_count[user_id] = user_orders_count.get(user_id, 0) + 1
    user_total_spent[user_id] = user_total_spent.get(user_id, 0) + price

    # Общие суммы
    total_revenue += price
    total_items += quantity
    total_orders += 1

# Находим максимумы
best_day = max(day_stats, key=day_stats.get)
best_day_orders = day_stats[best_day]

top_user_by_orders = max(user_orders_count, key=user_orders_count.get)
top_user_orders_val = user_orders_count[top_user_by_orders]

top_user_by_spent = max(user_total_spent, key=user_total_spent.get)
top_user_spent_val = user_total_spent[top_user_by_spent]

# Средние значения
avg_order_price = total_revenue / total_orders if total_orders else 0
avg_item_price = total_revenue / total_items if total_items else 0

# Вывод результатов
print("РЕЗУЛЬТАТЫ ОБРАБОТКИ ЗАКАЗОВ ЗА ИЮЛЬ:")
print(f"1. Самый дорогой заказ: {max_price_order}, стоимость: {max_price_val}")
print(f"2. Заказ с наибольшим количеством товаров: {max_quantity_order}, товаров: {max_quantity_val}")
print(f"3. День с максимумом заказов: {best_day}, заказов: {best_day_orders}")
print(f"4. Пользователь с максимумом заказов: {top_user_by_orders}, заказов: {top_user_orders_val}")
print(f"5. Пользователь с макс. суммой заказов: {top_user_by_spent}, общая сумма: {top_user_spent_val}")
print(f"6. Средняя стоимость заказа: {avg_order_price:.2f}")
print(f"7. Средняя стоимость товара: {avg_item_price:.2f}")
