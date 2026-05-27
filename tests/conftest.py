import json
import os
from collections.abc import Iterator

import allure
import pytest
import requests


def attach_json(name: str, payload: object) -> None:
    allure.attach(
        json.dumps(payload, ensure_ascii=False, indent=2),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("TEST_API_BASE_URL", "http://127.0.0.1:8080").rstrip("/")


@pytest.fixture(scope="session")
def student_email() -> str:
    value = os.getenv("TEST_STUDENT_EMAIL", "").strip()
    if not value:
        pytest.fail("TEST_STUDENT_EMAIL is required")
    return value


@pytest.fixture(scope="session")
def student_password() -> str:
    value = os.getenv("TEST_STUDENT_PASSWORD", "").strip()
    if not value:
        pytest.fail("TEST_STUDENT_PASSWORD is required")
    return value


@pytest.fixture(scope="session")
def access_token(base_url: str, student_email: str, student_password: str) -> str:
    payload = {
        "email": student_email,
        "password": student_password,
    }

    with allure.step("Login as student and receive access token"):
        response = requests.post(
            f"{base_url}/auth/login",
            json=payload,
            timeout=20,
        )
        try:
            attach_json("login-response", response.json())
        except ValueError:
            allure.attach(
                response.text,
                name="login-response-text",
                attachment_type=allure.attachment_type.TEXT,
            )

    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture()
def api_client(base_url: str, access_token: str) -> Iterator[requests.Session]:
    with requests.Session() as session:
        session.base_url = base_url
        session.headers.update(
            {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
        )
        yield session
