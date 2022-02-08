# TODO: Test Multimeter
import pandas as pd
import requests
import regex as re
import secrets

# INFORMATION NEEDED TO SEND DATA #
# username = "?"
# password = "?"
username, password, customer_username, customer_password = secrets.secrets()

data = "sample_csv_files/St Marys Student Parish.xlsx"


def format(row):
    """
    Formats pandas df into xml format for ENERGY STAR

    Paramater: row of pandas dataframe
    Returns: formatted xml
    """
    if row["Actual Or Estimated"] == "Actual":
        estimation = "true"
    else:
        estimation = "false"

    cost = row["Usage Cost Total"]

    start_date = row["Read Start Date"].strftime("%Y-%m-%d")
    end_date = row["Read End Date"].strftime("%Y-%m-%d")

    usage = row["Usage (CCF)"]

    xml = """
    <meterConsumption estimatedValue="{}">
            <cost>{}</cost>
            <startDate>{}</startDate>
            <endDate>{}</endDate>
            <usage>{}</usage>
    </meterConsumption>
    """.format(
        estimation, cost, start_date, end_date, usage
    ).replace(
        " ", ""
    )

    return xml


def read_data(excel_file: str):
    """
    Reads excel data and formats it for API post

    Paramiters: path to excel file
    Returns: dictionary - {Meter #: xml meter data} 
    """
    df = pd.read_excel(excel_file)
    # delete extra columns
    df = df[df.filter(regex="^(?!Unnamed)").columns]

    r_dict = {}

    grouped = df.groupby(df["Meter #"])
    meter_num = df["Meter #"].unique()

    for meter in meter_num:
        meter_df = grouped.get_group(meter)

        meter_df["formatted"] = meter_df.apply(format, axis=1)

        data = "\n".join(list(meter_df["formatted"]))

        xml = """
        <meterData>
            {}
        </meterData>
        """.format(
            data
        ).replace(
            " ", ""
        )

        r_dict[meter] = xml

    return r_dict


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
    Returns: meter # for a meterId
    """
    response = requests.get(
        "{}/meter/{}".format(base_url, meter_id), headers=header, auth=authorization,
    )
    code = response.status_code
    assert code == 200

    text = response.text

    meter_number = re.findall(r"(?><name>)(.*)(?><\/name>)", text)[0]

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


def run(data: str, username: str, password: str):

    auth = requests.auth.HTTPBasicAuth(username, password)
    # read excel file and format data into xml
    # {Meter #: xml meter data}
    meter_data_dict = read_data(data)

    # get accountId from jsut unsername and password
    accountId = xml_get_account(auth)

    # gets list of propertyIds that each account has
    propertyIds = xml_get_properties(accountId, auth)

    for propertyId in propertyIds:
        # get list of all meterIds
        # returns list of meterIds
        meterIds = xml_get_properties_meter(propertyId, auth)

        # mathch meterIds with Meter #
        # returns dict with {Meter #: meterId}
        meterId_dict = {}
        for id in meterIds:
            meter_number = xml_get_meter(id, auth)
            meterId_dict[meter_number] = id

        # send meter data to correct meterId
        for meter_number in meter_data_dict:
            meter_id = meterId_dict[meter_number]
            xml_post_meter_data(meter_id, meter_data_dict[meter_number], auth)

