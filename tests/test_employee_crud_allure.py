import uuid

import allure
import pytest

from conftest import attach_json


def unique_employee_payload(prefix: str = "jenkins") -> dict:
    suffix = uuid.uuid4().hex[:8]
    return {
        "email": f"{prefix}.{suffix}@easyitlab.tech",
        "full_name": f"Jenkins Employee {suffix}",
        "password": "employee123",
    }


@allure.epic("EasyBank Student API")
@allure.feature("Employees")
@allure.story("Employee CRUD")
@allure.title("Student can create, update, block, unblock and delete employee")
@allure.description(
    "The test creates an employee in the current student's scope, "
    "updates it, blocks and unblocks it, then deletes it."
)
@pytest.mark.employees
@pytest.mark.rest_api
def test_student_can_manage_employee(api_client):
    create_payload = unique_employee_payload()

    with allure.step("Create employee with POST /students/employees"):
        attach_json("create-employee-request", create_payload)
        response = api_client.post(
            f"{api_client.base_url}/students/employees",
            json=create_payload,
            timeout=20,
        )
        attach_json("create-employee-response", response.json())

        assert response.status_code == 200
        created = response.json()
        created_employee_id = created["id"]
        created_employee_uuid = created["uuid"]
        assert created["email"] == create_payload["email"]
        assert created["full_name"] == create_payload["full_name"]

    with allure.step("Read employee with GET /students/employees/{employee_id}"):
        response = api_client.get(
            f"{api_client.base_url}/students/employees/{created_employee_id}",
            timeout=20,
        )
        attach_json("get-employee-response", response.json())

        assert response.status_code == 200
        assert response.json()["id"] == created_employee_id

    with allure.step("Update employee with PATCH /students/employees/{employee_id}"):
        update_payload = {
            "email": create_payload["email"].replace("@", ".updated@"),
            "full_name": "Jenkins Employee Updated",
        }
        attach_json("update-employee-request", update_payload)

        response = api_client.patch(
            f"{api_client.base_url}/students/employees/{created_employee_id}",
            json=update_payload,
            timeout=20,
        )
        attach_json("update-employee-response", response.json())

        assert response.status_code == 200
        assert response.json()["email"] == update_payload["email"]
        assert response.json()["full_name"] == update_payload["full_name"]

    with allure.step("Block employee with PATCH /students/employees/{employee_id}/block"):
        response = api_client.patch(
            f"{api_client.base_url}/students/employees/{created_employee_id}/block",
            timeout=20,
        )
        attach_json("block-employee-response", response.json())

        assert response.status_code == 200
        assert response.json()["is_blocked"] is True
        assert response.json()["is_active"] is False

    with allure.step("Unblock employee with PATCH /students/employees/{employee_id}/unblock"):
        response = api_client.patch(
            f"{api_client.base_url}/students/employees/{created_employee_id}/unblock",
            timeout=20,
        )
        attach_json("unblock-employee-response", response.json())

        assert response.status_code == 200
        assert response.json()["is_blocked"] is False
        assert response.json()["is_active"] is True

    with allure.step("Delete employee with DELETE /students/employees/{employee_id}"):
        response = api_client.delete(
            f"{api_client.base_url}/students/employees/{created_employee_id}",
            timeout=20,
        )
        attach_json("delete-employee-response", response.json())

        assert response.status_code == 200
        assert response.json()["deleted_employee_id"] == created_employee_uuid
