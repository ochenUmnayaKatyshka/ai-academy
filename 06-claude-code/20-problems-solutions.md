# Проблемы и решения

VS Code + Claude Code — два продукта которые работают вместе. Иногда бывают нюансы. Это нормально.

---

## Известные проблемы

### 1. Серый экран / зависание

**Что:** нажимаешь подтверждение несколько раз быстро — интерфейс виснет.

**Решение:** закрой вкладку, открой новую панель Claude Code. История сохранится.

> 💡 Не торопись с подтверждениями. Один клик, подождал, следующий.

### 2. История чатов не загружается

**Что:** открываешь старый чат из истории — пустой экран, бесконечная загрузка или ошибка. Это известная проблема расширения Claude Code. Чаты сохраняются, но не всегда корректно восстанавливаются.

**Решение:** подожди минуту. Попробуй Developer: Reload Window. Если не помогает — начни новый чат.

**Как с этим жить:**

- Не рассчитывай что вернёшься к старому чату через неделю — может не открыться

- Важные решения и выводы фиксируй в файлах проекта (docs/, CLAUDE.md), а не держи только в чате

- Если чат важный — сделай скриншот ключевых моментов

### 3. Бесконечная загрузка

**Что:** Claude «думает» бесконечно, спиннер крутится.

**Решение:** проверь интернет. Нажми Stop. Отправь снова. Developer: Reload Window.

### 4. Высокое потребление памяти

**Что:** VS Code тормозит, вентиляторы шумят.

**Решение:** перезапусти VS Code. Закрой ненужные чаты. Используй `/compact`.

---

## Универсальное решение

`Cmd/Ctrl + Shift + P` → **Developer: Reload Window**

VS Code перезагрузится без закрытия. Решает 80% проблем.

---

## Профилактика

1. **Коммиты чаще** — при зависании несохранённая работа потеряется

2. **Не торопись** — быстрые клики → зависания

3. **Обновляй расширение** — новые версии содержат исправления

4. **Перезапускай** — раз в несколько часов нормальная практика

---

## Тест

<form id="test-form" data-lesson="cc-20">
<div class="test__question" data-correct="b">
<p><strong>1. Что делать если VS Code завис?</strong></p>
<label class="test__option"><input type="radio" name="q1" value="a"> Выбросить компьютер</label>
<label class="test__option"><input type="radio" name="q1" value="b"> Developer: Reload Window</label>
<label class="test__option"><input type="radio" name="q1" value="c"> Удалить VS Code</label>
</div>
<div class="test__question" data-correct="a">
<p><strong>2. Как избежать зависаний?</strong></p>
<label class="test__option"><input type="radio" name="q2" value="a"> Не торопиться с подтверждениями и перезапускать VS Code</label>
<label class="test__option"><input type="radio" name="q2" value="b"> Работать только ночью</label>
<label class="test__option"><input type="radio" name="q2" value="c"> Не использовать Claude Code</label>
</div>
<div class="test__question" data-correct="c">
<p><strong>3. Почему важны частые коммиты?</strong></p>
<label class="test__option"><input type="radio" name="q3" value="a"> Чтобы GitHub выглядел красиво</label>
<label class="test__option"><input type="radio" name="q3" value="b"> Это необязательно</label>
<label class="test__option"><input type="radio" name="q3" value="c"> При зависании или сбое несохранённая работа может потеряться</label>
</div>
</form>
<button id="test-submit">Проверить ответы</button>
<div id="test-result" class="test__result" style="display:none"></div>
