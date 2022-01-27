from csv_file_data import read_data
import api_calls

# INFORMATION NEEDED TO SEND DATA #
propertyId = "?"
username = "?"
password = "?"


def run():
    # read excel file and format data into xml
    # {Meter #: xml meter data}
    meter_data_dict = read_data("sample_csv_files/St Marys Student Parish.xlsx")

    # get propertyId from jsut unsername and password
    propertyId = api_calls.xml_get_account()

    # get list of all meterIds
    # returns list of meterIds
    meterIds = api_calls.xml_get_properties_meter(propertyId)

    # mathch meterIds with Meter #
    # returns dict with {Meter #: meterId}
    meterId_dict = {}
    for id in meterIds:
        meter_number = api_calls.xml_get_meter(id)
        meterId_dict[meter_number] = id

    # send meter data to correct meterId
    for meter_number in meter_data_dict:
        meter_id = meterId_dict[meter_number]
        api_calls.xml_post_meter_data(meter_id, meter_data_dict[meter_number])
