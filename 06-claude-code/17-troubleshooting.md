# Когда что-то не работает

Что-то сломалось. Ошибка на экране. Ничего не происходит. Или происходит не то. Это нормально — у всех так, и чаще чем ты думаешь.

---

## Первое правило

Не паникуй. Ошибки — часть работы. Если есть коммит — можно откатиться. Если нет — тоже не конец света.

---

## Покажи ошибку Claude

**Лучший способ — текст ошибки:**

1. Выдели текст ошибки

2. Скопируй

3. Вставь в чат: «Вот ошибка: [текст]. Что это?»

**Если текст не помогает — скриншот:**

- Сделай скриншот

- Вставь в чат: «Вот что показывает, появляется когда нажимаю кнопку»

> 💡 **Консоль браузера:**
> Правой кнопкой мыши → Inspect → вкладка Console. Там видны ошибки JavaScript (красный текст). Попроси Claude объяснить как открыть, если непонятно.

---

## Типичные ситуации

**Ничего не происходит:**
```
Нажимаю кнопку — ничего. Посмотри файл form.js
```

**Ошибка в браузере:**
```
В консоли вот это: [скриншот]. Объясни и исправь.
```

**Выглядит не так:**
```
Кнопка должна быть справа, но она слева. Посмотри стили.
```

**Раньше работало:**
```
Вчера работало, сегодня нет. Что изменилось?
```

---

## Когда Claude не помогает

1. **Опиши подробнее** — не «не работает», а «не работает когда ввожу email без @»

2. **Покажи что ожидалось** — «должно показывать "Спасибо", а показывает пустую страницу»

3. **Новый чат** — иногда свежий контекст помогает

4. **Разбей на части** — сначала кнопка, потом форма, потом сервер

---

## Откат к рабочей версии

```
Покажи последние коммиты
```
```
Верни проект к коммиту "..."
```

> ⚠️ **Важно:**
> Поэтому коммиты важны! Без них откатиться некуда.

---

## Если зависло

- **Кнопка Stop** — пока Claude думает, нажми Stop

- **Developer: Reload Window** — `Cmd/Ctrl + Shift + P` → «Developer: Reload Window»

- **Перезапуск VS Code** — закрыть и открыть заново

---

## Главный совет

Ошибки — это информация. Они говорят что не так. Не игнорируй текст ошибки. Читай, показывай Claude, разбирайся.

Каждая исправленная ошибка — новые знания.

---

## Тест

<form id="test-form" data-lesson="cc-17">
<div class="test__question" data-correct="b">
<p><strong>1. Что делать первым при ошибке?</strong></p>
<label class="test__option"><input type="radio" name="q1" value="a"> Удалить проект</label>
<label class="test__option"><input type="radio" name="q1" value="b"> Скопировать текст ошибки и показать Claude</label>
<label class="test__option"><input type="radio" name="q1" value="c"> Перезагрузить компьютер</label>
</div>
<div class="test__question" data-correct="a">
<p><strong>2. Как открыть консоль браузера?</strong></p>
<label class="test__option"><input type="radio" name="q2" value="a"> Правая кнопка мыши → Inspect → Console</label>
<label class="test__option"><input type="radio" name="q2" value="b"> File → Open Console</label>
<label class="test__option"><input type="radio" name="q2" value="c"> Установить расширение</label>
</div>
<div class="test__question" data-correct="c">
<p><strong>3. Что делать если Claude зависает?</strong></p>
<label class="test__option"><input type="radio" name="q3" value="a"> Ждать бесконечно</label>
<label class="test__option"><input type="radio" name="q3" value="b"> Закрыть ноутбук</label>
<label class="test__option"><input type="radio" name="q3" value="c"> Нажать Stop или Developer: Reload Window</label>
</div>
</form>
<button id="test-submit">Проверить ответы</button>
<div id="test-result" class="test__result" style="display:none"></div>
