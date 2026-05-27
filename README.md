# easybank-jenkins-example-pipeline

Учебный проект с API-автотестами для урока 51: Jenkins, Jenkinsfile, Pytest и Allure.

Проект используется вместе с open source стендом:

```text
https://github.com/danilfg/bank-test-platform
```

## Что делает проект

Тест проверяет CRUD-сценарий сотрудника в Student API:

```text
POST   /students/employees
GET    /students/employees/{employee_id}
PATCH  /students/employees/{employee_id}
PATCH  /students/employees/{employee_id}/block
PATCH  /students/employees/{employee_id}/unblock
DELETE /students/employees/{employee_id}
```

## Структура

```text
easybank-jenkins-example-pipeline/
├── Jenkinsfile
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
├── scripts/
│   └── run_tests.sh
└── tests/
    ├── conftest.py
    └── test_employee_crud_allure.py
```

## Локальный запуск

Сначала запусти `bank-test-platform` локально.

Пример:

```bash
git clone https://github.com/danilfg/bank-test-platform.git
cd bank-test-platform
make up
make migrate
make seed
```

После запуска API должен быть доступен:

```text
Swagger: http://127.0.0.1:8080/docs
```

Затем в этом репозитории с автотестами укажи переменные окружения:

```bash
export TEST_API_BASE_URL="http://127.0.0.1:8080"
export TEST_STUDENT_EMAIL="student@easyitlab.tech"
export TEST_STUDENT_PASSWORD="student123"
```

Запусти тесты:

```bash
bash scripts/run_tests.sh
```

Или напрямую:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest -q --alluredir=allure-results
```

## Запуск через Jenkins

1. Запушь этот проект в публичный GitHub-репозиторий.
2. Открой Student Cabinet:

```text
http://127.0.0.1:5174/
```

3. Перейди в раздел Jenkins.
4. Укажи GitHub repository URL.
5. Branch: `main`.
6. Jenkinsfile path: `Jenkinsfile`.
7. Нажми `Configure job`.
8. Открой Jenkins:

```text
http://127.0.0.1:8086/
```

9. Выполни `Scan Multibranch Pipeline Now`.
10. Открой branch job `main`.
11. Нажми `Build with Parameters`.
12. Укажи:

```text
TEST_STUDENT_EMAIL
TEST_STUDENT_PASSWORD
TEST_BRANCH=main
```

13. Запусти build.
14. Проверь `Console Output` и `Allure Report`.

## Что смотреть в Allure

В Allure Report должны быть видны:

- название теста;
- feature/story;
- шаги CRUD-сценария;
- request payload;
- response body;
- status code;
- traceback, если тест упал.

## Важно

`allure-results/`, `.venv/`, `.env` и другие локальные файлы не коммитятся в Git.
