# ENERGY-STAR-API

## Table of Contents 

* [Overview](#overview)
* [Development](#dev)
    * [Local Environment](#local_env)
    * [Test Environment](#test_env)
    * [Live Environment](#live_env)
    * [Tests](#tests)
    * [Deploy](#deploy)

instructions for how to run this

## [Overview](#overview)

This project houses the process of automated upload of Excel files to [ENERGY STAR portfolio managager](https://portfoliomanager.energystar.gov). This data will be used for benchmarking building energy usage. ENERY STAR does accept direct CSV upload. However, particular formatting is needed. 

## [Development](#dev)

### [Local Environment](#local_env)

The [RESTclient](https://addons.mozilla.org/en-US/firefox/addon/restclient/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=search) Firefox extention is recomended as and API GUI for quick development and testing. Any other one will suffuce.

### [Test Environment](#test_env)
Development of this tool must be done in the test environemt. Once testing is done, submit registration request in the Software Development tab under Account Settings in your Portfolio Manager account. More instructions can be found on [ENERGY STAR](https://www.energystar.gov/buildings/resources_audience/service_product_providers/existing_buildings/benchmarking_clients//use_pm_web_services)

The base URL for the test environment is `https://portfoliomanager.energystar.gov/wstest/`. This can be found and changed on line 88 of main.py file.

To create a test account follow these simple steps using an REST client:
* Select POST for the HTTP Method
* Set the URL to `https://portfoliomanager.energystar.gov/wstest/account`
* Add the following HTTP Header fields and values to the HTTP request:
    * Header Field Name - Content-Type
    * Value - application/xml
* Set the request body to the following XML. The XML conforms to the account.xsd schema, which can be referenced in the [XML Schemas](https://portfoliomanager.energystar.gov/webservices/home/test/api/account/account/post)

```xml
<account>
    <username>  </username>
    <password>  </password>
    <webserviceUser>  </webserviceUser>
    <searchable>  </searchable>
    <contact>
        <firstName>  </firstName>
        <lastName>  </lastName>
        <address address1="123 Main St" city="Edmonton"
        state="AB" postalCode="T5G 2S7" country="CA"/>
        <email>john_doe@acme.com</email>
        <jobTitle>Building Administrator Data Exchange User</jobTitle>
        <phone>703-555-2121</phone>
    </contact>
    <organization name="ACME Corporation">
        <primaryBusiness>Other</primaryBusiness>
        <otherBusinessDescription>other</otherBusinessDescription>
        <energyStarPartner>true</energyStarPartner>
        <energyStarPartnerType>Service and Product Providers</energyStarPartnerType>
    </organization>
</account>
```
Put your test account username and password on lines _____________ of main.py
RUN GET TO SEE ACCOUNT ID AND CHANGE IN TESTS line 114

The information in your test account can be created using the following steps:
__Note:__ if this information isn't exactly what is seen below, tests may not pass.

When you create a property, you will be required to enter basic information, such as a property name and address. This information is submitted via a POST call, may be edited via a PUT call, and may be deleted with a DELETE call. Finally, once property information has been uploaded to Portfolio Manager, it may be accessed via a GET call. Once you run a POST call, the response will indicate that the POST was successful, but there is no user interface to see the values. If you want to see the values, you can run a GET call to query the database. 

For each of the following tasks, in the RESTclient of your choice use your username and password to create basic authentication. 

To create a property use the following call:
``` xml
POST /account/(customer_accountId)/property
Content-Type: application/xml
Authorization: Basic

<property>
    <name>Broadway School</name>
    <primaryFunction>K-12 School</primaryFunction>
    <address address1="123 South St" city="Edmonton"
        state="AB" postalCode="T5G 2S7" country="CA"/>
    <yearBuilt>2000</yearBuilt>
    <constructionStatus>Existing</constructionStatus>
    <grossFloorArea temporary="false" units="Square Feet">
        <value>10000</value>
    </grossFloorArea>
    <occupancyPercentage>80</occupancyPercentage>
    <isFederalProperty>false</isFederalProperty>
    Testing Web Services Page 6
    Web Services
</property>
```

To create an energy meter use the following call:
``` xml
POST /property/(propertyId)/meter
Content-Type: application/xml
Authorization: Basic

<meter>
    <type>Electric</type>
    <name>Electric Main Meter</name>
    <unitOfMeasure>kBtu (thousand Btu)</unitOfMeasure>
    <metered>true</metered>
    <firstBillDate>2010-01-01</firstBillDate>
    <inUse>true</inUse>
</meter>
```

To create energy meter data use the following call:
``` xml
POST /meter/(energy_meterId)/consumptionData
Content-Type: application/xml
Authorization: Basic

<meterData>
    <meterConsumption estimatedValue="true">
        <cost>21</cost>
        <startDate>2018-12-01</startDate>
        <endDate>2018-12-31</endDate>
        <usage>130</usage>
    </meterConsumption>
        <meterConsumption estimatedValue="false">
        <cost>20</cost>
        <startDate>2018-11-01</startDate>
        <endDate>2018-11-30</endDate>
        <usage>120</usage>
    </meterConsumption>
</meterData>
```

The full documentation for ENERGY STAR test environment can be found on [ENERGY STAR](https://portfoliomanager.energystar.gov/webservices/home/test/api;jsessionid=31B86EFB940286445D37997C8E98016C)

### [Live Environment](#live_env)
Once registration request has been approved in your Portfolio Manager account you are now able to put your tool into production. 
More instructions for this process can be found on [ENERGY STAR](https://www.energystar.gov/buildings/resources_audience/service_product_providers/existing_buildings/benchmarking_clients//use_pm_web_services)

The base URL for the test environment is `https://portfoliomanager.energystar.gov/ws/`. This can be found and changed on line 88 of main.py file.

In order to exchange data in Portfolio Manager, users must set up a connection with a web services provider account and then share their properties and/or meters with this account. [This](https://portfoliomanager.energystar.gov/webservices/pdf/Connection_and_Sharing_for_Data_Exchange_en_US.pdf) document outlines how to set up this connection, and share access to properties and meters. 

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

__Note:__ Current code coverage is 53%. Don't know how to write tests for funtions that only POST and GET from an API, but did due dilligence and sanaty checks on them.

__Error codes:__
* 200 - Success.
* 201 - Resource was created.
* 400 - Bad request submitted. An application error code and message is provided.
* 401 - Authentication credentials were missing or were invalid.
* 403 - You are trying to access data that you do not have access to.
* 404 - You are trying to access a resource that does not exist.
* 405 - The HTTP method for this resource is not supported.
* 415 - You did not specify a supported content/media type with your request. * Currently only "application/xml" is supported.
* 500 - An internal server error has occurred. Please try again.
* 502 - Web services are unavailable due to system maintenance. Please try again.

### [Deploy](#deploy)
