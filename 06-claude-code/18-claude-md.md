# Файл CLAUDE.md

Один из самых важных инструментов для эффективной работы.

---

## Что это такое

CLAUDE.md — текстовый файл в папке проекта. Claude читает его автоматически при каждом запуске и следует написанным правилам.

> 💡 **Простыми словами:**
> Как инструкция для нового сотрудника: «Вот как мы тут работаем». Пишешь правила — Claude их соблюдает.

---

## Зачем

1. **Не повторять одно и то же** — вместо «не трогай config.json» в каждом сообщении — записал и забыл

2. **Защита от ошибок** — Claude не удалит важный файл и не закоммитит секреты

3. **Специфика проекта** — где-то нельзя трогать определённые папки

4. **Общие правила** — если работаешь с другими

---

## Как создать

**Способ 1:** Напиши `/init` — Claude проанализирует проект и создаст базовые правила.

**Способ 2:** Попроси: `Создай CLAUDE.md с правилами безопасности`

**Способ 3:** Создай файл вручную в корне проекта.

> 💡 **Быстрое добавление:**
> Нажми `#` и напиши правило — Claude сам добавит его в CLAUDE.md.

---

## Где может лежать

```
my-project/
  CLAUDE.md              ← основной, в корне
  frontend/
    CLAUDE.md            ← для подпапки
  CLAUDE.local.md        ← локальный, не в git
```

- В корне — для всего проекта

- В подпапках — для больших проектов

- `CLAUDE.local.md` — личные правила, не добавляй в git

- `~/.claude/CLAUDE.md` — глобальный, для всех проектов

---

## Правила на английском

Claude лучше воспринимает инструкции на английском. Слова-маркеры:

- **NEVER** — строгий запрет

- **ALWAYS** — обязательное действие

- **MUST** — требование

- **IMPORTANT** — важное замечание

> ⚠️ **Важно:**
> Правила на английском, пояснения можно на русском:
> `NEVER commit .env files` — правило
> `# Здесь API ключи` — пояснение

---

## Реальный пример

```markdown
# Project Rules

## 1. NEVER restore previous versions without confirmation
ALWAYS ask before restoring any backup

## 2. Security - NEVER commit credentials
- config.json contains API key - NEVER commit
- .env files - NEVER commit
- ALWAYS check git status before commits

## 3. Git workflow
- Main branch: main
- ALWAYS create descriptive commit messages

## 4. Before deleting
ALWAYS ask before deleting any file

## 5. Project structure
- src/ - main code
- docs/ - documentation
```

Файл короткий, правила конкретные, написаны с NEVER/ALWAYS.

---

## Советы

- **Коротко** — до 500 строк максимум, лучше меньше

- **По необходимости** — Claude накосячил? Добавь правило

- **Чисти** — раз в месяц удали устаревшее

- **Без секретов** — никаких API ключей, файл попадает в git

---

## Тест

<form id="test-form" data-lesson="cc-18">
<div class="test__question" data-correct="a">
<p><strong>1. Что такое CLAUDE.md?</strong></p>
<label class="test__option"><input type="radio" name="q1" value="a"> Файл с правилами, которые Claude соблюдает автоматически</label>
<label class="test__option"><input type="radio" name="q1" value="b"> Документация для пользователей</label>
<label class="test__option"><input type="radio" name="q1" value="c"> Файл с паролями</label>
</div>
<div class="test__question" data-correct="b">
<p><strong>2. На каком языке лучше писать правила?</strong></p>
<label class="test__option"><input type="radio" name="q2" value="a"> Только на русском</label>
<label class="test__option"><input type="radio" name="q2" value="b"> На английском, с NEVER/ALWAYS/MUST</label>
<label class="test__option"><input type="radio" name="q2" value="c"> Без разницы</label>
</div>
<div class="test__question" data-correct="c">
<p><strong>3. Как быстро создать CLAUDE.md?</strong></p>
<label class="test__option"><input type="radio" name="q3" value="a"> Скачать из интернета</label>
<label class="test__option"><input type="radio" name="q3" value="b"> Попросить ChatGPT</label>
<label class="test__option"><input type="radio" name="q3" value="c"> Написать /init в чате Claude Code</label>
</div>
</form>
<button id="test-submit">Проверить ответы</button>
<div id="test-result" class="test__result" style="display:none"></div>
