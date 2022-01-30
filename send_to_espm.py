from csv_file_data import read_data
import api_calls
import requests


def run(username: str, password: str):

    auth = requests.auth.HTTPBasicAuth(username, password)
    # read excel file and format data into xml
    # {Meter #: xml meter data}
    meter_data_dict = read_data("sample_csv_files/St Marys Student Parish.xlsx")

    # get accountId from jsut unsername and password
    accountId = api_calls.xml_get_account(auth)

    # gets list of propertyIds that each account has
    propertyIds = api_calls.xml_get_properties(accountId, auth)

    for propertyId in propertyIds:
        # get list of all meterIds
        # returns list of meterIds
        meterIds = api_calls.xml_get_properties_meter(propertyId, auth)

        # mathch meterIds with Meter #
        # returns dict with {Meter #: meterId}
        meterId_dict = {}
        for id in meterIds:
            meter_number = api_calls.xml_get_meter(id, auth)
            meterId_dict[meter_number] = id

        # send meter data to correct meterId
        for meter_number in meter_data_dict:
            meter_id = meterId_dict[meter_number]
            api_calls.xml_post_meter_data(meter_id, meter_data_dict[meter_number], auth)
