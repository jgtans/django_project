┌──────────── Браузер ────────────┐
│  http://127.0.0.1:8080/...      │
└──────────────┬─────────────────┘
               ▼
      seatplan/urls.py  ← «диспетчер»: сверяет адрес СО ВЕРХУ ВНИЗ
   ├─ /admin/…     → админка (CRUD через формы → срабатывает clean())
   ├─ /ckeditor5/… → CKEditor 5 (WYSIWYG)
   ├─ /media/…     → отдача медиа-файлов (только в dev, DEBUG=True)
   └─ /__debug__/  → debug_toolbar (панель SQL-запросов)
   ✗ ВСЁ. Публичных страниц сайта НЕТ — «парадной двери» ещё не построили.

      PostgreSQL · seatplan_db
   ├─ workspaces_workspace
   ├─ employees_employee ──FK──▶ workspaces (role, hired_at…)
   ├─ employees_skill · employees_employeeskill (level 1–10)
   └─ employees_employeephoto (order, image)

      Фоновая логика:
   ├─ employees/signals.py → post_delete: файл фото удаляется с диска
   └─ employees/tests.py   → 6 тестов правила соседства


