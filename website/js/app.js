// ===== AI Academy — Progress & UI Logic =====

(function() {
  'use strict';

  const STORAGE_KEY = 'ai-academy-progress';
  const TOTAL_LESSONS = 30;

  // Stage lesson counts for counters
  const STAGES = {
    1: { lessons: ['0-0-setup','1-1-terminal','1-2-files','1-3-variables','1-4-conditions','1-5-functions','1-6-working-files','1-7-git'], total: 8 },
    2: { lessons: ['2-1-llm','2-2-api','2-3-first-api','2-4-prompts','2-5-tokens','2-6-scripts'], total: 6 },
    3: { lessons: ['3-1-chatbot-vs-agent','3-2-tools','3-3-memory','3-4-agent-sdk','3-5-multi-step'], total: 5 },
    4: { lessons: ['4-1-telegram','4-2-databases','4-3-deploy','4-4-platforms','4-5-security'], total: 5 },
    5: { lessons: ['5-1-rag','5-2-multi-agent','5-3-fine-tuning','5-4-optimization','5-5-architecture'], total: 5 }
  };

  // --- Storage ---
  function getProgress() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch(e) {
      return {};
    }
  }

  function saveProgress(progress) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }

  function isCompleted(lessonId) {
    return !!getProgress()[lessonId];
  }

  function markCompleted(lessonId) {
    var progress = getProgress();
    progress[lessonId] = true;
    saveProgress(progress);
  }

  // --- Update UI on index page ---
  function updateIndexPage() {
    var progress = getProgress();
    var completedCount = Object.keys(progress).length;

    // Update progress bar
    var progressText = document.getElementById('progress-text');
    var progressFill = document.getElementById('progress-fill');
    if (progressText) {
      progressText.textContent = completedCount + ' из ' + TOTAL_LESSONS + ' уроков';
    }
    if (progressFill) {
      progressFill.style.width = (completedCount / TOTAL_LESSONS * 100) + '%';
    }

    // Update stage counters
    for (var stageNum in STAGES) {
      var stage = STAGES[stageNum];
      var completed = 0;
      stage.lessons.forEach(function(lessonId) {
        if (progress[lessonId]) completed++;
      });
      var counter = document.querySelector('[data-stage="' + stageNum + '"]');
      if (counter) {
        counter.textContent = completed + '/' + stage.total;
      }
    }

    // Update lesson cards (add checkmark)
    var cards = document.querySelectorAll('.lesson-card');
    cards.forEach(function(card) {
      var lessonId = card.getAttribute('data-lesson');
      if (lessonId && progress[lessonId]) {
        card.classList.add('lesson-card--completed');
        // Add checkmark if not already present
        if (!card.querySelector('.lesson-card__check')) {
          var check = document.createElement('span');
          check.className = 'lesson-card__check';
          check.textContent = '✅';
          card.appendChild(check);
        }
      }
    });
  }

  // --- Lesson page: test logic ---
  function initTest() {
    var testForm = document.getElementById('test-form');
    if (!testForm) return;

    var submitBtn = document.getElementById('test-submit');
    var resultDiv = document.getElementById('test-result');
    var lessonId = testForm.getAttribute('data-lesson');

    // If already completed, show it
    if (isCompleted(lessonId)) {
      resultDiv.innerHTML = '✅ Урок пройден!';
      resultDiv.className = 'test__result test__result--pass';
      resultDiv.style.display = 'block';
    }

    submitBtn.addEventListener('click', function() {
      var questions = testForm.querySelectorAll('.test__question');
      var total = questions.length;
      var correct = 0;

      questions.forEach(function(q) {
        var correctAnswer = q.getAttribute('data-correct');
        var selected = q.querySelector('input[type="radio"]:checked');
        var options = q.querySelectorAll('.test__option');

        // Reset styles
        options.forEach(function(opt) {
          opt.classList.remove('test__option--correct', 'test__option--wrong');
        });

        if (selected) {
          var selectedValue = selected.value;
          if (selectedValue === correctAnswer) {
            correct++;
            selected.closest('.test__option').classList.add('test__option--correct');
          } else {
            selected.closest('.test__option').classList.add('test__option--wrong');
            // Highlight correct answer
            options.forEach(function(opt) {
              var radio = opt.querySelector('input[type="radio"]');
              if (radio && radio.value === correctAnswer) {
                opt.classList.add('test__option--correct');
              }
            });
          }
        }
      });

      var percent = (correct / total) * 100;

      if (percent >= 80) {
        resultDiv.innerHTML = '✅ ' + correct + ' из ' + total + ' правильно — урок пройден!';
        resultDiv.className = 'test__result test__result--pass';
        markCompleted(lessonId);
      } else {
        resultDiv.innerHTML = '❌ ' + correct + ' из ' + total + ' правильно. Нужно ≥80%. Попробуйте ещё раз!';
        resultDiv.className = 'test__result test__result--fail';
      }
      resultDiv.style.display = 'block';
    });
  }

  // --- Copy buttons for code blocks ---
  function initCopyButtons() {
    var codeBlocks = document.querySelectorAll('.lesson-content pre');
    codeBlocks.forEach(function(pre) {
      var wrapper = document.createElement('div');
      wrapper.className = 'code-block';
      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);

      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.textContent = 'Копировать';
      btn.addEventListener('click', function() {
        var code = pre.querySelector('code');
        var text = code ? code.textContent : pre.textContent;
        navigator.clipboard.writeText(text).then(function() {
          btn.textContent = 'Скопировано!';
          setTimeout(function() { btn.textContent = 'Копировать'; }, 1500);
        });
      });
      wrapper.appendChild(btn);
    });
  }

  // --- Init ---
  document.addEventListener('DOMContentLoaded', function() {
    // Index page
    if (document.getElementById('progress-fill')) {
      updateIndexPage();
    }

    // Lesson page
    initTest();
    initCopyButtons();
  });

  // Register Service Worker
  window.addEventListener('load', () => {
    if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) {
      navigator.serviceWorker.register('/sw.js')
        .then(registration => {
          console.log('Service Worker registered:', registration);
        })
        .catch(error => {
          console.error('Service Worker registration failed:', error);
        });
    }
  });

})();
