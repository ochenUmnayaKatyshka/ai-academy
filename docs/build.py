#!/usr/bin/env python3
"""
Скрипт для генерации HTML-страниц уроков из .md файлов (V2 — брутальный минимализм).
Запуск: python3 build.py
"""

import os
import markdown

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COURSE_DIR = os.path.dirname(BASE_DIR)  # ai-academy/
OUTPUT_DIR = os.path.join(BASE_DIR, 'lessons')
MATERIALS_OUTPUT_DIR = os.path.join(BASE_DIR, 'materials')

# Materials: (html_filename, md_path, title)
MATERIALS = [
    ('claude-code-guide.html', 'reference/claude-code-friendly-guide.md', 'Claude Code: что и как'),
]

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

# Claude Code lessons
CC_OUTPUT_DIR = os.path.join(BASE_DIR, 'lessons-cc')
CC_LESSONS = [
    ('cc-01', '01-what-is-claude-code.html', '06-claude-code/01-what-is-claude-code.md', 'Что такое Claude Code',         1, 1, 5),
    ('cc-02', '02-vs-code.html',             '06-claude-code/02-vs-code.md',             'Программа VS Code',             1, 2, 5),
    ('cc-03', '03-claude-code-extension.html','06-claude-code/03-claude-code-extension.md','Расширение Claude Code',       1, 3, 5),
    ('cc-04', '04-first-project.html',       '06-claude-code/04-first-project.md',       'Твой первый проект',            1, 4, 5),
    ('cc-05', '05-browser-result.html',      '06-claude-code/05-browser-result.md',      'Смотрим результат в браузере',  1, 5, 5),
    ('cc-06', '06-github.html',              '06-claude-code/06-github.md',              'Подключение GitHub',            2, 1, 3),
    ('cc-07', '07-interface.html',           '06-claude-code/07-interface.md',            'Интерфейс Claude Code',         2, 2, 3),
    ('cc-08', '08-talking-to-claude.html',   '06-claude-code/08-talking-to-claude.md',   'Как разговаривать с Claude',     2, 3, 3),
    ('cc-09', '09-why-docs.html',            '06-claude-code/09-why-docs.md',            'Зачем документация',            3, 1, 3),
    ('cc-10', '10-writing-docs.html',        '06-claude-code/10-writing-docs.md',        'Пишем документацию',            3, 2, 3),
    ('cc-11', '11-improvement-cycle.html',   '06-claude-code/11-improvement-cycle.md',   'Цикл улучшения',               3, 3, 3),
    ('cc-12', '12-create-edit-files.html',   '06-claude-code/12-create-edit-files.md',   'Создание и изменение файлов',   4, 1, 3),
    ('cc-13', '13-attach-files.html',        '06-claude-code/13-attach-files.md',        'Прикрепление файлов',           4, 2, 3),
    ('cc-14', '14-git-save.html',            '06-claude-code/14-git-save.md',            'Git: сохранение работы',        4, 3, 3),
    ('cc-15', '15-research-roles.html',      '06-claude-code/15-research-roles.md',      'Исследование и роли',           5, 1, 8),
    ('cc-16', '16-multiple-chats.html',      '06-claude-code/16-multiple-chats.md',      'Несколько чатов',               5, 2, 8),
    ('cc-17', '17-troubleshooting.html',     '06-claude-code/17-troubleshooting.md',     'Когда что-то не работает',      5, 3, 8),
    ('cc-18', '18-claude-md.html',           '06-claude-code/18-claude-md.md',           'Файл CLAUDE.md',               5, 4, 8),
    ('cc-19', '19-work-modes.html',          '06-claude-code/19-work-modes.md',          'Режимы работы',                 5, 5, 8),
    ('cc-20', '20-problems-solutions.html',  '06-claude-code/20-problems-solutions.md',  'Проблемы и решения',            5, 6, 8),
    ('cc-21', '21-publish-online.html',      '06-claude-code/21-publish-online.md',      'Публикация в интернет',         5, 7, 8),
    ('cc-22', '22-whats-next.html',          '06-claude-code/22-whats-next.md',          'Что дальше',                    5, 8, 8),
]

CC_MODULE_NAMES = {
    1: 'Установка',
    2: 'GitHub и основы',
    3: 'Документация',
    4: 'Работа с файлами',
    5: 'Для продвинутых'
}

INLINE_CSS = """
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  font-family:'Space Mono',monospace;
  background:#f5f5f0;color:#0a0a0a;
  font-size:15px;line-height:1.7;min-height:100vh;
}
body::before{
  content:'';position:fixed;top:0;left:0;width:100%;height:100%;
  background-image:radial-gradient(circle,#000 0.7px,transparent 0.7px);
  background-size:24px 24px;opacity:0.06;pointer-events:none;z-index:0;
}
body>*{position:relative;z-index:1}
a{color:#0a0a0a;text-decoration:none}
.container{max-width:780px;margin:0 auto;padding:0 28px}

/* Header */
.lesson-header{
  display:flex;justify-content:space-between;align-items:center;
  padding:20px 28px;max-width:780px;margin:0 auto;
  border-bottom:1.5px solid #ddd;
}
.lesson-header__back{
  font-size:12px;text-transform:uppercase;letter-spacing:1px;
  font-weight:700;color:#0a0a0a;
}
.lesson-header__back:hover{color:#888}
.lesson-header__meta{font-size:12px;color:#999;text-transform:uppercase;letter-spacing:0.5px}

/* Content */
.lesson-content{padding:40px 0}
.lesson-content h1{
  font-family:'Space Grotesk',sans-serif;
  font-size:32px;font-weight:700;color:#0a0a0a;
  margin-bottom:20px;line-height:1.2;
  text-transform:uppercase;letter-spacing:-1px;
}
.lesson-content h2{
  font-family:'Space Grotesk',sans-serif;
  font-size:22px;font-weight:700;color:#0a0a0a;
  margin-top:48px;margin-bottom:16px;
  padding-top:24px;border-top:1.5px solid #ddd;
  text-transform:uppercase;letter-spacing:-0.5px;
}
.lesson-content h3{
  font-family:'Space Grotesk',sans-serif;
  font-size:18px;font-weight:700;color:#0a0a0a;
  margin-top:32px;margin-bottom:12px;
}
.lesson-content h4{
  font-family:'Space Grotesk',sans-serif;
  font-size:16px;font-weight:700;color:#333;
  margin-top:24px;margin-bottom:8px;
}
.lesson-content p{margin-bottom:16px;color:#333}
.lesson-content strong{color:#0a0a0a;font-weight:700}
.lesson-content em{color:#666;font-style:italic}
.lesson-content blockquote{
  border-left:3px solid #c8e600;
  padding:12px 16px;margin:16px 0;
  background:rgba(200,230,0,0.06);color:#555;
}
.lesson-content ul,.lesson-content ol{margin:12px 0 16px 24px;color:#333}
.lesson-content li{margin-bottom:6px}
.lesson-content hr{border:none;border-top:1.5px solid #ddd;margin:32px 0}

/* Code */
.lesson-content pre{
  background:#1a1a1a;border:1.5px solid #333;
  padding:16px;overflow-x:auto;margin:16px 0;position:relative;
}
.lesson-content code{
  font-family:'Space Mono','JetBrains Mono',monospace;
  font-size:13px;line-height:1.6;
}
.lesson-content p code,.lesson-content li code{
  background:#e8e8e0;padding:2px 6px;font-size:13px;color:#0a0a0a;
}
.lesson-content pre code{background:none;padding:0;color:#e5e5e5}
.code-block{position:relative}
.copy-btn{
  position:absolute;top:8px;right:8px;
  background:#c8e600;border:none;color:#0a0a0a;
  padding:4px 12px;font-size:11px;cursor:pointer;
  font-family:'Space Mono',monospace;font-weight:700;
  text-transform:uppercase;letter-spacing:0.5px;
  transition:all .2s;
}
.copy-btn:hover{background:#b8d600}

/* Tables */
.lesson-content table{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}
.lesson-content th{background:#e8e8e0;padding:10px 12px;text-align:left;font-weight:700;color:#0a0a0a;border-bottom:1.5px solid #ccc}
.lesson-content td{padding:10px 12px;border-bottom:1px solid #ddd;color:#333}

/* Details/spoilers */
.lesson-content details{border:1.5px solid #ddd;margin:12px 0;overflow:hidden}
.lesson-content summary{padding:12px 16px;cursor:pointer;font-weight:700;color:#0a0a0a;user-select:none}
.lesson-content summary:hover{background:rgba(200,230,0,0.1)}
.lesson-content details[open] summary{border-bottom:1.5px solid #ddd}
.lesson-content details>*:not(summary){padding:0 16px}
.lesson-content details>p:first-of-type{padding-top:12px}
.lesson-content img{max-width:560px;width:100%;margin:16px 0;display:block;border-radius:6px}

/* Test */
.test__question{margin-bottom:24px}
.test__option{display:block;padding:8px 12px;margin:6px 0;cursor:pointer;border:1px solid #ddd;transition:all .2s}
.test__option:hover{border-color:#c8e600;background:rgba(200,230,0,0.06)}
.test__option input[type=radio]{margin-right:8px}
.test__option--correct{border-color:#4caf50;background:rgba(76,175,80,0.08)}
.test__option--wrong{border-color:#f44336;background:rgba(244,67,54,0.08)}
#test-submit{
  font-family:'Space Mono',monospace;font-size:13px;font-weight:700;
  background:#c8e600;border:1.5px solid #0a0a0a;color:#0a0a0a;
  padding:10px 24px;cursor:pointer;text-transform:uppercase;letter-spacing:0.5px;
  transition:all .2s;margin-top:8px;
}
#test-submit:hover{background:#b8d600}
.test__result{margin-top:16px;padding:12px 16px;font-weight:700;font-size:14px}
.test__result--pass{background:rgba(76,175,80,0.1);border:1px solid #4caf50;color:#2e7d32}
.test__result--fail{background:rgba(244,67,54,0.1);border:1px solid #f44336;color:#c62828}
.test__note{font-size:12px;color:#999;font-style:italic;margin-bottom:20px;padding:8px 0;border-left:2px solid #ddd;padding-left:12px;opacity:0.8}

/* Dark test */
body.dark .test__option{border-color:#333;color:#bbb}
body.dark .test__option:hover{border-color:#c8e600;background:rgba(200,230,0,0.08)}
body.dark #test-submit{background:#c8e600;border-color:#c8e600;color:#0a0a0a}
body.dark .test__note{color:#666;border-left-color:#333}

/* Girls test */
body.girls .test__option{border-color:#e0d5d0;font-family:'Georgia',serif}
body.girls .test__option:hover{border-color:#c47a8a;background:#faf5f3}
body.girls #test-submit{background:#f8e0e6;border-color:#d0c5c0;color:#c47a8a;font-family:'Georgia',serif}
body.girls .test__note{color:#9a8a8a;border-left-color:#e0d5d0;font-family:'Georgia',serif}

/* Nav */
.lesson-nav{display:flex;justify-content:space-between;padding:32px 0;margin-top:32px;border-top:1.5px solid #ddd}
.lesson-nav__btn{
  font-family:'Space Mono',monospace;
  font-size:12px;color:#0a0a0a;
  display:flex;align-items:center;gap:6px;
  padding:10px 16px;border:1.5px solid #0a0a0a;
  transition:all .2s;text-transform:uppercase;letter-spacing:0.5px;font-weight:700;
}
.lesson-nav__btn:hover{border-color:#c8e600;box-shadow:0 0 0 1.5px #c8e600}
.lesson-nav__btn--disabled{color:#ccc;border-color:#ddd;pointer-events:none}

/* Theme toggle */
.theme-toggle{
  position:fixed;top:20px;right:20px;
  background:#f5f5f0;border:1px solid #ccc;
  padding:6px 14px;cursor:pointer;font-family:'Space Mono',monospace;
  font-size:12px;color:#666;z-index:100;transition:all .2s;
}
.theme-toggle:hover{border-color:#0a0a0a;color:#0a0a0a}

/* ===== DARK THEME ===== */
body.dark{background:#0a0a0a;color:#e5e5e5}
body.dark::before{background-image:radial-gradient(circle,#fff 0.7px,transparent 0.7px);opacity:0.04}
body.dark a{color:#e5e5e5}
body.dark .lesson-header{border-bottom-color:#222}
body.dark .lesson-header__back{color:#e5e5e5}
body.dark .lesson-header__meta{color:#555}
body.dark .lesson-content h1,body.dark .lesson-content h2,body.dark .lesson-content h3,body.dark .lesson-content h4{color:#e5e5e5}
body.dark .lesson-content p{color:#bbb}
body.dark .lesson-content strong{color:#e5e5e5}
body.dark .lesson-content em{color:#888}
body.dark .lesson-content blockquote{background:rgba(200,230,0,0.05);color:#aaa}
body.dark .lesson-content ul,body.dark .lesson-content ol{color:#bbb}
body.dark .lesson-content p code,body.dark .lesson-content li code{background:#1a1a1a;color:#c8e600}
body.dark .lesson-content th{background:#1a1a1a;color:#e5e5e5;border-bottom-color:#333}
body.dark .lesson-content td{border-bottom-color:#222;color:#bbb}
body.dark .lesson-content hr{border-top-color:#222}
body.dark .lesson-content details{border-color:#333}
body.dark .lesson-content details[open] summary{border-bottom-color:#333}
body.dark .lesson-nav{border-top-color:#222}
body.dark .lesson-nav__btn{border-color:#333;color:#e5e5e5}
body.dark .lesson-nav__btn:hover{border-color:#c8e600}
body.dark .lesson-nav__btn--disabled{color:#444;border-color:#222}
body.dark .theme-toggle{background:#111;border-color:#333;color:#888}
body.dark .theme-toggle:hover{border-color:#e5e5e5;color:#e5e5e5}

/* ===== GIRLS THEME ===== */
body.girls{background:#f5f0ed;color:#3a3a3a;font-family:'Georgia','Times New Roman',serif}
body.girls::before{background-image:radial-gradient(circle,#8a6a6a 0.6px,transparent 0.6px);opacity:0.04}
body.girls a{color:#3a3a3a}
body.girls .lesson-header{border-bottom-color:#e0d5d0}
body.girls .lesson-header__back{color:#c47a8a;font-family:'Georgia',serif}
body.girls .lesson-header__meta{color:#9a8a8a;font-family:'Georgia',serif}
body.girls .lesson-content h1,body.girls .lesson-content h2{color:#3a3a3a;font-family:'Georgia',serif;font-weight:400;text-transform:none;letter-spacing:0}
body.girls .lesson-content h3,body.girls .lesson-content h4{color:#4a4a4a;font-family:'Georgia',serif;font-weight:400}
body.girls .lesson-content p{color:#5a5a5a;font-family:'Georgia',serif}
body.girls .lesson-content strong{color:#3a3a3a}
body.girls .lesson-content em{color:#7a6a6a}
body.girls .lesson-content blockquote{border-left-color:#d4a0aa;background:#faf5f3;color:#7a6a6a}
body.girls .lesson-content ul,body.girls .lesson-content ol{color:#5a5a5a}
body.girls .lesson-content pre{background:#faf5f3;border-color:#e0d5d0}
body.girls .lesson-content pre code{color:#5a4a4a}
body.girls .lesson-content p code,body.girls .lesson-content li code{color:#8a5a6a;background:#faf5f3}
body.girls .lesson-content th{background:#faf5f3;color:#3a3a3a;border-bottom-color:#e0d5d0}
body.girls .lesson-content td{border-bottom-color:#ece5e0;color:#5a5a5a}
body.girls .lesson-content hr{border-top-color:#e0d5d0}
body.girls .lesson-content details{border-color:#e0d5d0}
body.girls .lesson-content summary{color:#c47a8a}
body.girls .lesson-content details[open] summary{border-bottom-color:#e0d5d0}
body.girls .lesson-nav{border-top-color:#e0d5d0}
body.girls .lesson-nav__btn{border-color:#d0c5c0;color:#c47a8a;font-family:'Georgia',serif}
body.girls .lesson-nav__btn:hover{border-color:#c47a8a}
body.girls .lesson-nav__btn--disabled{color:#ccc;border-color:#e0d5d0}
body.girls .copy-btn{background:#f8e0e6;color:#c47a8a}
body.girls .theme-toggle{background:#fff;border-color:#e0d5d0;color:#9a8a8a;font-family:'Georgia',serif}
body.girls .theme-toggle:hover{border-color:#c47a8a;color:#3a3a3a}

@media(max-width:640px){
  .container{padding:0 20px}
  .lesson-header{padding:16px 20px}
  .lesson-content h1{font-size:26px}
}
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
      var c=pre.querySelector('code');
      if(!c||!c.className.match(/\\blanguage-/))return;
      var w=document.createElement('div');w.className='code-block';pre.parentNode.insertBefore(w,pre);w.appendChild(pre);
      var b=document.createElement('button');b.className='copy-btn';b.textContent='КОПИРОВАТЬ';
      b.addEventListener('click',function(){var t=c.textContent;navigator.clipboard.writeText(t).then(function(){b.textContent='СКОПИРОВАНО';setTimeout(function(){b.textContent='КОПИРОВАТЬ'},1500)})});
      w.appendChild(b)});
  }
  document.addEventListener('DOMContentLoaded',function(){initTest();initCopy()});
})();
"""

THEME_JS = """
var themes=['light','dark','girls'];
var themeLabels={light:'\\uD83C\\uDF38 для девочек',dark:'\\uD83D\\uDCAA нормальный пацан',girls:'\\u2600 светлая'};
function toggleTheme(){
  var body=document.body;
  var current='light';
  if(body.classList.contains('dark'))current='dark';
  else if(body.classList.contains('girls'))current='girls';
  var idx=themes.indexOf(current);
  var next=themes[(idx+1)%themes.length];
  body.classList.remove('dark','girls');
  if(next!=='light')body.classList.add(next);
  document.getElementById('theme-label').textContent=themeLabels[next];
  localStorage.setItem('ai-academy-theme',next);
}
(function(){
  var saved=localStorage.getItem('ai-academy-theme');
  if(saved&&saved!=='light'){
    document.body.classList.add(saved);
    var el=document.getElementById('theme-label');
    if(el)el.textContent=themeLabels[saved]||themeLabels.light;
  }
})();
"""

GOOGLE_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">'

def get_lesson_html_template(title, stage, lesson_num, stage_total, lesson_id, content_html, prev_link, next_link):
    stage_name = STAGE_NAMES[stage]

    prev_btn = f'<a href="{prev_link}" class="lesson-nav__btn">\u2190 ПРЕДЫДУЩИЙ</a>' if prev_link else '<span class="lesson-nav__btn lesson-nav__btn--disabled">\u2190 ПРЕДЫДУЩИЙ</span>'
    next_btn = f'<a href="{next_link}" class="lesson-nav__btn">СЛЕДУЮЩИЙ \u2192</a>' if next_link else '<span class="lesson-nav__btn lesson-nav__btn--disabled">СЛЕДУЮЩИЙ \u2192</span>'

    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — AI Academy</title>
  {GOOGLE_FONTS}
  <style>{INLINE_CSS}</style>
</head>
<body>

  <button class="theme-toggle" onclick="toggleTheme()">
    <span id="theme-label">\U0001F338 для девочек</span>
  </button>

  <div class="lesson-header">
    <a href="../index.html" class="lesson-header__back">\u2190 НАЗАД К КУРСУ</a>
    <span class="lesson-header__meta">Этап {stage} \u00b7 Урок {lesson_num} из {stage_total}</span>
  </div>

  <div class="container">
    <div class="lesson-content">
      {content_html}
    </div>
  </div>

  <div class="container">
    <div class="lesson-nav">
      {prev_btn}
      {next_btn}
    </div>
  </div>

  <script>{INLINE_JS}</script>
  <script>{THEME_JS}</script>
</body>
</html>'''


def get_cc_lesson_html_template(title, module, lesson_num, module_total, lesson_id, content_html, prev_link, next_link):
    module_name = CC_MODULE_NAMES[module]

    prev_btn = f'<a href="{prev_link}" class="lesson-nav__btn">\u2190 ПРЕДЫДУЩИЙ</a>' if prev_link else '<span class="lesson-nav__btn lesson-nav__btn--disabled">\u2190 ПРЕДЫДУЩИЙ</span>'
    next_btn = f'<a href="{next_link}" class="lesson-nav__btn">СЛЕДУЮЩИЙ \u2192</a>' if next_link else '<span class="lesson-nav__btn lesson-nav__btn--disabled">СЛЕДУЮЩИЙ \u2192</span>'

    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Claude Code — AI Academy</title>
  {GOOGLE_FONTS}
  <style>{INLINE_CSS}</style>
</head>
<body>

  <button class="theme-toggle" onclick="toggleTheme()">
    <span id="theme-label">\U0001F338 для девочек</span>
  </button>

  <div class="lesson-header">
    <a href="../claude-code.html" class="lesson-header__back">\u2190 НАЗАД К CLAUDE CODE</a>
    <span class="lesson-header__meta">Модуль {module}: {module_name} \u00b7 Урок {lesson_num} из {module_total}</span>
  </div>

  <div class="container">
    <div class="lesson-content">
      {content_html}
    </div>
  </div>

  <div class="container">
    <div class="lesson-nav">
      {prev_btn}
      {next_btn}
    </div>
  </div>

  <script>{INLINE_JS}</script>
  <script>{THEME_JS}</script>
</body>
</html>'''


def get_material_html_template(title, content_html):
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Материалы — AI Academy</title>
  {GOOGLE_FONTS}
  <style>{INLINE_CSS}</style>
</head>
<body>

  <button class="theme-toggle" onclick="toggleTheme()">
    <span id="theme-label">\U0001F338 для девочек</span>
  </button>

  <div class="lesson-header">
    <a href="../materials.html" class="lesson-header__back">\u2190 НАЗАД К МАТЕРИАЛАМ</a>
    <span class="lesson-header__meta">Материалы</span>
  </div>

  <div class="container">
    <div class="lesson-content">
      {content_html}
    </div>
  </div>

  <script>{INLINE_JS}</script>
  <script>{THEME_JS}</script>
</body>
</html>'''


def build():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CC_OUTPUT_DIR, exist_ok=True)
    os.makedirs(MATERIALS_OUTPUT_DIR, exist_ok=True)

    md_converter = markdown.Markdown(
        extensions=['tables', 'fenced_code', 'codehilite', 'md_in_html'],
        extension_configs={
            'codehilite': {'css_class': 'highlight', 'guess_lang': False}
        }
    )

    built = 0
    errors = 0

    # Build main course lessons
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

    # Build Claude Code lessons
    cc_built = 0
    cc_errors = 0

    for i, lesson in enumerate(CC_LESSONS):
        lesson_id, html_file, md_path, title, module, lesson_num, module_total = lesson

        md_full_path = os.path.join(COURSE_DIR, md_path)

        if not os.path.exists(md_full_path):
            print(f'  ❌ CC файл не найден: {md_path}')
            cc_errors += 1
            continue

        with open(md_full_path, 'r', encoding='utf-8') as f:
            md_text = f.read()

        md_converter.reset()
        content_html = md_converter.convert(md_text)

        prev_link = CC_LESSONS[i-1][1] if i > 0 else None
        next_link = CC_LESSONS[i+1][1] if i < len(CC_LESSONS) - 1 else None

        html = get_cc_lesson_html_template(
            title, module, lesson_num, module_total, lesson_id,
            content_html, prev_link, next_link
        )

        output_path = os.path.join(CC_OUTPUT_DIR, html_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        cc_built += 1
        print(f'  ✅ [CC] {html_file} ← {md_path}')

    # Build Materials
    materials_built = 0
    materials_errors = 0

    for html_file, md_path, title in MATERIALS:
        md_full_path = os.path.join(COURSE_DIR, md_path)

        if not os.path.exists(md_full_path):
            print(f'  ❌ Material файл не найден: {md_path}')
            materials_errors += 1
            continue

        with open(md_full_path, 'r', encoding='utf-8') as f:
            md_text = f.read()

        md_converter.reset()
        content_html = md_converter.convert(md_text)

        html = get_material_html_template(title, content_html)

        output_path = os.path.join(MATERIALS_OUTPUT_DIR, html_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        materials_built += 1
        print(f'  ✅ [MATERIAL] {html_file} ← {md_path}')

    print(f'\nГотово: {built} уроков + {cc_built} Claude Code уроков + {materials_built} материалов, {errors + cc_errors + materials_errors} ошибок')


if __name__ == '__main__':
    print('🔨 Генерация HTML-страниц уроков (V2)...\n')
    build()
