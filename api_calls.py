# file used to house secrests locally before I fiugre out how to do that for real
from secrets import secrets
import requests
import regex as re

# initialize basic authentication
username, password, customer_username, customer_password = secrets()

accountId = 378825
customer_accountId = 378826
propertyId = 17879994
propertyUseId = 11362107
energy_meterId = 21655430
water_meterId = 21655459
waist_meterId = 21655488

# test URL
base_url = "https://portfoliomanager.energystar.gov/wstest/"
# production URL
# base_url = "https://portfoliomanager.energystar.gov/ws/"

header = {"Content-Type": "application/xml"}


def xml_get_account(authorization):
    """
    This web service retrieves your account information that includes your username, password, and contact information.

    Parameters: basic authorization
    Returns: accountId
    """
    response = requests.get(
        "{}account".format(base_url), headers=header, auth=authorization,
    )
    assert response.status_code == 200

    text = response.text

    accountId = re.findall(r"(?><id>)(.*)(?><\/id>)", text)[0]

    return accountId


def xml_get_properties(accountId: int, authorization):
    """
    This web service creates a property for a specific Portfolio Manager user based on the information 
    provided in the XML request and establishes all of the necessary sharing permissions between you 
    and the Portfolio Manager user. It returns the unique identifier to the newly created property and 
    a link to the corresponding web service to retrieve it.

    Parameters: accountId, basic authorization
    Returns: list of propertyIds
    """
    response = requests.get(
        "{}account/{}/property/list".format(base_url, accountId),
        headers=header,
        auth=authorization,
    )
    assert response.status_code == 200

    text = response.text

    propertieIds = re.findall(r'(?>id=")(\d*)(?>")', text)

    return propertieIds


def xml_get_properties_meter(property_id: int, authorization):
    """
    This web service returns a list of meters that are associated to a specific property.

    Paramater: property_id, basic authorization
    Returns: list of meterIds associated with a property
    """
    response = requests.get(
        "{}/association/property/{}/meter".format(base_url, property_id),
        headers=header,
        auth=authorization,
    )
    assert response.status_code == 200

    text = response.text

    meterIds = re.findall(r"(?><meterId>)(.*)(?><\/meterId>)", text)

    return meterIds


def xml_get_meter(meter_id: int, authorization):
    """
    This web service retrieves information for a specific meter. The meter must already be shared with you.

    Paramater: meter_id, basic authorization
    ReturnsL meter # for a meterId
    """
    response = requests.get(
        "{}/meter/{}".format(base_url, meter_id), headers=header, auth=authorization,
    )
    code = response.status_code
    assert code == 200

    text = response.text

    meter_number = re.finall(r"(?><name>)(.*)(?><\/name>)", text)[0]

    return meter_number


def xml_get_meter_consumtion_data(meter_id: int, authorization):
    """
    Returns the consumption data for a specified meter in sets of 120. The meter must already be shared with you.

    Paramater: meter_id, basic authorization
    Returns: consumption data for a specified meter
    """
    response = requests.get(
        "{}/meter/{}/consumptionData".format(base_url, meter_id),
        headers=header,
        auth=authorization,
    )
    assert response.status_code == 200
    return response.text


def xml_post_meter_data(meter_id: int, meter_data: str, authorization):
    """
    Adds consumption data, optional green power, and optional demand data to a specified meter. 
    The property that the meter belongs to must already be shared with you and you must have write access to the meter.

    Paramaters: meter_id, meter_data, basic authorization
    Returns: None
    """
    response = requests.post(
        "{}/meter/{}/consumptionData".format(base_url, meter_id),
        headers=header,
        auth=authorization,
        data=meter_data,
    )
    assert response.status_code == 201
