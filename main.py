# TODO: get meter_id associated with meter name ***Dont thik this will be possible***
# TODO: Test Multimeter

import secrets
import send_to_espm
import secrets

# INFORMATION NEEDED TO SEND DATA #
# username = "?"
# password = "?"
username, password, customer_username, customer_password = secrets()

data = "sample_csv_files/St Marys Student Parish.xlsx"

# send data to energy star
send_to_espm.run(data, username, password)

