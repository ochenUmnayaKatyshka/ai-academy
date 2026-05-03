# Настольная книга команд

> Распечатай и держи рядом. Всё, что нужно — на одном листе.
> Этот документ пополняется по мере прохождения курса.

---

## 1. Навигация по файловой системе

| Команда | Что делает | Пример |
|---------|-----------|--------|
| `pwd` | Показать текущую папку | `pwd` → `/Users/katya/Projects` |
| `ls` | Список файлов | `ls` |
| `ls -la` | Все файлы + скрытые + детали | `ls -la` |
| `cd папка` | Зайти в папку | `cd Documents` |
| `cd ..` | На уровень вверх | `cd ..` |
| `cd ~` | В домашнюю папку | `cd ~` |
| `cd /` | В корень системы | `cd /` |

## 2. Работа с файлами и папками

| Команда | Что делает | Пример |
|---------|-----------|--------|
| `mkdir имя` | Создать папку | `mkdir my-project` |
| `mkdir -p a/b/c` | Создать вложенные папки | `mkdir -p src/components/ui` |
| `touch файл` | Создать пустой файл | `touch app.py` |
| `cp откуда куда` | Копировать | `cp file.txt backup.txt` |
| `cp -r папка новая` | Копировать папку | `cp -r src src-backup` |
| `mv откуда куда` | Переместить / переименовать | `mv old.py new.py` |
| `rm файл` | Удалить файл | `rm temp.txt` |
| `rm -r папка` | Удалить папку с содержимым | `rm -r old-folder` |
| `cat файл` | Показать содержимое | `cat config.json` |

## 3. Python

| Команда | Что делает | Пример |
|---------|-----------|--------|
| `python3 --version` | Проверить версию Python | `python3 --version` |
| `python3 файл.py` | Запустить скрипт | `python3 app.py` |
| `python3 -m venv env` | Создать виртуальное окружение | `python3 -m venv .venv` |
| `source env/bin/activate` | Активировать окружение | `source .venv/bin/activate` |
| `deactivate` | Выйти из окружения | `deactivate` |
| `pip install пакет` | Установить библиотеку | `pip install anthropic` |
| `pip install -r файл` | Установить из списка | `pip install -r requirements.txt` |
| `pip list` | Список установленных пакетов | `pip list` |
| `pip freeze > файл` | Сохранить список пакетов | `pip freeze > requirements.txt` |

## 4. Git — контроль версий

| Команда | Что делает | Пример |
|---------|-----------|--------|
| `git init` | Создать репозиторий | `git init` |
| `git status` | Что изменилось? | `git status` |
| `git add файл` | Подготовить к сохранению | `git add app.py` |
| `git add .` | Подготовить всё | `git add .` |
| `git commit -m "текст"` | Сохранить версию | `git commit -m "добавил авторизацию"` |
| `git log --oneline` | История изменений | `git log --oneline` |
| `git push` | Отправить на GitHub | `git push` |
| `git pull` | Скачать обновления | `git pull` |
| `git clone url` | Скачать репозиторий | `git clone https://github.com/user/repo` |
| `git branch имя` | Создать ветку | `git branch feature-login` |
| `git checkout ветка` | Переключиться на ветку | `git checkout feature-login` |

## 5. Node.js и npm

| Команда | Что делает | Пример |
|---------|-----------|--------|
| `node --version` | Проверить версию Node | `node --version` |
| `npm init -y` | Создать проект | `npm init -y` |
| `npm install пакет` | Установить пакет | `npm install express` |
| `npm install -g пакет` | Установить глобально | `npm install -g openclaw` |
| `npm run скрипт` | Запустить скрипт | `npm run start` |
| `npx команда` | Запустить без установки | `npx create-next-app` |

## 6. Серверы и сеть

| Команда | Что делает | Пример |
|---------|-----------|--------|
| `ssh user@ip` | Подключиться к серверу | `ssh root@192.168.1.100` |
| `scp файл user@ip:путь` | Скопировать файл на сервер | `scp app.py root@server:/home/` |
| `curl url` | Сделать HTTP-запрос | `curl https://api.example.com` |
| `ping адрес` | Проверить доступность | `ping google.com` |
| `lsof -i :порт` | Кто занимает порт? | `lsof -i :3000` |
| `kill PID` | Остановить процесс | `kill 12345` |

## 7. Docker

| Команда | Что делает | Пример |
|---------|-----------|--------|
| `docker ps` | Запущенные контейнеры | `docker ps` |
| `docker images` | Список образов | `docker images` |
| `docker run образ` | Запустить контейнер | `docker run -d nginx` |
| `docker stop id` | Остановить контейнер | `docker stop abc123` |
| `docker-compose up` | Запустить всё из compose | `docker-compose up -d` |
| `docker-compose down` | Остановить всё | `docker-compose down` |

## 8. Переменные окружения и конфиг

| Команда | Что делает | Пример |
|---------|-----------|--------|
| `echo $ПЕРЕМЕННАЯ` | Показать значение | `echo $PATH` |
| `export KEY=value` | Установить переменную | `export API_KEY=sk-123` |
| `cat .env` | Показать файл окружения | `cat .env` |
| `chmod 600 файл` | Ограничить доступ | `chmod 600 .env` |

## 9. Быстрые комбинации в терминале

| Комбинация | Что делает |
|-----------|-----------|
| `Tab` | Автодополнение команды/пути |
| `Ctrl+C` | Остановить текущую команду |
| `Ctrl+L` | Очистить экран |
| `↑ / ↓` | История предыдущих команд |
| `Ctrl+R` | Поиск по истории команд |
| `Ctrl+A` | Курсор в начало строки |
| `Ctrl+E` | Курсор в конец строки |

---

*Последнее обновление: Этап 1*
