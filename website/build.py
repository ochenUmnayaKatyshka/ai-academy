#!/usr/bin/env python3
"""
Скрипт для генерации HTML-страниц уроков из .md файлов.
Запуск: python3 build.py
"""

import os
import markdown

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COURSE_DIR = os.path.dirname(BASE_DIR)  # ai-academy/
OUTPUT_DIR = os.path.join(BASE_DIR, 'lessons')

# Lesson definitions: (lesson_id, html_filename, md_path, title, stage, lesson_num, stage_total)
LESSONS = [
    # Stage 1 — Фундамент
    ('0-0-setup',        '0-0-setup.html',        '01-fundament/00-setup.md',              'Подготовка',            1, 1, 8),
    ('1-1-terminal',     '1-1-terminal.html',      '01-fundament/01-terminal.md',           'Терминал',              1, 2, 8),
    ('1-2-files',        '1-2-files.html',         '01-fundament/02-files-and-formats.md',  'Файлы и форматы',       1, 3, 8),
    ('1-3-variables',    '1-3-variables.html',      '01-fundament/03-python-variables.md',   'Переменные и типы',     1, 4, 8),
    ('1-4-conditions',   '1-4-conditions.html',     '01-fundament/04-conditions-and-loops.md','Условия и циклы',      1, 5, 8),
    ('1-5-functions',    '1-5-functions.html',      '01-fundament/05-functions.md',          'Функции',               1, 6, 8),
    ('1-6-working-files','1-6-working-files.html',  '01-fundament/06-working-with-files.md', 'Работа с файлами',     1, 7, 8),
    ('1-7-git',          '1-7-git.html',            '01-fundament/07-git-and-github.md',     'Git и GitHub',          1, 8, 8),
    # Stage 2 — Понимание AI
    ('2-1-llm',          '2-1-llm.html',            '02-understanding-ai/01-what-is-llm.md',      'Что такое LLM',              2, 1, 6),
    ('2-2-api',          '2-2-api.html',            '02-understanding-ai/02-api.md',               'API — язык программ',        2, 2, 6),
    ('2-3-first-api',    '2-3-first-api.html',      '02-understanding-ai/03-first-api-call.md',    'Первый вызов Claude API',    2, 3, 6),
    ('2-4-prompts',      '2-4-prompts.html',        '02-understanding-ai/04-prompt-engineering.md','Prompt Engineering',         2, 4, 6),
    ('2-5-tokens',       '2-5-tokens.html',         '02-understanding-ai/05-tokens-and-cost.md',   'Токены и стоимость',         2, 5, 6),
    ('2-6-scripts',      '2-6-scripts.html',        '02-understanding-ai/06-building-with-api.md', 'Скрипты с Claude API',       2, 6, 6),
    # Stage 3 — AI-агенты
    ('3-1-chatbot-vs-agent','3-1-chatbot-vs-agent.html','03-ai-agents/01-chatbot-vs-agent.md','Чат-бот vs Агент',         3, 1, 5),
    ('3-2-tools',        '3-2-tools.html',          '03-ai-agents/02-tools.md',              'Tools — руки агента',       3, 2, 5),
    ('3-3-memory',       '3-3-memory.html',         '03-ai-agents/03-memory.md',             'Память агента',             3, 3, 5),
    ('3-4-agent-sdk',    '3-4-agent-sdk.html',      '03-ai-agents/04-agent-sdk.md',          'Первый агент (SDK)',        3, 4, 5),
    ('3-5-multi-step',   '3-5-multi-step.html',     '03-ai-agents/05-multi-step.md',         'Мульти-шаговые задачи',    3, 5, 5),
    # Stage 4 — Продукты
    ('4-1-telegram',     '4-1-telegram.html',       '04-products/01-telegram-bot.md',        'Telegram-бот с AI',         4, 1, 5),
    ('4-2-databases',    '4-2-databases.html',      '04-products/02-databases.md',           'Базы данных',               4, 2, 5),
    ('4-3-deploy',       '4-3-deploy.html',         '04-products/03-server-and-deploy.md',   'Сервер и деплой',           4, 3, 5),
    ('4-4-platforms',    '4-4-platforms.html',       '04-products/04-platforms.md',           'Платформы и OpenClaw',      4, 4, 5),
    ('4-5-security',     '4-5-security.html',       '04-products/05-security.md',            'Безопасность',              4, 5, 5),
    # Stage 5 — Эксперт
    ('5-1-rag',          '5-1-rag.html',            '05-expert/01-rag.md',                   'RAG — поиск по данным',     5, 1, 5),
    ('5-2-multi-agent',  '5-2-multi-agent.html',    '05-expert/02-multi-agent.md',           'Мульти-агентные системы',   5, 2, 5),
    ('5-3-fine-tuning',  '5-3-fine-tuning.html',    '05-expert/03-fine-tuning.md',           'Fine-tuning',               5, 3, 5),
    ('5-4-optimization', '5-4-optimization.html',   '05-expert/04-optimization.md',          'Оптимизация и стоимость',   5, 4, 5),
    ('5-5-architecture', '5-5-architecture.html',   '05-expert/05-architecture.md',          'Архитектура AI-продуктов',  5, 5, 5),
]

STAGE_NAMES = {
    1: 'Фундамент',
    2: 'Понимание AI',
    3: 'AI-агенты',
    4: 'Продукты',
    5: 'Эксперт'
}

INLINE_CSS = """
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0a0a0a;color:#e5e5e5;font-size:16px;line-height:1.6;min-height:100vh}
a{color:#6b8afd;text-decoration:none}a:hover{color:#8ba4fd}
.container{max-width:640px;margin:0 auto;padding:0 20px}
.container--wide{max-width:720px}
.lesson-header{display:flex;justify-content:space-between;align-items:center;padding:20px;border-bottom:1px solid #1a1a1a}
.lesson-header__back{font-size:14px;color:#6b8afd;display:flex;align-items:center;gap:6px}
.lesson-header__meta{font-size:13px;color:#666}
.lesson-video{margin:32px 0}
.lesson-video__player{width:100%;aspect-ratio:16/9;border-radius:12px;border:1px solid #2a2a2a;background:#141414;overflow:hidden}
.lesson-video__player iframe{width:100%;height:100%;border:none}
.lesson-content{padding:32px 0}
.lesson-content h1{font-size:28px;font-weight:700;color:#fff;margin-bottom:16px;line-height:1.3}
.lesson-content h2{font-size:22px;font-weight:600;color:#fff;margin-top:40px;margin-bottom:16px;padding-top:24px;border-top:1px solid #1a1a1a}
.lesson-content h3{font-size:18px;font-weight:600;color:#e5e5e5;margin-top:28px;margin-bottom:12px}
.lesson-content h4{font-size:16px;font-weight:600;color:#e5e5e5;margin-top:20px;margin-bottom:8px}
.lesson-content p{margin-bottom:16px;color:#ccc}
.lesson-content strong{color:#e5e5e5;font-weight:600}
.lesson-content em{color:#aaa}
.lesson-content blockquote{border-left:3px solid #6b8afd;padding:12px 16px;margin:16px 0;background:#111;border-radius:0 8px 8px 0;color:#aaa;font-style:italic}
.lesson-content ul,.lesson-content ol{margin:12px 0 16px 24px;color:#ccc}
.lesson-content li{margin-bottom:6px}
.lesson-content hr{border:none;border-top:1px solid #1a1a1a;margin:32px 0}
.lesson-content pre{background:#1a1a1a;border:1px solid #2a2a2a;border-radius:8px;padding:16px;overflow-x:auto;margin:16px 0;position:relative}
.lesson-content code{font-family:'JetBrains Mono','Fira Code','Consolas',monospace;font-size:14px;line-height:1.5}
.lesson-content p code,.lesson-content li code{background:#1a1a1a;padding:2px 6px;border-radius:4px;font-size:14px;color:#e5a0e0}
.lesson-content pre code{background:none;padding:0;color:#e5e5e5}
.code-block{position:relative}
.copy-btn{position:absolute;top:8px;right:8px;background:#2a2a2a;border:1px solid #3a3a3a;color:#888;padding:4px 10px;border-radius:6px;font-size:12px;cursor:pointer;transition:all .2s;font-family:inherit}
.copy-btn:hover{background:#3a3a3a;color:#e5e5e5}
.lesson-content table{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}
.lesson-content th{background:#1a1a1a;padding:10px 12px;text-align:left;font-weight:600;color:#e5e5e5;border-bottom:1px solid #2a2a2a}
.lesson-content td{padding:10px 12px;border-bottom:1px solid #1a1a1a;color:#ccc}
.lesson-content details{background:#111;border:1px solid #2a2a2a;border-radius:8px;margin:12px 0;overflow:hidden}
.lesson-content summary{padding:12px 16px;cursor:pointer;font-weight:600;color:#6b8afd;user-select:none}
.lesson-content summary:hover{color:#8ba4fd}
.lesson-content details[open] summary{border-bottom:1px solid #1a1a1a}
.lesson-content details>*:not(summary){padding:0 16px}
.lesson-content details>p:first-of-type{padding-top:12px}
.lesson-content img{max-width:100%;border-radius:8px;margin:16px 0}
.lesson-nav{display:flex;justify-content:space-between;padding:32px 0;margin-top:32px;border-top:1px solid #1a1a1a}
.lesson-nav__btn{font-size:14px;color:#6b8afd;display:flex;align-items:center;gap:6px;padding:10px 16px;border-radius:8px;border:1px solid #2a2a2a;background:#141414;transition:border-color .2s}
.lesson-nav__btn:hover{border-color:#6b8afd;color:#8ba4fd}
.lesson-nav__btn--disabled{color:#444;pointer-events:none;opacity:.5}
@media(max-width:480px){.container{padding:0 16px}.lesson-header{padding:16px}}

.theme-toggle{position:fixed;top:16px;right:16px;background:#1a1a1a;border:1px solid #2a2a2a;border-radius:24px;padding:8px 16px;cursor:pointer;font-size:13px;z-index:100;transition:all .3s;display:flex;align-items:center;gap:8px;color:#888;font-family:inherit}
.theme-toggle:hover{border-color:#6b8afd;color:#e5e5e5}

body.girls{background:#f5f0ed;color:#2a2a2a;font-family:'Georgia','Times New Roman',serif}
body.girls .lesson-header{border-bottom-color:#e0d5d0}
body.girls .lesson-header__back{color:#c47a8a}
body.girls .lesson-header__meta{color:#9a8a8a}
body.girls a{color:#c47a8a}body.girls a:hover{color:#a05a6a}
body.girls .lesson-content h1,body.girls .lesson-content h2{color:#3a3a3a;font-family:'Georgia',serif;font-weight:400}
body.girls .lesson-content h3,body.girls .lesson-content h4{color:#4a4a4a;font-family:'Georgia',serif;font-weight:400}
body.girls .lesson-content p{color:#5a5a5a;font-family:'Georgia',serif}
body.girls .lesson-content strong{color:#3a3a3a}
body.girls .lesson-content em{color:#7a6a6a}
body.girls .lesson-content blockquote{border-left-color:#d4a0aa;background:#faf5f3;color:#7a6a6a}
body.girls .lesson-content pre{background:#faf5f3;border-color:#e0d5d0}
body.girls .lesson-content code{color:#8a5a6a}
body.girls .lesson-content pre code{color:#5a4a4a}
body.girls .lesson-content p code,body.girls .lesson-content li code{color:#8a5a6a;background:#faf5f3}
body.girls .lesson-content ul,body.girls .lesson-content ol{color:#5a5a5a}
body.girls .lesson-content th{background:#faf5f3;color:#3a3a3a;border-bottom-color:#e0d5d0}
body.girls .lesson-content td{border-bottom-color:#ece5e0;color:#5a5a5a}
body.girls .lesson-content hr{border-top-color:#e0d5d0}
body.girls .lesson-content details{background:#faf5f3;border-color:#e0d5d0}
body.girls .lesson-content summary{color:#c47a8a}
body.girls .lesson-content details[open] summary{border-bottom-color:#e0d5d0}
body.girls .lesson-nav{border-top-color:#e0d5d0}
body.girls .lesson-nav__btn{background:#fff;border-color:#e0d5d0;color:#c47a8a}
body.girls .lesson-nav__btn:hover{border-color:#c47a8a}
body.girls .copy-btn{background:#ece5e0;border-color:#e0d5d0;color:#8a7a7a}
body.girls .theme-toggle{background:#fff;border-color:#e0d5d0;color:#9a8a8a}
body.girls .theme-toggle:hover{border-color:#c47a8a;color:#3a3a3a}
"""

INLINE_JS = """
(function(){
  'use strict';
  var STORAGE_KEY='ai-academy-progress';
  function getProgress(){try{return JSON.parse(localStorage.getItem(STORAGE_KEY))||{}}catch(e){return{}}}
  function saveProgress(p){localStorage.setItem(STORAGE_KEY,JSON.stringify(p))}
  function isCompleted(id){return!!getProgress()[id]}
  function markCompleted(id){var p=getProgress();p[id]=true;saveProgress(p)}
  function initTest(){
    var f=document.getElementById('test-form');if(!f)return;
    var btn=document.getElementById('test-submit'),res=document.getElementById('test-result'),lid=f.getAttribute('data-lesson');
    if(isCompleted(lid)){res.innerHTML='\\u2705 Урок пройден!';res.className='test__result test__result--pass';res.style.display='block'}
    btn.addEventListener('click',function(){
      var qs=f.querySelectorAll('.test__question'),total=qs.length,correct=0;
      qs.forEach(function(q){var ca=q.getAttribute('data-correct'),sel=q.querySelector('input[type=radio]:checked'),opts=q.querySelectorAll('.test__option');
        opts.forEach(function(o){o.classList.remove('test__option--correct','test__option--wrong')});
        if(sel){if(sel.value===ca){correct++;sel.closest('.test__option').classList.add('test__option--correct')}else{sel.closest('.test__option').classList.add('test__option--wrong');opts.forEach(function(o){var r=o.querySelector('input[type=radio]');if(r&&r.value===ca)o.classList.add('test__option--correct')})}}});
      if((correct/total)*100>=80){res.innerHTML='\\u2705 '+correct+' из '+total+' правильно — урок пройден!';res.className='test__result test__result--pass';markCompleted(lid)}
      else{res.innerHTML='\\u274c '+correct+' из '+total+' правильно. Нужно \\u226580%. Попробуйте ещё раз!';res.className='test__result test__result--fail'}
      res.style.display='block'});
  }
  function initCopy(){
    document.querySelectorAll('.lesson-content pre').forEach(function(pre){
      var w=document.createElement('div');w.className='code-block';pre.parentNode.insertBefore(w,pre);w.appendChild(pre);
      var b=document.createElement('button');b.className='copy-btn';b.textContent='Копировать';
      b.addEventListener('click',function(){var c=pre.querySelector('code'),t=c?c.textContent:pre.textContent;navigator.clipboard.writeText(t).then(function(){b.textContent='Скопировано!';setTimeout(function(){b.textContent='Копировать'},1500)})});
      w.appendChild(b)});
  }
  document.addEventListener('DOMContentLoaded',function(){initTest();initCopy()});
})();
"""

def get_lesson_html_template(title, stage, lesson_num, stage_total, lesson_id, content_html, prev_link, next_link):
    stage_name = STAGE_NAMES[stage]

    prev_btn = f'<a href="{prev_link}" class="lesson-nav__btn">\u2190 Предыдущий</a>' if prev_link else '<span class="lesson-nav__btn lesson-nav__btn--disabled">\u2190 Предыдущий</span>'
    next_btn = f'<a href="{next_link}" class="lesson-nav__btn">Следующий \u2192</a>' if next_link else '<span class="lesson-nav__btn lesson-nav__btn--disabled">Следующий \u2192</span>'

    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — AI Academy</title>
  <style>{INLINE_CSS}</style>
</head>
<body>

  <button class="theme-toggle" onclick="toggleTheme()">
    <span id="theme-icon">\U0001F338</span> <span id="theme-label">\u0434\u043b\u044f \u0434\u0435\u0432\u043e\u0447\u0435\u043a</span>
  </button>

  <div class="lesson-header">
    <a href="../index.html" class="lesson-header__back">\u2190 Назад к курсу</a>
    <span class="lesson-header__meta">Этап {stage} \u00b7 Урок {lesson_num} из {stage_total}</span>
  </div>

  <div class="container container--wide">
    <div class="lesson-content">
      {content_html}
    </div>
  </div>

  <div class="container container--wide">
    <div class="lesson-nav">
      {prev_btn}
      {next_btn}
    </div>
  </div>

  <script>{INLINE_JS}</script>
  <script>
function toggleTheme(){{var b=document.body,i=document.getElementById('theme-icon'),l=document.getElementById('theme-label');if(b.classList.contains('girls')){{b.classList.remove('girls');i.textContent='\U0001F338';l.textContent='\u0434\u043b\u044f \u0434\u0435\u0432\u043e\u0447\u0435\u043a';localStorage.setItem('ai-academy-theme','dark')}}else{{b.classList.add('girls');i.textContent='\U0001F4AA';l.textContent='\u043d\u043e\u0440\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u043f\u0430\u0446\u0430\u043d';localStorage.setItem('ai-academy-theme','girls')}}}}
(function(){{var s=localStorage.getItem('ai-academy-theme');if(s==='girls'){{document.body.classList.add('girls');var i=document.getElementById('theme-icon'),l=document.getElementById('theme-label');if(i)i.textContent='\U0001F4AA';if(l)l.textContent='\u043d\u043e\u0440\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u043f\u0430\u0446\u0430\u043d'}}}})();
  </script>
</body>
</html>'''


def build():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    md_converter = markdown.Markdown(
        extensions=['tables', 'fenced_code', 'codehilite', 'md_in_html'],
        extension_configs={
            'codehilite': {'css_class': 'highlight', 'guess_lang': False}
        }
    )

    built = 0
    errors = 0

    for i, lesson in enumerate(LESSONS):
        lesson_id, html_file, md_path, title, stage, lesson_num, stage_total = lesson

        md_full_path = os.path.join(COURSE_DIR, md_path)

        if not os.path.exists(md_full_path):
            print(f'  ❌ Файл не найден: {md_path}')
            errors += 1
            continue

        with open(md_full_path, 'r', encoding='utf-8') as f:
            md_text = f.read()

        md_converter.reset()
        content_html = md_converter.convert(md_text)

        # Prev/next links
        prev_link = LESSONS[i-1][1] if i > 0 else None
        next_link = LESSONS[i+1][1] if i < len(LESSONS) - 1 else None

        html = get_lesson_html_template(
            title, stage, lesson_num, stage_total, lesson_id,
            content_html, prev_link, next_link
        )

        output_path = os.path.join(OUTPUT_DIR, html_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        built += 1
        print(f'  ✅ {html_file} ← {md_path}')

    print(f'\nГотово: {built} уроков сгенерировано, {errors} ошибок')


if __name__ == '__main__':
    print('🔨 Генерация HTML-страниц уроков...\n')
    build()
