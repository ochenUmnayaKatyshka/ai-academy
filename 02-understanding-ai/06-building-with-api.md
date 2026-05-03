# Урок 2.6 — Собираем полезные скрипты с Claude API

> В уроке 2.3 мы создали чат с Claude в терминале. Но чат — это только начало. API можно использовать для автоматизации реальных задач: перевод текстов, анализ отзывов, генерация контента. В этом уроке мы напишем 4 полезных скрипта — каждый решает конкретную задачу. Заодно закрепим всё, что знаем: переменные, функции, файлы, циклы и API.

---

## Зачем этот урок

В предыдущих уроках мы изучали вещи по отдельности:
- Python: переменные, функции, файлы (уроки 1.3-1.6)
- AI: API, промпты, токены (уроки 2.1-2.5)

Теперь соединим всё вместе. Каждый скрипт в этом уроке использует **и Python, и Claude API** для решения задачи, которую вручную делать долго и скучно.

```
Что мы построим:

  Скрипт 1: Переводчик файлов
    Читает текст из файла → переводит через Claude → сохраняет результат

  Скрипт 2: Анализатор отзывов
    Читает отзывы из файла → Claude определяет тональность каждого

  Скрипт 3: Генератор описаний товаров
    Список товаров → Claude пишет описание для каждого

  Скрипт 4: Умный обработчик CSV
    Читает таблицу → Claude анализирует данные → сохраняет отчёт
```

Каждый скрипт — несколько десятков строк. Но они делают реальную работу, которая вручную заняла бы часы.

---

## Подготовка

Убедись, что установлены библиотеки (из урока 2.3):

```bash
pip3 install anthropic python-dotenv
```

Файл `.env` в папке проекта:

```
ANTHROPIC_API_KEY=sk-ant-api03-твой-ключ
```

Базовая настройка — одинаковая для всех скриптов:

```python
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()  # загружает API-ключ из .env
client = Anthropic()  # создаёт клиент для работы с Claude
```

Мы уже делали это в уроке 2.3. Если что-то непонятно — вернись туда.

---

## Скрипт 1: Переводчик файлов

### Задача

У тебя есть текст на русском. Нужно перевести на английский и сохранить в файл. Вручную — копировать в переводчик, ждать, копировать обратно. Скрипт делает это за секунды.

### Код

```python
# translator.py — переводит текст из файла через Claude

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


def translate(text, target_language="English"):
    """
    Отправляет текст в Claude и получает перевод.
    text — текст для перевода (строка)
    target_language — на какой язык переводить (по умолчанию English)
    """
    response = client.messages.create(
        model="claude-haiku-4-5",       # Haiku — быстрый и дешёвый (урок 2.5)
        max_tokens=2048,                 # максимум токенов в ответе
        messages=[{
            "role": "user",
            "content": f"Translate the following text to {target_language}. "
                       f"Return ONLY the translation, nothing else.\n\n{text}"
            # f-строка (урок 1.3) — вставляем переменные прямо в текст
        }]
    )
    return response.content[0].text
    # response.content — список блоков ответа
    # [0] — первый блок
    # .text — текст этого блока


# === ГЛАВНАЯ ЧАСТЬ ПРОГРАММЫ ===

# Шаг 1: Читаем файл с текстом
input_file = "text_to_translate.txt"

# open() открывает файл, read() читает содержимое (урок 1.6)
with open(input_file, "r", encoding="utf-8") as f:
    original_text = f.read()

print(f"Прочитан файл: {input_file}")
print(f"Длина текста: {len(original_text)} символов")

# Шаг 2: Переводим
print("Перевожу...")
translated = translate(original_text, target_language="English")

# Шаг 3: Сохраняем результат
output_file = "translated.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(translated)

print(f"Перевод сохранён в: {output_file}")
```

### Как запустить

1. Создай файл `text_to_translate.txt` с любым текстом на русском:

```
Искусственный интеллект меняет мир. Компании используют AI для автоматизации рутинных задач, анализа данных и создания новых продуктов. Через несколько лет AI-ассистенты станут такими же привычными, как смартфоны.
```

2. Запусти:

```bash
python3 translator.py
```

3. Открой `translated.txt` — там будет перевод.

### Разбор: что здесь нового

```python
def translate(text, target_language="English"):
```
Функция с **параметром по умолчанию** (урок 1.5). Если не указать язык — переведёт на английский. Но можно вызвать `translate(text, "Spanish")` — и переведёт на испанский.

```python
f"Translate the following text to {target_language}. "
f"Return ONLY the translation, nothing else.\n\n{text}"
```
**Промпт** (урок 2.4). Чёткая инструкция: переведи, верни ТОЛЬКО перевод. Без этого Claude может добавить пояснения вроде «Вот перевод:».

```python
with open(input_file, "r", encoding="utf-8") as f:
    original_text = f.read()
```
Чтение файла (урок 1.6). `encoding="utf-8"` — чтобы кириллица читалась правильно.

---

## Скрипт 2: Анализатор отзывов

### Задача

У тебя список отзывов клиентов. Нужно понять: какие позитивные, какие негативные, какие нейтральные. Вручную — читать каждый и решать. При 100 отзывах — это час работы. Скрипт делает это за минуту.

### Код

```python
# review_analyzer.py — анализирует тональность отзывов

import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


def analyze_review(review_text):
    """
    Отправляет отзыв в Claude → получает тональность.
    Возвращает словарь: {"sentiment": "positive/negative/neutral", "summary": "..."}
    """
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"""Analyze this customer review. Respond in JSON format:
{{"sentiment": "positive" or "negative" or "neutral", "summary": "one sentence summary in Russian"}}

Review: {review_text}"""
            # Двойные фигурные скобки {{ }} — чтобы Python не путал их
            # с f-строковыми подстановками {review_text}
        }]
    )
    # Парсим JSON из ответа Claude
    result = json.loads(response.content[0].text)
    # json.loads() превращает строку JSON в словарь Python (урок 1.6)
    return result


# === ГЛАВНАЯ ЧАСТЬ ===

# Список отзывов (в реальном проекте — из файла или базы данных)
reviews = [
    "Отличный магазин! Заказ пришёл на следующий день, всё целое.",
    "Ужасное обслуживание. Ждала посылку 3 недели, никто не отвечал.",
    "Нормально, но упаковка могла бы быть лучше.",
    "Качество супер, но доставка дорогая. В целом доволен.",
    "Больше никогда не закажу. Товар не соответствует описанию.",
    "Быстро, удобно, рекомендую!",
    "Средненько. Ничего особенного.",
]

# Счётчики для статистики
stats = {"positive": 0, "negative": 0, "neutral": 0}

print("=== Анализ отзывов ===\n")

# Проходим по каждому отзыву (цикл for — урок 1.4)
for i, review in enumerate(reviews, 1):
    # enumerate(reviews, 1) — нумерация с 1
    # i = номер, review = текст отзыва

    result = analyze_review(review)
    sentiment = result["sentiment"]
    summary = result["summary"]

    # Обновляем статистику
    stats[sentiment] += 1
    # stats["positive"] += 1 — увеличиваем счётчик на 1

    # Выводим результат
    print(f"  #{i}: [{sentiment.upper():8s}] {summary}")
    # :8s — форматирование: текст занимает минимум 8 символов (для ровных колонок)

print(f"\n=== Статистика ===")
print(f"  Позитивных: {stats['positive']}")
print(f"  Негативных: {stats['negative']}")
print(f"  Нейтральных: {stats['neutral']}")

total = len(reviews)
positive_pct = stats["positive"] / total * 100
print(f"\n  Позитивных отзывов: {positive_pct:.0f}%")
# :.0f — форматирование числа: 0 знаков после запятой
```

### Пример вывода

```
=== Анализ отзывов ===

  #1: [POSITIVE] Быстрая доставка, товар в порядке.
  #2: [NEGATIVE] Долгая доставка и отсутствие поддержки.
  #3: [NEUTRAL ] Средняя оценка, замечание к упаковке.
  #4: [POSITIVE] Хорошее качество, но дорогая доставка.
  #5: [NEGATIVE] Товар не соответствует описанию.
  #6: [POSITIVE] Быстро и удобно.
  #7: [NEUTRAL ] Ничего особенного.

=== Статистика ===
  Позитивных: 3
  Негативных: 2
  Нейтральных: 2

  Позитивных отзывов: 43%
```

### Разбор: что здесь нового

```python
json.loads(response.content[0].text)
```
Claude возвращает строку `'{"sentiment": "positive", "summary": "..."}'`. `json.loads()` превращает эту строку в словарь Python, чтобы можно было обращаться к полям: `result["sentiment"]`.

```python
for i, review in enumerate(reviews, 1):
```
`enumerate()` — функция Python, которая добавляет нумерацию. Без неё у тебя только `review` (текст). С ней — `i` (номер) и `review` (текст). `1` — начать нумерацию с единицы, а не с нуля.

```python
stats[sentiment] += 1
```
`+=` — сокращение для «прибавить». `stats["positive"] += 1` — то же самое, что `stats["positive"] = stats["positive"] + 1`.

---

## Скрипт 3: Генератор описаний товаров

### Задача

У тебя список товаров с характеристиками. Нужно написать привлекательное описание для сайта. Вручную — 5-10 минут на товар. При 50 товарах — целый день. Скрипт генерирует все за несколько минут.

### Код

```python
# product_descriptions.py — генерирует описания товаров для сайта

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


def generate_description(product):
    """
    Генерирует описание товара для сайта.
    product — словарь с полями: name, category, features, price
    """
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": f"""Напиши короткое продающее описание товара для интернет-магазина.
2-3 предложения, дружелюбный тон, упомяни ключевые преимущества.

Товар: {product['name']}
Категория: {product['category']}
Характеристики: {product['features']}
Цена: {product['price']} руб."""
        }]
    )
    return response.content[0].text


# === СПИСОК ТОВАРОВ ===

# Список словарей (урок 1.3: словари, урок 1.4: списки)
products = [
    {
        "name": "Беспроводные наушники AirSound Pro",
        "category": "Электроника",
        "features": "Bluetooth 5.3, шумоподавление, 24 часа работы, быстрая зарядка",
        "price": 4990
    },
    {
        "name": "Рюкзак Urban Explorer",
        "category": "Аксессуары",
        "features": "30 литров, водоотталкивающий, отделение для ноутбука, USB-порт",
        "price": 3490
    },
    {
        "name": "Умная колонка HomeVoice",
        "category": "Умный дом",
        "features": "Голосовой ассистент, Wi-Fi, Bluetooth, стерео звук, таймеры",
        "price": 5990
    },
]

# === ГЕНЕРИРУЕМ ОПИСАНИЯ ===

print("=== Генерация описаний товаров ===\n")

# Открываем файл для записи всех описаний
with open("descriptions.txt", "w", encoding="utf-8") as f:

    for product in products:
        print(f"Генерирую: {product['name']}...")

        description = generate_description(product)

        # Выводим на экран
        print(f"\n  {product['name']} — {product['price']} руб.")
        print(f"  {description}\n")

        # Записываем в файл
        f.write(f"## {product['name']} — {product['price']} руб.\n\n")
        f.write(f"{description}\n\n")
        f.write("---\n\n")

print("Все описания сохранены в descriptions.txt")
```

### Разбор: что здесь нового

```python
product['name']
```
Обращение к значению в словаре по ключу (урок 1.3). `product` — это словарь с ключами `name`, `category`, `features`, `price`.

```python
with open("descriptions.txt", "w", encoding="utf-8") as f:
    for product in products:
        ...
        f.write(...)
```
Файл открывается **один раз** перед циклом. Внутри цикла каждое описание дописывается в тот же файл. Когда цикл завершится, файл закроется автоматически (так работает `with` — урок 1.6).

---

## Скрипт 4: Умный обработчик CSV

### Задача

У тебя таблица с данными (расходы, продажи, обращения). Нужно проанализировать и написать отчёт. Скрипт читает CSV-файл, отправляет данные в Claude и получает анализ.

### Что такое CSV

**CSV (Comma-Separated Values)** — формат таблицы в текстовом файле. Как Excel, но без оформления. Каждая строка — строка таблицы. Значения разделены запятыми.

```
Пример файла expenses.csv:

дата,категория,сумма,описание
2025-03-01,еда,1500,Продукты на неделю
2025-03-02,транспорт,350,Такси до работы
2025-03-03,еда,800,Обед с коллегами
2025-03-04,развлечения,2000,Кино и ужин
2025-03-05,еда,1200,Продукты
2025-03-06,транспорт,200,Метро
2025-03-07,здоровье,3500,Стоматолог
```

### Код

```python
# expense_analyzer.py — анализирует расходы из CSV-файла

import os
import csv
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


# === ШАГ 1: ЧИТАЕМ CSV ===

expenses = []  # список для хранения всех строк

with open("expenses.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    # csv.DictReader — читает CSV и превращает каждую строку в словарь
    # Первая строка (дата,категория,сумма,описание) становится ключами
    # Каждая следующая строка — словарь:
    # {"дата": "2025-03-01", "категория": "еда", "сумма": "1500", ...}

    for row in reader:
        expenses.append(row)
        # append() добавляет элемент в конец списка (урок 1.4)

print(f"Прочитано {len(expenses)} записей из expenses.csv")


# === ШАГ 2: СЧИТАЕМ СТАТИСТИКУ (Python, без Claude) ===

total = 0
by_category = {}  # словарь: категория → сумма

for expense in expenses:
    amount = int(expense["сумма"])
    # int() превращает строку "1500" в число 1500
    # CSV хранит всё как текст — нужно конвертировать

    category = expense["категория"]
    total += amount

    # Если категория уже есть — прибавляем. Если нет — создаём.
    if category in by_category:
        by_category[category] += amount
    else:
        by_category[category] = amount

print(f"Общая сумма расходов: {total} руб.")
print(f"По категориям: {by_category}")


# === ШАГ 3: ПРОСИМ CLAUDE ПРОАНАЛИЗИРОВАТЬ ===

# Формируем текст с данными для Claude
data_summary = f"""
Период: {expenses[0]['дата']} — {expenses[-1]['дата']}
Общая сумма: {total} руб.
Количество транзакций: {len(expenses)}

Расходы по категориям:
"""

for category, amount in by_category.items():
    # .items() возвращает пары (ключ, значение) из словаря
    percentage = amount / total * 100
    data_summary += f"  {category}: {amount} руб. ({percentage:.1f}%)\n"

# Отправляем в Claude
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=500,
    messages=[{
        "role": "user",
        "content": f"""Проанализируй мои расходы. Дай короткий отчёт:
1. На что уходит больше всего
2. Что можно оптимизировать
3. Общая оценка

Данные:
{data_summary}"""
    }]
)

analysis = response.content[0].text


# === ШАГ 4: СОХРАНЯЕМ ОТЧЁТ ===

with open("expense_report.txt", "w", encoding="utf-8") as f:
    f.write("=== ОТЧЁТ О РАСХОДАХ ===\n\n")
    f.write(f"Период: {expenses[0]['дата']} — {expenses[-1]['дата']}\n")
    f.write(f"Общая сумма: {total} руб.\n\n")
    f.write("--- По категориям ---\n")
    for category, amount in by_category.items():
        f.write(f"  {category}: {amount} руб.\n")
    f.write(f"\n--- Анализ от Claude ---\n\n")
    f.write(analysis)
    f.write("\n")

print(f"\nОтчёт сохранён в expense_report.txt")
print(f"\n{analysis}")
```

### Как запустить

1. Создай файл `expenses.csv` (содержимое выше)
2. Запусти `python3 expense_analyzer.py`
3. Открой `expense_report.txt`

### Разбор: что здесь нового

```python
import csv
```
Встроенный модуль Python для работы с CSV-файлами. Не нужно устанавливать через pip — он уже есть в Python.

```python
reader = csv.DictReader(f)
```
`DictReader` читает CSV и превращает каждую строку в словарь. Первая строка файла — это ключи (`дата`, `категория`, `сумма`, `описание`). Каждая следующая строка — значения.

```python
expenses[-1]['дата']
```
`[-1]` — последний элемент списка. `expenses[0]` — первый, `expenses[-1]` — последний. Так мы получаем дату первой и последней записи.

```python
for category, amount in by_category.items():
```
`.items()` возвращает пары из словаря. Если `by_category = {"еда": 3500, "транспорт": 550}`, то цикл пройдёт по парам: `("еда", 3500)`, `("транспорт", 550)`.

---

## Паттерн, который объединяет все скрипты

Заметь: все 4 скрипта построены по одной схеме:

```
1. ПРОЧИТАТЬ данные (из файла, списка, CSV)
        │
        ▼
2. ОБРАБОТАТЬ через Claude API (перевод, анализ, генерация)
        │
        ▼
3. СОХРАНИТЬ результат (в файл, на экран)
```

Это базовый паттерн AI-автоматизации: **вход → обработка → выход**. Он встречается везде:

```
Бот поддержки:    сообщение клиента → Claude → ответ
RAG-система:      вопрос → поиск + Claude → ответ с источниками
Анализатор:       данные → Claude → отчёт
Генератор:        параметры → Claude → контент
```

В Этапе 3 мы усложним этот паттерн: добавим **инструменты** (Claude сам решает, что прочитать), **цикл** (Claude делает несколько шагов) и **память** (Claude помнит предыдущие действия). Но основа — та же самая.

---

## Частые ошибки и как их исправить

Здесь собраны ошибки, которые чаще всего встречаются при написании скриптов с API. Сохрани эту страницу — пригодится в следующих уроках.

### Ошибка 1: AuthenticationError

```
anthropic.AuthenticationError: Error code: 401
```

**Причина:** неправильный API-ключ или его нет.

```
Что проверить:
  1. Файл .env существует в папке проекта
  2. В нём ANTHROPIC_API_KEY=sk-ant-api03-... (без пробелов вокруг =)
  3. Ключ скопирован полностью (не обрезан)
  4. load_dotenv() вызывается ДО создания клиента
```

### Ошибка 2: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'anthropic'
```

**Причина:** библиотека не установлена.

```
Решение:
  pip3 install anthropic     (macOS)
  pip install anthropic      (Windows)

  Если используешь виртуальное окружение — убедись, что оно активировано:
    source venv/bin/activate  (macOS)
    venv\Scripts\activate     (Windows)
```

### Ошибка 3: FileNotFoundError

```
FileNotFoundError: [Errno 2] No such file or directory: 'text_to_translate.txt'
```

**Причина:** файл не найден. Либо его нет, либо ты запускаешь скрипт из другой папки.

```
Решение:
  1. Убедись, что файл существует
  2. Убедись, что ты в правильной папке:
     pwd (macOS) — покажет текущую папку
     cd ~/Documents/Projects/ai-academy — перейти в нужную
  3. Или укажи полный путь к файлу:
     "/Users/katya/Documents/text.txt" вместо "text.txt"
```

### Ошибка 4: json.JSONDecodeError

```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1
```

**Причина:** Claude вернул не чистый JSON, а текст с пояснениями.

```
Что Claude вернул:
  "Вот результат анализа: {"sentiment": "positive"}"
  ^^^^^^^^^^^^^^^^^^^^^^^^ — это лишний текст

Решение: улучшить промпт
  Плохо:  "Проанализируй отзыв"
  Хорошо: "Respond in JSON format ONLY. No other text."
```

### Ошибка 5: RateLimitError

```
anthropic.RateLimitError: Error code: 429
```

**Причина:** слишком много запросов за короткое время.

```
Решение:
  Добавь паузу между запросами в цикле:

  import time

  for review in reviews:
      result = analyze_review(review)
      time.sleep(1)  # ждём 1 секунду между запросами
```

---

## Практика

### Задание 1: Переведи свой текст

Возьми любой текст (статью, описание, пост) и переведи через `translator.py`. Попробуй перевести на разные языки: English, Spanish, French, Chinese.

### Задание 2: Проанализируй свои отзывы

Добавь 10 своих отзывов в `review_analyzer.py` (можно скопировать с Wildberries, Ozon или любого магазина). Посмотри, правильно ли Claude определяет тональность.

### Задание 3: Свой скрипт

Придумай свою задачу и напиши скрипт по паттерну «вход → Claude → выход». Примеры:
- Генератор постов для соцсетей (список тем → посты)
- Анализатор резюме (текст резюме → оценка и советы)
- Корректор текста (текст с ошибками → исправленный текст)

---

## Задачки на закрепление

**Задача 1:** По какому паттерну работают все скрипты в этом уроке?

<details>
<summary>Ответ</summary>

Вход → Обработка → Выход. Скрипт читает данные (из файла, списка, CSV), отправляет их в Claude API для обработки (перевод, анализ, генерация), получает результат и сохраняет (в файл или выводит на экран). Этот паттерн — основа всех AI-приложений.
</details>

**Задача 2:** Почему в скрипте с отзывами мы используем `json.loads()`, а не просто читаем текст ответа?

<details>
<summary>Ответ</summary>

Claude возвращает строку: `'{"sentiment": "positive", "summary": "..."}'`. Это строка — с ней нельзя работать как со словарём (нельзя написать `result["sentiment"]`). `json.loads()` превращает строку JSON в словарь Python, после чего можно обращаться к полям по ключу. Без `json.loads()` пришлось бы вручную парсить текст.
</details>

**Задача 3:** Что делает `enumerate(reviews, 1)`?

<details>
<summary>Ответ</summary>

`enumerate()` добавляет нумерацию к элементам списка. Без неё цикл `for review in reviews` даёт только текст отзыва. С ней `for i, review in enumerate(reviews, 1)` даёт и номер (`i`), и текст (`review`). Параметр `1` означает: начать нумерацию с единицы (по умолчанию — с нуля).
</details>

**Задача 4:** Почему в скрипте с CSV мы делаем `int(expense["сумма"])`, а не просто используем `expense["сумма"]`?

<details>
<summary>Ответ</summary>

CSV хранит все значения как текст (строки). `expense["сумма"]` — это строка `"1500"`, а не число `1500`. Складывать строки нельзя: `"1500" + "350"` даст `"1500350"` вместо `1850`. `int()` превращает строку в целое число, после чего с ним можно считать: `1500 + 350 = 1850`.
</details>

---

## Глоссарий

| Термин | Что значит |
|--------|-----------|
| **CSV** | Comma-Separated Values — табличный формат файла, где значения разделены запятыми. Как Excel, но текстовый |
| **csv.DictReader** | Функция Python, которая читает CSV и превращает каждую строку в словарь |
| **enumerate()** | Функция Python, которая добавляет нумерацию к элементам списка при переборе в цикле |
| **json.loads()** | Функция, которая превращает строку JSON в словарь Python. loads = load string |
| **json.dumps()** | Функция, которая превращает словарь Python в строку JSON. dumps = dump string |
| **f-строка** | Строка с `f` перед кавычками: `f"Привет, {name}!"`. Позволяет вставлять переменные прямо в текст |
| **append()** | Метод списка: добавляет элемент в конец. `my_list.append("новый")` |
| **items()** | Метод словаря: возвращает пары (ключ, значение). Для перебора в цикле |
| **Параметр по умолчанию** | Значение аргумента функции, если его не передали: `def f(x, lang="en")` |
| **Паттерн** | Повторяющийся шаблон решения. «Вход → обработка → выход» — паттерн AI-скриптов |
| **RateLimitError** | Ошибка: слишком много запросов к API за короткое время. Решение: добавить паузу |
| **time.sleep()** | Функция Python: пауза на N секунд. `time.sleep(1)` — ждать 1 секунду |

---

## Главное

```
Все AI-скрипты работают по одному паттерну:
  ВХОД → ОБРАБОТКА (Claude API) → ВЫХОД

Этот паттерн масштабируется:
  Один текст      → translate()     → один перевод
  100 отзывов     → analyze_review()→ таблица тональностей
  Список товаров  → generate()      → описания для сайта
  CSV с данными   → analyze()       → отчёт

Python читает и готовит данные.
Claude думает и генерирует.
Python сохраняет результат.

Частые ошибки:
  AuthenticationError → проверь .env и API-ключ
  ModuleNotFoundError → pip install anthropic
  FileNotFoundError   → проверь путь к файлу
  JSONDecodeError     → улучши промпт ("JSON only")
  RateLimitError      → добавь time.sleep(1) между запросами
```

---

## Что дальше?

Ты написала 4 скрипта, которые делают реальную работу. Каждый из них — прямая линия: данные → Claude → результат. Но что если программа должна **сама решать**, какие данные нужны и что делать дальше? Не ты говоришь «переведи файл» — а программа сама находит файл, решает, что с ним делать, и действует. Это и есть **AI-агент** — тема Этапа 3.
