# Прикрепление файлов

Иногда нужно показать Claude что-то конкретное: скриншот ошибки, дизайн-макет, документ.

---

## Скриншоты

Самый частый случай — показать ошибку или результат.

1. Сделай скриншот (`Cmd+Shift+4` на Mac, `Win+Shift+S` на Windows)

2. Вставь в поле ввода (`Cmd/Ctrl + V`) или используй `/attach`

3. Напиши сообщение и отправь

Claude увидит изображение и поймёт контекст.

**Примеры:**
```
Вот что показывает браузер. Почему не работает?
[скриншот ошибки]
```
```
Вот макет из Figma. Сделай похожую страницу.
[скриншот дизайна]
```
```
Получилось вот так, но кнопка должна быть справа.
[скриншот результата]
```

> 💡 **Совет:**
> Скриншот + текстовое описание = лучший результат.

---

## Навигация по проекту

Claude умеет искать в проекте:

```
Покажи структуру проекта
```
```
Найди файл где определена функция calculateTotal
```
```
Покажи все места где вызывается API /users
```

---

## Понимание кода

Нашёл файл, но не понимаешь что там:

```
Объясни что делает этот файл
```
```
Как работает функция processOrder?
```

Можно уточнять:
```
А почему здесь async/await?
```

---

## Связи между файлами

```
Какие файлы импортируют utils/helpers.js?
```
```
Покажи цепочку от нажатия кнопки до запроса к серверу
```

> ⚠️ **Важно:**
> В больших проектах такие запросы могут занять время. Claude читает много файлов.

---

## Практика

1. Сделай скриншот чего-нибудь и отправь Claude с вопросом «что это?»

2. Попроси показать структуру проекта

3. Найди файл по функции которая в нём есть

---

## Тест

<form id="test-form" data-lesson="cc-13">
<div class="test__question" data-correct="b">
<p><strong>1. Как прикрепить скриншот к сообщению?</strong></p>
<label class="test__option"><input type="radio" name="q1" value="a"> Сохранить на рабочий стол</label>
<label class="test__option"><input type="radio" name="q1" value="b"> Вставить через Cmd/Ctrl + V в поле ввода</label>
<label class="test__option"><input type="radio" name="q1" value="c"> Отправить по почте</label>
</div>
<div class="test__question" data-correct="a">
<p><strong>2. Что даёт лучший результат при ошибке?</strong></p>
<label class="test__option"><input type="radio" name="q2" value="a"> Скриншот + текстовое описание проблемы</label>
<label class="test__option"><input type="radio" name="q2" value="b"> Только слово «не работает»</label>
<label class="test__option"><input type="radio" name="q2" value="c"> Перезагрузить компьютер</label>
</div>
<div class="test__question" data-correct="c">
<p><strong>3. Может ли Claude найти связи между файлами?</strong></p>
<label class="test__option"><input type="radio" name="q3" value="a"> Нет</label>
<label class="test__option"><input type="radio" name="q3" value="b"> Только в маленьких проектах</label>
<label class="test__option"><input type="radio" name="q3" value="c"> Да, может показать какие файлы связаны друг с другом</label>
</div>
</form>
<button id="test-submit">Проверить ответы</button>
<div id="test-result" class="test__result" style="display:none"></div>
