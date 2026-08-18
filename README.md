# Django Project «Seatplan»
## 🔧 Установка и запуск

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/jgtans/django_project.git
   cd django_project

---

2. Создать и активировать виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate      # Linux/macOS
    venv\Scripts\activate         # Windows

---

3. Установить зависимости:
    ```bash
    Копировать
    Скачать
    pip install -r requirements.txt

---
   
4. Применить миграции:
    ```bash
    python manage.py migrate

---
   
5. Запустить сервер разработки:
    ```bash
    python manage.py runserver 8080

---
   
6. Открыть в браузере: http://127.0.0.1:8080


---
## Порядок запуска (Docker)
1. `docker compose up -d --build` — поднимает PostgreSQL и Django, миграции выполняются автоматически.
2. `docker compose exec web python manage.py createsuperuser` — создать администратора.
3. Адреса: сайт http://localhost:8000, API http://localhost:8000/api/v1/employees/, Swagger http://localhost:8000/swagger/.
4. Роли: в админке назначь пользователю группу `watchers` (смотритель) или `admins` (администратор).
5. Остановка: `docker compose down` (данные БД сохраняются в томе pgdata).