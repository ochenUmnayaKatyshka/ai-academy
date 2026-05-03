# Создание и изменение файлов

Разберёмся как Claude работает с файлами в VS Code.

---

## Создание файлов

Просто скажи что создать:

```
Создай файл index.html с базовой структурой страницы
```

Или проще:
```
Сделай главную страницу сайта
```

Claude покажет содержимое с зелёным фоном — это новый файл. Нажимаешь Accept — файл появляется в проекте. Если папки не существует — Claude создаст и её.

---

## Чтение файлов

Claude может читать файлы для понимания контекста:

```
Посмотри файл index.html и объясни что там происходит
```

> 💡 **Совет:**
> Claude часто читает файлы сам. Но если хочешь убедиться — укажи явно. Открытый файл автоматически прикрепляется к контексту чата.

---

## Diff: изменения файлов

Когда Claude хочет изменить существующий файл, он показывает **diff** — сравнение двух версий.

> 💡 **Что такое diff:**
> Diff (от «difference» — различие) показывает что изменится: какие строки удалятся, какие добавятся.

Как читать:

- `- старая строка` (красная) — будет удалена

- `+ новая строка` (зелёная) — будет добавлена

**Пример.** Было: `<h1>Привет</h1>`

Запрос: «Сделай заголовок красным»

Diff покажет:
```
- <h1>Привет</h1>
+ <h1 style="color: red;">Привет</h1>
```

> ⚠️ **Важно:**
> Всегда читай diff перед Accept. Claude иногда понимает задачу не так.

---

## Удаление и перемещение

```
Удали файл temp.txt
```
```
Переименуй old.js в new.js
```
```
Перенеси utils.js в папку src/helpers/
```

Claude покажет что делает и попросит подтверждение.

> ⚠️ **Осторожно:**
> Удалённые файлы без Git не восстановить. Сначала сохрани в Git (урок 14).

---

## Массовые операции

Claude справляется с несколькими файлами:
```
Добавь комментарий с датой в начало каждого .js файла
```

Но чем больше файлов — тем внимательнее смотри diff.

---

## Практика

1. Создай файл `notes.md` с текстом «Мои заметки»

2. Добавь список из трёх пунктов

3. Измени первый пункт — посмотри diff

4. Удали файл

Цикл: запрос → diff → подтверждение → результат.

---

## Тест

<form id="test-form" data-lesson="cc-12">
<div class="test__question" data-correct="a">
<p><strong>1. Что означает зелёный цвет в diff?</strong></p>
<label class="test__option"><input type="radio" name="q1" value="a"> Строка будет добавлена</label>
<label class="test__option"><input type="radio" name="q1" value="b"> Строка будет удалена</label>
<label class="test__option"><input type="radio" name="q1" value="c"> Ошибка в коде</label>
</div>
<div class="test__question" data-correct="b">
<p><strong>2. Что делать перед Accept?</strong></p>
<label class="test__option"><input type="radio" name="q2" value="a"> Закрыть глаза</label>
<label class="test__option"><input type="radio" name="q2" value="b"> Прочитать что Claude предлагает изменить</label>
<label class="test__option"><input type="radio" name="q2" value="c"> Перезапустить VS Code</label>
</div>
<div class="test__question" data-correct="c">
<p><strong>3. Может ли Claude создать несколько файлов за раз?</strong></p>
<label class="test__option"><input type="radio" name="q3" value="a"> Нет, только по одному</label>
<label class="test__option"><input type="radio" name="q3" value="b"> Только два</label>
<label class="test__option"><input type="radio" name="q3" value="c"> Да, несколько файлов одним запросом</label>
</div>
</form>
<button id="test-submit">Проверить ответы</button>
<div id="test-result" class="test__result" style="display:none"></div>
