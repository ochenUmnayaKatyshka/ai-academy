# Режимы работы

Claude Code умеет работать по-разному: осторожно спрашивать каждый шаг или действовать автономно.

---

## Режимы редактирования

Внизу панели Claude Code — кнопка режима. Три варианта:

**1. Plan Mode** — только думает и планирует, код не трогает.

**2. Ask before edits** — показывает каждое изменение и ждёт подтверждения. Самый безопасный.

**3. Edit automatically** — применяет изменения без подтверждения. Быстро, но рискованнее.

> 💡 **Какой выбрать:**
>
> - Начинающим — Ask Before Edit
>
> - Когда доверяешь задаче — Auto Edit

---

## Когда автоматический режим

**Хорошо для:**

- Простые задачи

- Массовое форматирование

- Создание по шаблону

- Когда рядом и следишь

**Плохо для:**

- Удаление файлов

- Работа с конфигурациями

- Что-то делаешь впервые

- Отошёл от компьютера

> ⚠️ **Важно:**
> Даже в автоматическом режиме CLAUDE.md работает.

---

## Режим думания

Рядом с полем ввода — переключатель extended thinking.

**Обычный:** быстрые ответы для простых задач.

**Расширенное думание:** дольше, но глубже. Для сложных задач: архитектура, отладка, планирование.

> 💡 **Когда включать:**
>
> - Сложная задача с множеством файлов
>
> - Нужно продумать архитектуру
>
> - Баг который не можешь найти

---

## Выделение контекста

Выделяешь код в редакторе — Claude видит что именно. Внизу панели: «X lines selected».

- Выдели код мышкой

- Он автоматически добавляется в контекст

- Спрашивай про конкретный фрагмент

---

## Тест

<form id="test-form" data-lesson="cc-19">
<div class="test__question" data-correct="b">
<p><strong>1. Что делает Auto Edit?</strong></p>
<label class="test__option"><input type="radio" name="q1" value="a"> Только планирует</label>
<label class="test__option"><input type="radio" name="q1" value="b"> Применяет изменения без подтверждения</label>
<label class="test__option"><input type="radio" name="q1" value="c"> Удаляет файлы</label>
</div>
<div class="test__question" data-correct="a">
<p><strong>2. Когда включать расширенное думание?</strong></p>
<label class="test__option"><input type="radio" name="q2" value="a"> Для сложных задач с множеством файлов</label>
<label class="test__option"><input type="radio" name="q2" value="b"> Для простых вопросов</label>
<label class="test__option"><input type="radio" name="q2" value="c"> Всегда</label>
</div>
<div class="test__question" data-correct="c">
<p><strong>3. Какой режим безопаснее для начинающих?</strong></p>
<label class="test__option"><input type="radio" name="q3" value="a"> Auto Edit</label>
<label class="test__option"><input type="radio" name="q3" value="b"> Plan Mode</label>
<label class="test__option"><input type="radio" name="q3" value="c"> Ask Before Edit</label>
</div>
</form>
<button id="test-submit">Проверить ответы</button>
<div id="test-result" class="test__result" style="display:none"></div>
