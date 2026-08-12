django_project/
├── manage.py
├── requirements.txt
├── .gitignore
├── db.sqlite3 (или PostgreSQL)
├── seatplan/ # основной пакет проекта
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
├── workspaces/ # приложение «Рабочие места»
│ ├── models.py
│ ├── admin.py
│ ├── migrations/
│ └── ...
├── employees/ # приложение «Сотрудники»
│ ├── models.py
│ ├── admin.py
│ ├── signals.py # пост-удаление фото
│ ├── tests.py # 6 тестов
│ ├── migrations/
│ └── ...
└── media/ # пользовательские загрузки (в dev)
