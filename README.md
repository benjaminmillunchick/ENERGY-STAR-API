# ENERGY-STAR-API

## Table of Contents 

* [Overview](#overview)
* [Resources](#resources)
* [Tests](#tests)

## [Overview](#overview)

This project houses the process of automated upload of CSV files to [ENERGY STAR portfolio managager](https://portfoliomanager.energystar.gov). This data will be used for benchmarking buildoing energy usage. ENERY STAR does accept direct CSV upload. However, particular formatting is needed. 

- MVP: get excel file, read it and format it, send to energy star.
- Questions: what authentication and identificaitons are needed? Can I pull meterId with just Meter #?

## [Resources](#resources)

Development of this tool must be done in the test environemt. Once testing is done, submit registration request in the Software Development tab under Account Settings in your Portfolio Manager account. More instructions can be found on [ENERGY STAR](https://www.energystar.gov/buildings/resources_audience/service_product_providers/existing_buildings/benchmarking_clients//use_pm_web_services)

[ENERGY STAR API Documentation ENERGY STAR Portfolio Manager Documentation](https://portfoliomanager.energystar.gov/webservices/home)

- Making API calls with XML body linked [here](https://www.ontestautomation.com/writing-tests-for-restful-apis-in-python-using-requests-part-3-working-with-xml/)


## [Tests](#tests)
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