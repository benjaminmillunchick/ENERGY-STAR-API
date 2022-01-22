# TODO: get meter_id associated with meter name
# TODO: Test Multimeter

import api_calls
from csv_file_data import read_data

meter_data_dict = read_data("sample_csv_files/St Marys Student Parish.xlsx")

for meter_num in meter_data_dict:
    api_calls.xml_post_meter_data(meter_num, meter_data_dict[meter_num])


# print(api_calls.xml_get_meter_consumtion_data(21655430))
