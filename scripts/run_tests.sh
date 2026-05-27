#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
. .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

if [ -z "${TEST_STUDENT_EMAIL:-}" ]; then
  echo "[ERROR] TEST_STUDENT_EMAIL is required"
  exit 1
fi

if [ -z "${TEST_STUDENT_PASSWORD:-}" ]; then
  echo "[ERROR] TEST_STUDENT_PASSWORD is required"
  exit 1
fi

pytest -q --alluredir=allure-results
