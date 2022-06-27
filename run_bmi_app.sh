#!/bin/bash

echo "Running BMI app"


DEP_FILE=requirements.txt
TEST_FILE=app_test.py
APP=bmi_calc.py
PYTHON=python3

chmod 755 ${TEST_FILE}
chmod 755 ${APP}

echo "Installing dependencies..."
pip install -r ${DEP_FILE}

echo "Running tests..."
run_test() {
    ${PYTHON} ${TEST_FILE} 2>&1 | grep 'OK'
}

if run_test = 'OK'; then
    echo "Running app..."
    ${PYTHON} ${APP}
fi
