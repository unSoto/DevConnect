import sqlite3
from contextlib import closing

DB_PATH = "devconnect.db"

# Инициализация базы данных

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS resumes (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT,
                    specialization TEXT,
                    experience TEXT,
                    skills TEXT,
                    contacts TEXT
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS vacancies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    company_name TEXT,
                    position TEXT,
                    requirements TEXT,
                    conditions TEXT,
                    contacts TEXT
                )
            ''')

# CRUD для резюме

def get_resume(user_id):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM resumes WHERE user_id=?", (user_id,))
        return cur.fetchone()

def create_resume(user_id, name, specialization, experience, skills, contacts):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("REPLACE INTO resumes (user_id, name, specialization, experience, skills, contacts) VALUES (?, ?, ?, ?, ?, ?)",
                         (user_id, name, specialization, experience, skills, contacts))

def delete_resume(user_id):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("DELETE FROM resumes WHERE user_id=?", (user_id,))

def update_resume(user_id, name, specialization, experience, skills, contacts):
    create_resume(user_id, name, specialization, experience, skills, contacts)

# CRUD для вакансий

def get_vacancy_by_user(user_id):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vacancies WHERE user_id=?", (user_id,))
        return cur.fetchone()

def create_vacancy(user_id, company_name, position, requirements, conditions, contacts):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("REPLACE INTO vacancies (user_id, company_name, position, requirements, conditions, contacts) VALUES (?, ?, ?, ?, ?, ?)",
                         (user_id, company_name, position, requirements, conditions, contacts))

def delete_vacancy(user_id):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("DELETE FROM vacancies WHERE user_id=?", (user_id,))

def update_vacancy(user_id, company_name, position, requirements, conditions, contacts):
    create_vacancy(user_id, company_name, position, requirements, conditions, contacts)

# Получение вакансий с пагинацией

def get_vacancies(offset=0, limit=5):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vacancies ORDER BY RANDOM() LIMIT ? OFFSET ?", (limit, offset))
        return cur.fetchall()

# Получение резюме с пагинацией (исключая пользователя)

def get_resumes_excluding_user(user_id, offset=0, limit=5):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM resumes WHERE user_id != ? ORDER BY RANDOM() LIMIT ? OFFSET ?", (user_id, limit, offset))
        return cur.fetchall()

# Функция для заполнения тестовыми данными

def populate_test_data():
    """Заполняет базу данных тестовыми резюме и вакансиями"""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            # Тестовые резюме (10 штук)
            test_resumes = [
                (1, "Иван Иванов", "Python Developer", "3 года", "Python, Django, PostgreSQL", "+7 (999) 111-11-11"),
                (2, "Мария Петрова", "Frontend Developer", "2 года", "React, JavaScript, CSS", "+7 (999) 222-22-22"),
                (3, "Алексей Сидоров", "Data Scientist", "4 года", "Python, ML, SQL", "+7 (999) 333-33-33"),
                (4, "Елена Козлова", "UX/UI Designer", "3 года", "Figma, Photoshop, Prototyping", "+7 (999) 444-44-44"),
                (5, "Дмитрий Новиков", "DevOps Engineer", "5 лет", "Docker, Kubernetes, AWS", "+7 (999) 555-55-55"),
                (6, "Ольга Морозова", "Full Stack Developer", "4 года", "Node.js, React, MongoDB", "+7 (999) 666-66-66"),
                (7, "Сергей Волков", "Mobile Developer", "3 года", "Flutter, Dart, Firebase", "+7 (999) 777-77-77"),
                (8, "Анна Соколова", "QA Engineer", "2 года", "Selenium, Postman, JIRA", "+7 (999) 888-88-88"),
                (9, "Максим Орлов", "System Administrator", "6 лет", "Linux, Windows Server, Active Directory", "+7 (999) 999-99-99"),
                (10, "Татьяна Лебедева", "Product Manager", "3 года", "Agile, Scrum, Analytics", "+7 (999) 000-00-00")
            ]

            # Тестовые вакансии (10 штук)
            test_vacancies = [
                (11, "Яндекс", "Senior Python Developer", "Опыт работы с Python 3+ года, знание Django/FastAPI", "Зарплата 200k-300k, удаленка, ДМС", "hr@yandex.ru"),
                (12, "Сбербанк", "Frontend Developer", "React/Vue.js, опыт 2+ года, TypeScript", "Зарплата 150k-250k, офис в центре", "frontend@sber.ru"),
                (13, "Mail.ru Group", "Data Scientist", "Python, ML фреймворки, опыт работы с большими данными", "Зарплата 250k-400k, гибкий график", "ds@mail.ru"),
                (14, "Ozon", "UX/UI Designer", "Figma, опыт работы 2+ года, портфолио", "Зарплата 120k-200k, удаленка возможна", "design@ozon.ru"),
                (15, "Avito", "DevOps Engineer", "Docker, K8s, опыт работы с облачными сервисами", "Зарплата 180k-280k, офис/удаленка", "devops@avito.ru"),
                (16, "Tinkoff", "Full Stack Developer", "Node.js/React, опыт 3+ года", "Зарплата 200k-350k, современный офис", "jobs@tinkoff.ru"),
                (17, "Kaspersky", "Mobile Developer", "Flutter/React Native, опыт 2+ года", "Зарплата 150k-250k, ДМС, спортзал", "mobile@kaspersky.ru"),
                (18, "2GIS", "QA Automation Engineer", "Python/Java, Selenium, API testing", "Зарплата 130k-220k, гибкий график", "qa@2gis.ru"),
                (19, "Selectel", "System Administrator", "Linux, опыт администрирования серверов", "Зарплата 100k-180k, вахта/удаленка", "sysadmin@selectel.ru"),
                (20, "Skyeng", "Product Manager", "Опыт управления продуктами, аналитика", "Зарплата 150k-250k, удаленка", "pm@skyeng.ru")
            ]

            # Очищаем существующие данные
            conn.execute("DELETE FROM resumes")
            conn.execute("DELETE FROM vacancies")

            # Вставляем тестовые резюме
            conn.executemany(
                "INSERT INTO resumes (user_id, name, specialization, experience, skills, contacts) VALUES (?, ?, ?, ?, ?, ?)",
                test_resumes
            )

            # Вставляем тестовые вакансии
            conn.executemany(
                "INSERT INTO vacancies (user_id, company_name, position, requirements, conditions, contacts) VALUES (?, ?, ?, ?, ?, ?)",
                test_vacancies
            )

            print(f"Добавлено {len(test_resumes)} резюме и {len(test_vacancies)} вакансий")
