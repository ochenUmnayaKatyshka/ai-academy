# Урок 1.6 — Python: работа с файлами

> Программа работает с данными. Но когда программа завершается — всё, что было в переменных, исчезает. Файлы решают эту проблему: записал данные в файл — они сохранились навсегда.

---

## Зачем программе работать с файлами

Когда ты закрываешь Telegram и открываешь снова — сообщения на месте. Они не исчезли, потому что были сохранены в файл (или базу данных, но принцип тот же).

Без файлов:
- Настройки сбрасываются при каждом запуске
- История действий теряется
- AI-агент забывает всё, что знал

С файлами:
- Агент помнит предыдущие разговоры
- Настройки сохраняются между запусками
- Логи записываются для анализа

---

## Чтение файла

```python
# open() — открыть файл
# "r" = read = "для чтения"

file = open("notes.txt", "r")
content = file.read()       # .read() — прочитать всё содержимое
file.close()                # .close() — закрыть файл (обязательно!)

print(content)
```

### Лучший способ — with

```python
# with автоматически закрывает файл, когда блок заканчивается
# Не нужно помнить про .close()

with open("notes.txt", "r") as file:
    content = file.read()

print(content)

# "as file" = "назовём открытый файл словом file"
# Всё что с отступом — работа с файлом
# Когда отступ заканчивается — файл автоматически закрыт
```

### Чтение по строкам

```python
# Если файл большой — читаем по строкам, а не весь целиком

with open("messages.txt", "r") as file:
    for line in file:
        print(line)
        # line — одна строка из файла
        # Цикл проходит по каждой строке по очереди
```

---

## Запись в файл

```python
# "w" = write = "для записи"
# ВАЖНО: "w" полностью перезаписывает файл! Старое содержимое удаляется.

with open("notes.txt", "w") as file:
    file.write("Первая строка\n")
    file.write("Вторая строка\n")
    # \n = перенос строки (без него всё слипнется в одну строку)

# Теперь в notes.txt:
# Первая строка
# Вторая строка
```

### Добавление в конец файла

```python
# "a" = append = "добавить в конец"
# Не стирает старое, а дописывает после

with open("log.txt", "a") as file:
    file.write("Пользователь зашёл в 10:00\n")
    file.write("Пользователь нажал кнопку\n")

# Каждый запуск программы — новые строки добавляются в конец
```

**Аналогия:**
- `"w"` — стереть доску и написать заново
- `"a"` — дописать на доску, не стирая

---

## Работа с JSON-файлами

JSON — самый популярный формат для хранения данных в AI-проектах. Настройки, память агента, ответы API — всё это JSON.

### Чтение JSON

```python
import json
# import = "подключить библиотеку"
# json — встроенная библиотека Python для работы с JSON

with open("config.json", "r") as file:
    data = json.load(file)
    # json.load() — прочитать JSON и превратить в Python-словарь

print(data["name"])
print(data["age"])
```

### Запись JSON

```python
import json

user = {
    "name": "Катя",
    "age": 25,
    "skills": ["Python", "терминал"],
    "is_learning": True
}

with open("user.json", "w") as file:
    json.dump(user, file, ensure_ascii=False, indent=4)
    # json.dump() — записать словарь в файл как JSON
    # ensure_ascii=False — чтобы русские буквы не превращались в коды
    # indent=4 — отступы для читаемости

# В файле user.json теперь:
# {
#     "name": "Катя",
#     "age": 25,
#     "skills": ["Python", "терминал"],
#     "is_learning": true
# }
```

---

## Работа с .env файлами

API-ключи хранятся в `.env`. Чтобы читать их из Python — нужна библиотека `python-dotenv`.

```bash
# Сначала установи библиотеку (в терминале)
pip install python-dotenv
```

```python
# файл: .env
# ANTHROPIC_API_KEY=sk-ant-abc123
```

```python
# файл: app.py
import os
from dotenv import load_dotenv

load_dotenv()
# load_dotenv() — читает .env файл и загружает переменные

api_key = os.getenv("ANTHROPIC_API_KEY")
# os.getenv() — получить значение переменной окружения

print(f"Ключ загружен: {api_key[:10]}...")
# [:10] — показываем только первые 10 символов (не светим ключ целиком)
```

---

## Проверка: существует ли файл

```python
import os

# os.path.exists() — проверяет, есть ли файл или папка
if os.path.exists("config.json"):
    print("Файл найден")
else:
    print("Файла нет")
```

---

## Реальный пример: память AI-агента

Агент должен помнить информацию между запусками. Вот как это работает:

```python
import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    # Если файл памяти существует — читаем
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    # Если нет — возвращаем пустую память
    return {"user_name": None, "facts": []}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, ensure_ascii=False, indent=4)

def remember_fact(memory, fact):
    memory["facts"].append(fact)
    save_memory(memory)

# Использование
memory = load_memory()

if memory["user_name"] is None:
    memory["user_name"] = "Катя"
    save_memory(memory)
    print("Приятно познакомиться, Катя!")
else:
    print(f"С возвращением, {memory['user_name']}!")

remember_fact(memory, "Изучает Python")
remember_fact(memory, "Хочет создавать AI-агентов")

print(f"Я помню о тебе: {memory['facts']}")
```

Первый запуск: `Приятно познакомиться, Катя!`
Второй запуск: `С возвращением, Катя!` — потому что имя уже сохранено в файле.

---

## Практика

Создай файл `diary.py`:

```python
import json
import os

DIARY_FILE = "diary.json"

def load_diary():
    if os.path.exists(DIARY_FILE):
        with open(DIARY_FILE, "r") as file:
            return json.load(file)
    return []

def save_diary(entries):
    with open(DIARY_FILE, "w") as file:
        json.dump(entries, file, ensure_ascii=False, indent=4)

def add_entry(entries, text):
    entries.append(text)
    save_diary(entries)
    print(f"Записано: {text}")

# Загружаем дневник
entries = load_diary()

# Добавляем записи
add_entry(entries, "Начала изучать Python")
add_entry(entries, "Узнала что такое функции")
add_entry(entries, "Научилась работать с файлами")

# Показываем все записи
print("\nМой дневник:")
for i, entry in enumerate(entries, 1):
    print(f"  {i}. {entry}")
    # enumerate(entries, 1) — нумерует элементы начиная с 1
```

Запусти: `python3 diary.py`
Запусти ещё раз — записи сохранятся!

---

## Задачки на закрепление

**Задача 1:** В чём разница между `"w"` и `"a"` при открытии файла?

<details>
<summary>Ответ</summary>

`"w"` (write) — стирает всё и пишет заново. Старое содержимое удаляется.
`"a"` (append) — добавляет в конец файла. Старое остаётся.
</details>

**Задача 2:** Напиши код, который читает файл `data.json` и выводит значение поля `"name"`.

<details>
<summary>Ответ</summary>

```python
import json

with open("data.json", "r") as file:
    data = json.load(file)

print(data["name"])
```
</details>

**Задача 3:** Напиши функцию `save_settings(settings)`, которая принимает словарь и сохраняет его в `settings.json`.

<details>
<summary>Ответ</summary>

```python
import json

def save_settings(settings):
    with open("settings.json", "w") as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)

save_settings({"theme": "dark", "language": "ru", "notifications": True})
```
</details>

**Задача 4:** Зачем нужен `with` при работе с файлами? Что будет без него?

<details>
<summary>Ответ</summary>

`with` автоматически закрывает файл, когда блок кода заканчивается. Без него нужно вручную вызывать `file.close()`. Если забыть — файл останется открытым, данные могут не сохраниться, а программа будет тратить ресурсы.
</details>

**Задача 5:** Напиши программу, которая добавляет новую строку в файл `log.txt` каждый раз при запуске.

<details>
<summary>Ответ</summary>

```python
with open("log.txt", "a") as file:
    file.write("Программа запущена\n")

with open("log.txt", "r") as file:
    print(file.read())
```
</details>

---

## Глоссарий

| Термин | Что значит |
|--------|-----------|
| open() | Функция для открытия файла — указываешь имя, режим и кодировку |
| read() | Метод, который читает всё содержимое открытого файла целиком |
| write() | Метод, который записывает текст в открытый файл |
| with | Конструкция, которая автоматически закрывает файл после окончания работы с ним |
| Режим "r" / "w" / "a" | Режимы открытия файла: чтение (read), запись с нуля (write), дозапись в конец (append) |
| encoding | Параметр кодировки — указывай "utf-8", чтобы русские буквы читались правильно |
| json.load() | Функция, которая читает JSON-файл и превращает его в словарь Python |
| json.dump() | Функция, которая записывает словарь Python в файл в формате JSON |
| .env | Файл для хранения секретов (ключей, паролей), который не попадает в Git |
| dotenv | Библиотека python-dotenv для загрузки переменных из файла .env |
| load_dotenv() | Функция, которая загружает переменные из .env в окружение программы |
| os.getenv() | Функция, которая достаёт значение переменной окружения по имени |

---

## Главное

```
1. open() открывает файл, with — гарантирует, что файл закроется автоматически.
2. Режимы: "r" — читать, "w" — писать с нуля, "a" — дописать в конец.
3. Всегда указывай encoding="utf-8" — иначе русский текст может сломаться.
4. read() читает весь файл, write() записывает строку в файл.
5. JSON — универсальный формат для структурированных данных (настройки, ответы API).
6. json.load() читает JSON из файла, json.dump() записывает в файл.
7. Секреты (API-ключи, пароли) хранятся в .env и загружаются через load_dotenv().
8. os.getenv("ИМЯ") достаёт значение секрета — в коде ключ никогда не пишется напрямую.
9. .env добавляй в .gitignore, чтобы секреты не попали в GitHub.
```

---

## Что дальше?

В следующем уроке — **Git и GitHub**. Научишься сохранять версии кода, откатываться к предыдущим и делиться проектом с другими.
