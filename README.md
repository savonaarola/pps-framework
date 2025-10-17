# Python Pytest Selenium testing framework

## Generate allure reports

allure serve reports/allure-results


## Create Docker image
docker build -t pps-tests-01 .

## Launch Docker container
docker run --rm -v ${PWD}\reports\allure-results:/tests/reports/allure-results pps-tests-01

## Generate allure reports
allure serve reports/allure-results