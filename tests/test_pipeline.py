# import main
import main
import pandas as pd
from datetime import datetime
import secrets

from requests.auth import HTTPBasicAuth

# testing csv_file_data.py file
def test_format():

    # what if looks as we expect
    # actual
    mock_data1 = {
        "Actual Or Estimated": "Actual",
        "Usage Cost Total": 0,
        "Read Start Date": datetime.strptime(
            "2017-12-09 00:00:00", "%Y-%m-%d %H:%M:%S"
        ),
        "Read End Date": datetime.strptime("2017-12-09 00:00:00", "%Y-%m-%d %H:%M:%S"),
        "Usage (CCF)": 0,
    }
    mock1 = pd.Series(mock_data1)
    expected_result1 = """
        <meterConsumption estimatedValue="true">
                <cost>0</cost>
                <startDate>2017-12-09</startDate>
                <endDate>2017-12-09</endDate>
                <usage>0</usage>
        </meterConsumption>    
    """.replace(
        " ", ""
    )
    # estimate
    mock_data2 = {
        "Actual Or Estimated": "Estimated",
        "Usage Cost Total": 0,
        "Read Start Date": datetime.strptime(
            "2017-12-09 00:00:00", "%Y-%m-%d %H:%M:%S"
        ),
        "Read End Date": datetime.strptime("2017-12-09 00:00:00", "%Y-%m-%d %H:%M:%S"),
        "Usage (CCF)": 0,
    }
    mock2 = pd.Series(mock_data2)
    expected_result2 = """
        <meterConsumption estimatedValue="false">
                <cost>0</cost>
                <startDate>2017-12-09</startDate>
                <endDate>2017-12-09</endDate>
                <usage>0</usage>
        </meterConsumption>    
    """.replace(
        " ", ""
    )

    # what if dates arent formatted as we expect
    mock_data3 = {
        "Actual Or Estimated": "Estimated",
        "Usage Cost Total": 0,
        "Read Start Date": datetime.strptime(
            "12-09-2017 00:00:00", "%m-%d-%Y %H:%M:%S"
        ),
        "Read End Date": datetime.strptime("2017/12/09 00:00:00", "%Y/%m/%d %H:%M:%S"),
        "Usage (CCF)": 0,
    }
    mock3 = pd.Series(mock_data3)
    expected_result3 = """
        <meterConsumption estimatedValue="false">
                <cost>0</cost>
                <startDate>2017-12-09</startDate>
                <endDate>2017-12-09</endDate>
                <usage>0</usage>
        </meterConsumption>    
    """.replace(
        " ", ""
    )

    result1 = main.format(mock1)
    result2 = main.format(mock2)
    result3 = main.format(mock3)

    assert result1 == expected_result1
    assert result2 == expected_result2
    assert result3 == expected_result3

def test_read_data():
    mock_data1 = "tests/test_data.xlsx"
    expected_result1 = {
        100000000: """
        <meterData>

            <meterConsumption estimatedValue="true">
                <cost>100</cost>
                <startDate>2021-01-01</startDate>
                <endDate>2021-02-01</endDate>
                <usage>100</usage>
            </meterConsumption>

        </meterData>  
    """.replace(
            " ", ""
        )
    }
    # check formatting is as expexted
    # we know that format works as expected as it is tested, but think of two variations at least.
    result1 = main.read_data(mock_data1)

    assert result1 == expected_result1

def test_xml_get_account():
    mock_username, mock_password, _, _ = secrets.secrets()
    basic = HTTPBasicAuth(mock_username, mock_password)

    expected_result = "378825"

    result  = main.xml_get_account(basic)

    assert expected_result == result

def test_xml_get_properties():
    mock_username, mock_password, _, _ = secrets.secrets()
    basic = HTTPBasicAuth(mock_username, mock_password)

    expected_result = ["17879994"]

    result  = main.xml_get_properties(378825, basic)

    assert expected_result == result

def test_xml_get_properties_meter():
    mock_username, mock_password, _, _ = secrets.secrets()
    basic = HTTPBasicAuth(mock_username, mock_password)

    expected_result = ["21655430", "21655459", "21655488"]

    result = main.xml_get_properties_meter(17879994, basic)

    assert expected_result == expected_result

def test_xml_get_meter():
    mock_username, mock_password, _, _ = secrets.secrets()
    basic = HTTPBasicAuth(mock_username, mock_password)


    expected_result1 = "Electric Main Meter"
    expected_result2 = "Potable Indoor Meter"
    expected_result3 = "WasteEstimation"


    result1  = main.xml_get_meter(21655430, basic)
    result2  = main.xml_get_meter(21655459, basic)
    result3  = main.xml_get_meter(21655488, basic)

    assert expected_result1 == result1  
    assert expected_result2 == result2 
    assert expected_result3 == result3 

def test_xml_get_meter_consumtion_data():
    mock_username, mock_password, _, _ = secrets.secrets()
    basic = HTTPBasicAuth(mock_username, mock_password)

    result = main.xml_get_meter_consumtion_data(21655430, basic)

    assert type(result) == str