# Урок 4.2 — Базы данных

> В прошлом уроке мы создали Telegram-бота с Claude. Он работает, отвечает на вопросы, помнит контекст разговора. Но есть одна проблема: закрой терминал — и бот забудет все разговоры. Потому что вся история хранится в словаре `conversations = {}` — в оперативной памяти. Перезапуск = полная амнезия. В этом уроке мы это починим.

---

## Проблема: память, которая исчезает

Вот как сейчас работает наш бот из урока 4.1:

```python
conversations = {}  # словарь в оперативной памяти

# Пользователь пишет "Привет"
conversations[123456] = [{"role": "user", "content": "Привет"}]

# Claude отвечает
conversations[123456].append({"role": "assistant", "content": "Привет! Чем помочь?"})

# ... бот работает, история растёт ...

# Ctrl+C → бот остановился
# python ai_bot.py → бот запустился заново
# conversations = {} → пустой словарь. Всё потеряно.
```

Это как писать заметки на стикерах, которые приклеены к монитору. Выключил компьютер — стикеры упали. Нужно что-то надёжнее.

---

## Где хранить данные: три варианта

### Вариант 1: Файл (JSON)

Самое очевидное — записать данные в файл:

```python
import json

# Сохранить
with open("history.json", "w") as f:
    json.dump(conversations, f)

# Загрузить
with open("history.json", "r") as f:
    conversations = json.load(f)
```

**Проблема:** если два пользователя напишут боту одновременно, оба обработчика попытаются записать в один файл. Один перезапишет данные другого. Это называется **race condition** — гонка за ресурс.

### Вариант 2: База данных SQLite

**SQLite** — это база данных, которая хранит данные в одном файле. Но в отличие от JSON-файла, SQLite умеет:

- Безопасно обрабатывать несколько запросов одновременно (блокировки)
- Быстро искать по условию ("все сообщения от пользователя 123456")
- Хранить миллионы записей без замедления
- Гарантировать, что данные не повредятся при сбое

И самое главное: **SQLite встроена в Python**. Не нужно ничего устанавливать — `import sqlite3` и всё.

### Вариант 3: PostgreSQL / MySQL

Отдельная программа-сервер, которая работает в фоне. Нужна для больших проектов с тысячами одновременных пользователей. Для нашего бота — избыточна.

### Сравнение

| | JSON-файл | SQLite | PostgreSQL |
|---|---|---|---|
| **Установка** | Не нужна | Не нужна (встроена) | Отдельный сервер |
| **Данные на диске** | Да | Да | Да |
| **Поиск по условию** | Вручную (цикл в Python) | `SELECT WHERE user_id = ?` | `SELECT WHERE user_id = ?` |
| **Одновременная запись** | Опасно (потеря данных) | Безопасно (блокировка) | Безопасно (полная поддержка) |
| **Для чего** | Конфиги, маленькие списки | Боты, приложения, локальные проекты | Веб-приложения, большие системы |

**Наш выбор: SQLite.** Бесплатно, встроено в Python, надёжно, достаточно для бота.

```
Источник: sqlite.org
"SQLite competes with fopen(), not with PostgreSQL."
SQLite конкурирует с открытием файлов, а не с большими СУБД.
```

---

## Что такое SQL

SQL — это **язык запросов к базам данных**. Аббревиатура: **Structured Query Language** (язык структурированных запросов).

Это НЕ язык программирования. На SQL нельзя написать программу. SQL — это способ сказать базе данных: "найди мне это", "сохрани это", "удали это".

Аналогия: Python — это язык, на котором ты пишешь программу. SQL — это язык, на котором ты разговариваешь с базой данных внутри этой программы. Как два разных языка для двух разных задач.

SQL используют **все** базы данных: SQLite, PostgreSQL, MySQL, Oracle. Выучишь SQL один раз — используешь везде.

---

## SQL за 10 минут: пять команд

Тебе нужно знать всего 5 команд. Серьёзно — для бота этого хватит.

### 1. CREATE TABLE — создать таблицу

Таблица — это как таблица в Excel. У неё есть столбцы (с именами и типами) и строки (данные).

```sql
CREATE TABLE IF NOT EXISTS conversations (
    id        INTEGER PRIMARY KEY,
    user_id   INTEGER NOT NULL,
    role      TEXT NOT NULL,
    content   TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
```

Разберём:

| Элемент | Что значит |
|---------|-----------|
| `CREATE TABLE` | Создать таблицу |
| `IF NOT EXISTS` | Только если такой ещё нет (иначе ошибка при повторном запуске) |
| `conversations` | Имя таблицы |
| `id INTEGER PRIMARY KEY` | Уникальный номер строки, назначается автоматически |
| `user_id INTEGER NOT NULL` | ID пользователя Telegram, целое число, обязательное |
| `role TEXT NOT NULL` | `"user"` или `"assistant"`, строка, обязательная |
| `content TEXT NOT NULL` | Текст сообщения, обязательный |
| `timestamp TEXT NOT NULL` | Время сообщения, обязательное |

**Типы данных в SQLite:**

| Тип | Что хранит | Примеры |
|-----|-----------|---------|
| `INTEGER` | Целые числа | `1`, `42`, `123456789` |
| `TEXT` | Строки | `"привет"`, `"user"`, `"2024-01-15"` |
| `REAL` | Дробные числа | `3.14`, `0.99` |

Для бота хватит `INTEGER` и `TEXT`.

### 2. INSERT INTO — добавить строку

```sql
INSERT INTO conversations (user_id, role, content, timestamp)
VALUES (123456, 'user', 'Привет!', '2024-01-15 10:30:00');
```

Это как `conversations[123456].append({"role": "user", "content": "Привет!"})` — но данные сохраняются на диск.

### 3. SELECT — найти данные

```sql
-- Все сообщения пользователя 123456
SELECT role, content FROM conversations
WHERE user_id = 123456;

-- Только последние 20 сообщений (от новых к старым)
SELECT role, content FROM conversations
WHERE user_id = 123456
ORDER BY id DESC
LIMIT 20;
```

Разберём:

| Элемент | Что значит |
|---------|-----------|
| `SELECT role, content` | Какие столбцы вернуть |
| `FROM conversations` | Из какой таблицы |
| `WHERE user_id = 123456` | Условие (фильтр) |
| `ORDER BY id DESC` | Сортировка: `DESC` = от нового к старому, `ASC` = от старого к новому |
| `LIMIT 20` | Вернуть не больше 20 строк |

### 4. DELETE — удалить строки

```sql
-- Удалить все сообщения пользователя (команда /clear)
DELETE FROM conversations WHERE user_id = 123456;
```

### 5. UPDATE — изменить данные

```sql
UPDATE conversations SET content = 'исправленный текст' WHERE id = 5;
```

Нам пока не нужен, но знать полезно.

---

## SQL в Python: модуль sqlite3

Вот как SQL работает внутри Python:

### Шаг 1: Подключение

```python
import sqlite3

# Создаёт файл bot_history.db (если нет) или открывает существующий
conn = sqlite3.connect("bot_history.db")
```

`connect()` — это как `open()` для файлов. Создаёт соединение с базой данных. Если файла нет — создаст пустую базу.

### Шаг 2: Выполнение SQL

```python
# Создать таблицу
conn.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id        INTEGER PRIMARY KEY,
        user_id   INTEGER NOT NULL,
        role      TEXT NOT NULL,
        content   TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
""")
conn.commit()  # сохранить изменения на диск
```

`execute()` — выполнить SQL-запрос. `commit()` — зафиксировать изменения. Без `commit()` данные останутся в памяти и пропадут.

### Шаг 3: Вставка данных

```python
conn.execute(
    "INSERT INTO conversations (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
    (123456, "user", "Привет!", "2024-01-15 10:30:00")
)
conn.commit()
```

**Важно: знаки `?`**

`?` — это заполнители (placeholders). Python подставляет значения из кортежа `(123456, "user", ...)` безопасно.

Почему не написать так?

```python
# ОПАСНО — никогда так не делай!
conn.execute(f"INSERT INTO conversations VALUES ({user_id}, '{role}', '{content}', '{timestamp}')")
```

Потому что если `content` содержит одинарную кавычку (например, `it's`), запрос сломается. А если пользователь специально отправит `'; DROP TABLE conversations; --`, он **удалит всю таблицу**. Это называется **SQL-инъекция** — одна из самых известных уязвимостей в истории IT.

**Всегда используй `?` — это защита.**

### Шаг 4: Чтение данных

```python
cursor = conn.execute(
    "SELECT role, content FROM conversations WHERE user_id = ? ORDER BY id DESC LIMIT ?",
    (123456, 20)
)
rows = cursor.fetchall()
# rows = [("assistant", "Чем помочь?"), ("user", "Привет!")]
#         ^ новые первые (ORDER BY DESC)
```

- `cursor` — объект с результатами запроса
- `fetchall()` — получить все строки как список кортежей
- `fetchone()` — получить одну строку (или `None`, если данных нет)

### Шаг 5: Закрытие

```python
conn.close()
```

### Безопасный паттерн: `with`

Чтобы не забывать про `commit()` и обработку ошибок:

```python
conn = sqlite3.connect("bot_history.db")

with conn:  # если всё ок → commit(), если ошибка → rollback()
    conn.execute(
        "INSERT INTO conversations (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (123456, "user", "Привет!", "2024-01-15 10:30:00")
    )
# commit() вызван автоматически

conn.close()
```

`with conn:` — контекстный менеджер. Если код внутри выполнился без ошибок — автоматически вызывает `commit()`. Если произошла ошибка — вызывает `rollback()` (откат, как будто ничего не записывали).

**Важно:** `with conn:` НЕ закрывает соединение. `conn.close()` нужен отдельно.

---

## Обновляем бота: от словаря к базе данных

### Что было (урок 4.1)

```python
conversations = {}  # оперативная память → пропадает при перезапуске
```

### Что будет

```python
import sqlite3  # встроенный модуль → данные на диске → переживают перезапуск
```

### Шаг 1: Функции для работы с базой

Создадим отдельный файл `database.py` — чтобы не мешать логику бота с SQL-запросами:

```python
# database.py — работа с базой данных

import sqlite3
from datetime import datetime

DB_FILE = "bot_history.db"

def init_db():
    """Создать таблицу, если её ещё нет. Вызывается один раз при старте."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id        INTEGER PRIMARY KEY,
            user_id   INTEGER NOT NULL,
            role      TEXT NOT NULL,
            content   TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_message(user_id: int, role: str, content: str):
    """Сохранить одно сообщение в базу."""
    conn = sqlite3.connect(DB_FILE)
    with conn:
        conn.execute(
            "INSERT INTO conversations (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, role, content, datetime.now().isoformat())
        )
    conn.close()

def get_history(user_id: int, limit: int = 20) -> list[dict]:
    """Получить последние N сообщений пользователя в хронологическом порядке."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute(
        "SELECT role, content FROM conversations WHERE user_id = ? ORDER BY id DESC LIMIT ?",
        (user_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()

    # reversed() — потому что ORDER BY DESC возвращает новые первыми,
    # а Claude API ожидает старые первыми (хронологический порядок)
    return [{"role": row[0], "content": row[1]} for row in reversed(rows)]

def clear_history(user_id: int):
    """Удалить все сообщения пользователя (команда /clear)."""
    conn = sqlite3.connect(DB_FILE)
    with conn:
        conn.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
    conn.close()
```

### Разбор каждой функции

**`init_db()`** — создаёт таблицу при первом запуске. `IF NOT EXISTS` означает: если таблица уже есть — ничего не делать. Без этого при втором запуске была бы ошибка "table already exists".

**`save_message()`** — записывает одно сообщение. `datetime.now().isoformat()` — текущее время в формате `2024-01-15T10:30:00.123456`. Мы храним время на будущее — чтобы потом можно было узнать, когда был разговор.

**`get_history()`** — возвращает историю в формате, который Claude API ожидает: `[{"role": "user", "content": "..."}, ...]`. Формат не изменился — бот даже не знает, что данные теперь из базы.

**`clear_history()`** — удаляет все сообщения пользователя. Используется для команды `/clear`.

### Шаг 2: Обновлённый бот

```python
# ai_bot.py — Telegram-бот с Claude и базой данных

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from anthropic import Anthropic
from database import init_db, save_message, get_history, clear_history  # наш модуль

load_dotenv()
logging.basicConfig(level=logging.INFO)

claude = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    clear_history(user_id)
    await update.message.reply_text(
        "Привет! Я AI-ассистент на базе Claude. Задай мне любой вопрос!"
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    clear_history(user_id)
    await update.message.reply_text("История очищена. Начнём сначала!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # Сохранить сообщение пользователя в базу
    save_message(user_id, "user", user_text)

    # Получить историю из базы (последние 20 сообщений)
    history = get_history(user_id, limit=20)

    try:
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )

        response = claude.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="Ты — полезный ассистент в Telegram-чате. Отвечай кратко и по делу.",
            messages=history  # ← из базы данных, но формат тот же
        )

        reply = response.content[0].text

        # Сохранить ответ Claude в базу
        save_message(user_id, "assistant", reply)

        if len(reply) > 4000:
            for i in range(0, len(reply), 4000):
                await update.message.reply_text(reply[i:i+4000])
        else:
            await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Ошибка Claude API: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуй ещё раз.")

# Инициализация базы при запуске
init_db()

app = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("clear", clear))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен!")
app.run_polling()
```

### Что изменилось (сравнение)

| Было (урок 4.1) | Стало (урок 4.2) |
|---|---|
| `conversations = {}` | `from database import ...` |
| `conversations[user_id] = []` | `clear_history(user_id)` |
| `conversations[user_id].append(...)` | `save_message(user_id, "user", text)` |
| `messages=conversations[user_id]` | `messages=get_history(user_id)` |

Обрати внимание: вызов Claude API **вообще не изменился**. `messages=history` работает точно так же — потому что `get_history()` возвращает данные в том же формате `[{"role": "...", "content": "..."}]`.

### Структура проекта

```
my-telegram-bot/
    ai_bot.py          # Основной бот
    database.py        # Работа с базой данных
    bot_history.db     # Файл базы данных (создаётся автоматически)
    .env               # Токены
    .env.example       # Шаблон
    requirements.txt   # Зависимости
    .gitignore         # Что не загружать в git
```

**.gitignore** (обновлённый):
```
.env
__pycache__/
*.db
```

Добавили `*.db` — файл базы данных тоже не нужно загружать в git. У каждого будет своя база.

---

## Проверяем, что база работает

Можно заглянуть в базу прямо из Python:

```python
# check_db.py — скрипт для проверки базы данных

import sqlite3

conn = sqlite3.connect("bot_history.db")
cursor = conn.execute("SELECT user_id, role, content, timestamp FROM conversations ORDER BY id DESC LIMIT 10")

for row in cursor.fetchall():
    user_id, role, content, timestamp = row
    print(f"[{timestamp}] User {user_id} | {role}: {content[:50]}...")

conn.close()
```

Запусти после нескольких сообщений боту:

```bash
python check_db.py
```

Увидишь что-то вроде:

```
[2024-01-15T10:30:05] User 123456 | assistant: Привет! Чем могу помочь?...
[2024-01-15T10:30:00] User 123456 | user: Привет!...
```

Данные на диске. Перезапусти бота — история на месте.

---

## Визуализация: как устроена таблица

```
Таблица: conversations
┌────┬──────────┬───────────┬───────────────────┬──────────────────────┐
│ id │ user_id  │ role      │ content           │ timestamp            │
├────┼──────────┼───────────┼───────────────────┼──────────────────────┤
│ 1  │ 123456   │ user      │ Привет!           │ 2024-01-15T10:30:00  │
│ 2  │ 123456   │ assistant │ Привет! Чем       │ 2024-01-15T10:30:05  │
│    │          │           │ помочь?           │                      │
│ 3  │ 789012   │ user      │ What is Python?   │ 2024-01-15T10:31:00  │
│ 4  │ 789012   │ assistant │ Python — это      │ 2024-01-15T10:31:03  │
│    │          │           │ язык...           │                      │
│ 5  │ 123456   │ user      │ Расскажи про SQL  │ 2024-01-15T10:32:00  │
│ 6  │ 123456   │ assistant │ SQL — это язык    │ 2024-01-15T10:32:04  │
│    │          │           │ запросов...       │                      │
└────┴──────────┴───────────┴───────────────────┴──────────────────────┘
```

- Каждая строка — одно сообщение
- У каждого пользователя свой `user_id`
- `SELECT WHERE user_id = 123456` вернёт строки 1, 2, 5, 6 (только этого пользователя)
- `ORDER BY id DESC LIMIT 2` вернёт строки 6, 5 (последние две)

---

## Частые ошибки

### 1. Забыл `commit()`

```
Проблема: данные записываются, но после перезапуска пропадают
Причина: без commit() данные остаются в памяти
Решение: используй `with conn:` — он вызывает commit() автоматически
```

### 2. SQL-инъекция

```python
# ОПАСНО — пользователь может уничтожить базу
conn.execute(f"SELECT * FROM conversations WHERE user_id = {user_id}")

# БЕЗОПАСНО — используй ? (placeholder)
conn.execute("SELECT * FROM conversations WHERE user_id = ?", (user_id,))
```

### 3. Кортеж из одного элемента

```python
# ОШИБКА — Python думает, что это просто число в скобках
conn.execute("SELECT * FROM conversations WHERE user_id = ?", (user_id))

# ПРАВИЛЬНО — запятая после user_id делает это кортежем
conn.execute("SELECT * FROM conversations WHERE user_id = ?", (user_id,))
```

В Python `(42)` — это просто число 42 в скобках. А `(42,)` — это кортеж (tuple) из одного элемента. SQLite ожидает кортеж, не число.

### 4. Файл базы в git

```
Проблема: файл .db попал в GitHub
Решение: добавь *.db в .gitignore ДО первого коммита
```

---

## Практика

### Задание 1: Запусти бота с базой данных

Создай файл `database.py`, обнови `ai_bot.py`. Поговори с ботом, затем перезапусти его (`Ctrl+C` → `python ai_bot.py`). Напиши "О чём мы говорили?" — бот должен помнить.

### Задание 2: Скрипт проверки

Запусти `check_db.py` — убедись, что сообщения сохраняются в базе с правильными user_id, role и timestamp.

### Задание 3: Команда /stats

Добавь команду `/stats`, которая показывает пользователю, сколько сообщений он отправил:

```python
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect("bot_history.db")
    cursor = conn.execute(
        "SELECT COUNT(*) FROM conversations WHERE user_id = ? AND role = 'user'",
        (user_id,)
    )
    count = cursor.fetchone()[0]
    conn.close()
    await update.message.reply_text(f"Ты отправил(а) {count} сообщений.")
```

Не забудь зарегистрировать обработчик: `app.add_handler(CommandHandler("stats", stats))`

---

## Задачки на закрепление

**Задача 1:** Почему SQLite лучше JSON-файла для бота?

<details>
<summary>Ответ</summary>

SQLite безопасно обрабатывает одновременные запросы (когда два пользователя пишут одновременно). JSON-файл при одновременной записи может потерять данные — один обработчик перезапишет изменения другого. Также SQLite быстро ищет по условию (`WHERE user_id = ?`), а в JSON нужно загрузить весь файл и искать циклом.
</details>

**Задача 2:** Что делает `?` в SQL-запросе?

<details>
<summary>Ответ</summary>

`?` — это заполнитель (placeholder). Python подставляет значения из кортежа безопасно, экранируя специальные символы. Это защита от SQL-инъекции — атаки, при которой пользователь вставляет вредоносный SQL-код через ввод данных.
</details>

**Задача 3:** Зачем `reversed()` в функции `get_history()`?

<details>
<summary>Ответ</summary>

Мы запрашиваем `ORDER BY id DESC LIMIT 20` — это возвращает 20 последних сообщений, но от новых к старым. Claude API ожидает сообщения в хронологическом порядке (от старых к новым). `reversed()` переворачивает список обратно в правильный порядок.
</details>

**Задача 4:** Что произойдёт, если убрать `conn.commit()` после INSERT?

<details>
<summary>Ответ</summary>

Данные запишутся в память, но не сохранятся на диск. Пока программа работает — всё будет выглядеть нормально. Но при перезапуске эти данные пропадут. `commit()` — это как нажать Ctrl+S для базы данных. Используй `with conn:` — тогда commit() вызывается автоматически.
</details>

---

## Глоссарий

| Термин | Что значит |
|--------|-----------|
| **База данных** | Программа для надёжного хранения и поиска данных |
| **SQLite** | Лёгкая база данных, встроенная в Python. Хранит всё в одном файле |
| **SQL** | Язык запросов к базам данных (Structured Query Language) |
| **Таблица** | Структура данных со столбцами и строками (как в Excel) |
| **CREATE TABLE** | SQL-команда: создать таблицу |
| **INSERT INTO** | SQL-команда: добавить строку в таблицу |
| **SELECT** | SQL-команда: найти и вернуть данные |
| **DELETE** | SQL-команда: удалить строки |
| **WHERE** | Условие в запросе (фильтр) |
| **ORDER BY** | Сортировка результатов (ASC — по возрастанию, DESC — по убыванию) |
| **LIMIT** | Ограничить количество возвращаемых строк |
| **PRIMARY KEY** | Уникальный идентификатор строки (автоматический номер) |
| **NOT NULL** | Поле обязательно для заполнения |
| **commit()** | Сохранить изменения на диск (как Ctrl+S) |
| **placeholder (?)** | Безопасная подстановка значений в SQL-запрос |
| **SQL-инъекция** | Атака через вставку вредоносного SQL-кода в пользовательский ввод |
| **Race condition** | Проблема при одновременном доступе к ресурсу (гонка данных) |
| **cursor** | Объект для получения результатов SQL-запроса |
| **fetchall()** | Получить все строки результата как список |
| **fetchone()** | Получить одну строку результата (или None) |

---

## Главное

```
Проблема:
  conversations = {} → данные в оперативной памяти → пропадают при перезапуске

Решение:
  SQLite → данные на диске → переживают перезапуск, сбои, Ctrl+C

Что нужно знать:
  1. import sqlite3            — встроен в Python, ничего устанавливать не нужно
  2. conn = sqlite3.connect()  — открыть/создать базу данных
  3. conn.execute("SQL", (?))  — выполнить запрос (всегда через ?)
  4. with conn:                — автоматический commit/rollback
  5. conn.close()              — закрыть соединение

5 SQL-команд:
  CREATE TABLE — создать таблицу
  INSERT INTO  — добавить данные
  SELECT       — найти данные
  DELETE       — удалить данные
  UPDATE       — изменить данные

Безопасность:
  ✓ Всегда используй ? (placeholders) — защита от SQL-инъекций
  ✓ Никогда не вставляй пользовательские данные в SQL через f-строки
  ✓ Добавь *.db в .gitignore
```

---

## Что дальше?

Бот теперь помнит разговоры между перезапусками. Но он всё ещё работает только на твоём компьютере — закрыла ноутбук, бот не доступен. В следующем уроке — **сервер и деплой**: как запустить бота на удалённом сервере, чтобы он работал 24/7.
