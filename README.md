# ENERGY-STAR-API

## Table of Contents 

* [Overview](#overview)
* [Development](#dev)
    * [Test Environment](#test_env)
    * [Live Environment](#live_env)
    * [Tests](#tests)


## [Overview](#overview)

This project houses the process of automated upload of Excel files to [ENERGY STAR portfolio managager](https://portfoliomanager.energystar.gov). This data will be used for benchmarking building energy usage. ENERY STAR does accept direct CSV upload. However, particular formatting is needed. 

### [Test Environment](#test_env)
Development of this tool must be done in the test environemt. Once testing is done, submit registration request in the Software Development tab under Account Settings in your Portfolio Manager account. More instructions can be found on [ENERGY STAR](https://www.energystar.gov/buildings/resources_audience/service_product_providers/existing_buildings/benchmarking_clients//use_pm_web_services)

The base URL for the test environment is `https://portfoliomanager.energystar.gov/wstest/`. This can be found and changed on line 88 of main.py file.

Documentation for ENERGY STAR test environment can be found on [ENERGY STAR](https://portfoliomanager.energystar.gov/webservices/home/test/api;jsessionid=31B86EFB940286445D37997C8E98016C)

### [Live Environment](#live_env)
Once registration request has been approved in your Portfolio Manager account you are now able to put your tool into production. 
More instructions for this process can be found on [ENERGY STAR](https://www.energystar.gov/buildings/resources_audience/service_product_providers/existing_buildings/benchmarking_clients//use_pm_web_services)

The base URL for the test environment is `https://portfoliomanager.energystar.gov/ws/`. This can be found and changed on line 88 of main.py file.

Documentation for ENERGY STAR live environment can be found on [ENERGY STAR](https://portfoliomanager.energystar.gov/webservices/home/api)

### [Tests](#tests)
Tests can be executed by installing all requirements  and then executing the tests with pytest like so:
```bash
$ pytest
```
To view code coverage execute the following command:
```bash
$ pytest --cov=main tests/
```
If Coverage Gutters are installed to view coverage within the python file, exicute the following command:
```bash
$ pytest tests --cov-report xml:cov.xml --cov main
```