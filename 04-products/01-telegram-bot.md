# Урок 4.1 — Telegram-бот с AI

> До сих пор AI-агенты работали в терминале — ты запускала скрипт, он печатал ответ. Но реальные продукты работают там, где люди: в мессенджерах, на сайтах, в приложениях. В этом уроке мы подключим Claude к Telegram — и получим AI-ассистента, которым можно пользоваться с телефона.

---

## Прежде чем начать

Посмотри короткое видео — как создать первый продукт. А дальше пройдём всё пошагово.

<div class="video-wrapper">
<iframe src="https://www.youtube.com/embed/Nw0tksG2QnU" title="Как создать первый продукт" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---

## Что мы будем строить

```
Пользователь (Telegram)          Твой сервер              Anthropic
┌─────────────┐              ┌──────────────┐         ┌──────────┐
│ Пишет       │  ──────►     │ Python-бот   │ ──────► │ Claude   │
│ сообщение   │              │ получает     │         │ думает   │
│ в Telegram  │  ◄──────     │ текст,       │ ◄────── │ отвечает │
│ Видит ответ │              │ отправляет   │         │          │
└─────────────┘              │ в Claude,    │         └──────────┘
                             │ возвращает   │
                             │ ответ        │
                             └──────────────┘
```

Бот получает сообщение из Telegram → отправляет его в Claude API → получает ответ → отправляет обратно в Telegram. Три компонента, простая цепочка.

---

## Шаг 1: Создать бота в Telegram

Боты в Telegram создаются через специального бота — **@BotFather**. Это официальный бот от Telegram для управления ботами.

### Инструкция

1. Открой Telegram, найди **@BotFather** (с синей галочкой — это верификация)
2. Нажми **Start** (или отправь `/start`)
3. Отправь команду: `/newbot`
4. BotFather спросит **имя** бота — напиши любое (например, "My AI Helper")
5. BotFather спросит **username** — должен заканчиваться на `_bot` (например, `katya_ai_helper_bot`)
6. BotFather отправит **токен** — строка вида `4839574812:AAFD39kkdpWt3ywyRZergyOLMaJhac60qc`

**Этот токен — ключ к твоему боту.** Кто имеет токен — управляет ботом. Не публикуй его.

```
Источник: Telegram Official — "From BotFather to Hello World"
https://core.telegram.org/bots/tutorial
```

---

## Шаг 2: Установить библиотеки

```bash
pip install python-telegram-bot anthropic python-dotenv
```

| Библиотека | Зачем |
|-----------|-------|
| `python-telegram-bot` | SDK для Telegram (как `anthropic` для Claude) |
| `anthropic` | SDK для Claude API (из урока 2.3) |
| `python-dotenv` | Загружает токены из файла `.env` |

Помнишь из урока 3.4 — SDK это готовая библиотека от создателей сервиса? `python-telegram-bot` — это SDK для Telegram: он знает все URL, форматы и нюансы общения с сервером Telegram.

---

## Шаг 3: Файл с ключами (.env)

Создай файл `.env` (точка в начале — это важно):

```
TELEGRAM_BOT_TOKEN=4839574812:AAFD39kkdpWt3ywyRZergyOLMaJhac60qc
ANTHROPIC_API_KEY=sk-ant-api03-...
```

Почему не писать токены прямо в коде? Потому что код часто попадает в GitHub, а токены — это пароли. Файл `.env` остаётся локально и не загружается в git (если добавить его в `.gitignore` — урок 1.7).

---

## Шаг 4: Простой бот (без AI)

Сначала убедимся, что бот вообще работает — без Claude, просто эхо:

```python
# echo_bot.py — бот, который повторяет сообщения

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()  # загружает переменные из .env

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот. Напиши мне что-нибудь!")

# Любое текстовое сообщение
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)  # повторяет то же самое

# Запуск
app = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))       # реагирует на /start
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  # реагирует на текст
app.run_polling()  # запускает бота
```

### Разбор кода

```python
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
```
Импортируем из Telegram SDK. `Update` — входящее сообщение, `CommandHandler` — обработчик команд (`/start`), `MessageHandler` — обработчик обычных сообщений.

```python
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет!")
```
Функция-обработчик. Когда кто-то отправит `/start`, бот ответит "Привет!". `async def` — потому что Telegram SDK работает асинхронно (как Claude Agent SDK из урока 3.4).

```python
app = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
```
Создаёт приложение бота с нашим токеном.

```python
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
```
Регистрирует обработчики: `/start` → функция `start`, любой текст (кроме команд) → функция `echo`.

```python
app.run_polling()
```
Запускает бота. **Polling** — бот каждые несколько секунд спрашивает Telegram: "Есть новые сообщения?"

### Как запустить

```bash
python echo_bot.py
```

Открой Telegram, найди своего бота по username, нажми Start, напиши сообщение. Бот повторит его.

**Чтобы остановить** — нажми `Ctrl+C` в терминале.

---

## Шаг 5: Подключаем Claude

Теперь заменим эхо на Claude — бот будет думать и отвечать:

```python
# ai_bot.py — Telegram-бот с Claude

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from anthropic import Anthropic

load_dotenv()

# Настройка логов (чтобы видеть ошибки)
logging.basicConfig(level=logging.INFO)

# Claude-клиент
claude = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# История разговоров для каждого пользователя
conversations = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conversations[user_id] = []  # очистить историю
    await update.message.reply_text(
        "Привет! Я AI-ассистент на базе Claude. Задай мне любой вопрос!"
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conversations[user_id] = []
    await update.message.reply_text("История очищена. Начнём сначала!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # Инициализировать историю для нового пользователя
    if user_id not in conversations:
        conversations[user_id] = []

    # Добавить сообщение пользователя в историю
    conversations[user_id].append({"role": "user", "content": user_text})

    # Ограничить историю (чтобы не тратить слишком много токенов)
    if len(conversations[user_id]) > 20:
        conversations[user_id] = conversations[user_id][-20:]

    try:
        # Показать "печатает..." в Telegram
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )

        # Отправить запрос в Claude
        response = claude.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="Ты — полезный ассистент в Telegram-чате. Отвечай кратко и по делу.",
            messages=conversations[user_id]
        )

        reply = response.content[0].text

        # Сохранить ответ в историю
        conversations[user_id].append({"role": "assistant", "content": reply})

        # Telegram ограничивает сообщения до 4096 символов
        if len(reply) > 4000:
            for i in range(0, len(reply), 4000):
                await update.message.reply_text(reply[i:i+4000])
        else:
            await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Ошибка Claude API: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуй ещё раз.")

# Запуск
app = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("clear", clear))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен!")
app.run_polling()
```

### Что нового по сравнению с эхо-ботом

**1. История разговоров:**
```python
conversations = {}  # словарь: user_id → список сообщений
```
Каждый пользователь имеет свою историю. Это краткосрочная память из урока 3.3 — список `messages`, который растёт с каждым сообщением.

**2. Ограничение истории:**
```python
if len(conversations[user_id]) > 20:
    conversations[user_id] = conversations[user_id][-20:]
```
Храним только последние 20 сообщений. Больше = дороже (урок 2.5) и медленнее.

**3. Индикатор "печатает...":**
```python
await context.bot.send_chat_action(chat_id=..., action="typing")
```
Пока Claude думает, пользователь видит "бот печатает...". Без этого кажется, что бот завис.

**4. Разбивка длинных ответов:**
```python
if len(reply) > 4000:
    for i in range(0, len(reply), 4000):
        await update.message.reply_text(reply[i:i+4000])
```
Telegram ограничивает одно сообщение до 4096 символов. Claude может ответить длиннее — разбиваем на части.

**5. Обработка ошибок:**
```python
except Exception as e:
    await update.message.reply_text("Произошла ошибка. Попробуй ещё раз.")
```
Если Claude API недоступен или лимит исчерпан — бот не падает, а сообщает об ошибке.

---

## Структура проекта

```
my-telegram-bot/
    echo_bot.py        # Простой эхо-бот (шаг 4)
    ai_bot.py          # Бот с Claude (шаг 5)
    .env               # Токены (НЕ загружать в git!)
    .env.example        # Шаблон без реальных ключей (можно загружать)
    requirements.txt   # Зависимости
    .gitignore         # Файлы, которые git игнорирует
```

**requirements.txt:**
```
python-telegram-bot>=22.0
anthropic>=0.80.0
python-dotenv>=1.0.0
```

**.env.example** (шаблон для других — без реальных ключей):
```
TELEGRAM_BOT_TOKEN=your-telegram-token-here
ANTHROPIC_API_KEY=your-anthropic-key-here
```

**.gitignore** (обязательно!):
```
.env
__pycache__/
```

---

## Polling vs Webhook

Есть два способа получать сообщения из Telegram:

| | Polling | Webhook |
|---|---------|---------|
| **Как работает** | Бот спрашивает Telegram: "Новые сообщения?" | Telegram сам присылает сообщения на твой сервер |
| **Аналогия** | Проверять почтовый ящик каждые 5 секунд | Почтальон приносит почту к двери |
| **Нужен сервер?** | Нет — работает на ноутбуке | Да — нужен публичный URL с HTTPS |
| **Сложность** | Простой | Сложнее (нужен домен, SSL) |
| **Для кого** | Разработка, обучение, личные боты | Продакшн, много пользователей |

Мы используем **polling** (`app.run_polling()`) — он проще и работает где угодно. Webhook нужен для продакшна — это тема урока 4.3 (деплой).

---

## Частые ошибки

### 1. Бот не отвечает

```
Причина: бот не запущен или неправильный токен
Решение: проверь, что python ai_bot.py работает в терминале
         и токен в .env правильный (без пробелов)
```

### 2. `RuntimeError: event loop is already running`

```
Причина: запускаешь в Jupyter Notebook
Решение: запускай из обычного .py файла через терминал
```

### 3. Старые примеры из интернета не работают

```
Причина: библиотека python-telegram-bot версии 20+ изменила API
Решение: используй ApplicationBuilder (не Updater),
         все функции — async def (не обычные def)
```

### 4. Claude отвечает слишком дорого

```
Причина: модель claude-opus стоит $15-25 за миллион токенов
Решение: используй claude-sonnet или claude-haiku для бота
         (урок 2.5 — выбор модели по цене)
```

---

## Практика

### Задание 1: Эхо-бот

Создай бота через BotFather, получи токен, запусти `echo_bot.py`. Убедись, что бот повторяет сообщения.

### Задание 2: AI-бот

Замени эхо на Claude (`ai_bot.py`). Задай боту несколько вопросов подряд — убедись, что он помнит контекст (спроси "как меня зовут" после того, как представишься).

### Задание 3: Добавь системный промпт

Измени `system` в вызове Claude, чтобы бот вёл себя по-другому:

```python
# Вариант 1: бот-переводчик
system="Ты — переводчик. Переводи всё, что пишет пользователь, на английский."

# Вариант 2: бот-учитель
system="Ты — учитель Python. Объясняй всё простыми словами с примерами кода."

# Вариант 3: бот с характером
system="Ты — пират. Говори как пират, но при этом давай полезные ответы."
```

---

## Задачки на закрепление

**Задача 1:** Зачем нужен файл `.env`?

<details>
<summary>Ответ</summary>

Файл `.env` хранит секретные данные (токены, API-ключи) отдельно от кода. Код можно безопасно загрузить в GitHub, а `.env` остаётся только на твоём компьютере (если добавить его в `.gitignore`). Это защита от утечки ключей.
</details>

**Задача 2:** Зачем ограничивать историю до 20 сообщений?

<details>
<summary>Ответ</summary>

Каждое сообщение в истории — это токены, а токены стоят денег (урок 2.5). Если хранить всю историю, через 100 сообщений каждый запрос будет стоить в 100 раз дороже. Ограничение в 20 сообщений — баланс между памятью и стоимостью.
</details>

**Задача 3:** В чём разница между polling и webhook?

<details>
<summary>Ответ</summary>

Polling — бот сам спрашивает Telegram о новых сообщениях (проверяет почтовый ящик). Webhook — Telegram сам присылает сообщения на адрес сервера (почтальон приносит). Polling проще (не нужен сервер), webhook эффективнее для продакшна.
</details>

**Задача 4:** Что произойдёт, если Claude вернёт ответ на 5000 символов?

<details>
<summary>Ответ</summary>

Telegram ограничивает одно сообщение до 4096 символов. Поэтому в коде есть проверка: если ответ длиннее 4000 символов, он разбивается на части и отправляется несколькими сообщениями. Без этой проверки бот получил бы ошибку от Telegram.
</details>

---

## Глоссарий

| Термин | Что значит |
|--------|-----------|
| **@BotFather** | Официальный бот Telegram для создания и управления ботами |
| **Токен бота** | Секретный ключ для управления ботом (как API-ключ для Claude) |
| **python-telegram-bot** | SDK (библиотека) для создания Telegram-ботов на Python |
| **Polling** | Способ получения сообщений: бот сам спрашивает Telegram |
| **Webhook** | Способ получения сообщений: Telegram сам присылает на сервер |
| **Handler** | Обработчик — функция, которая реагирует на определённый тип сообщения |
| **CommandHandler** | Обработчик команд (`/start`, `/clear`) |
| **MessageHandler** | Обработчик обычных текстовых сообщений |
| **`.env`** | Файл с секретными переменными (токены, ключи) |
| **`.gitignore`** | Файл, который говорит git: "не загружай это" |

---

## Главное

```
Telegram-бот с AI — это три части:
  1. Telegram SDK — получает/отправляет сообщения
  2. Claude SDK — думает и генерирует ответ
  3. Твой код — соединяет первое со вторым

Минимальный бот:
  1. Создать бота через @BotFather → получить токен
  2. pip install python-telegram-bot anthropic python-dotenv
  3. Написать обработчик: получить текст → отправить в Claude → вернуть ответ
  4. python ai_bot.py → бот работает!

Безопасность:
  ✓ Токены в .env (не в коде)
  ✓ .env в .gitignore (не в git)
  ✓ История ограничена (не тратить деньги)
  ✓ Ошибки обрабатываются (бот не падает)
```

---

## Что дальше?

Сейчас бот работает, пока запущен на твоём компьютере. Закрыла терминал — бот умер. В следующих уроках — как дать боту **постоянную память** (база данных) и **постоянную жизнь** (сервер, который работает 24/7).
