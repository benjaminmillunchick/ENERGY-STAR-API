# file used to house secrests locally before I fiugre out how to do that for real
from secrets import secrets

import requests

# initialize basic authentication
username, password, customer_username, customer_password = secrets()

accountId = 378825
customer_accountId = 378826
propertyId = 17879994
propertyUseId = 11362107
energy_meterId = 21655430
water_meterId = 21655459
waist_meterId = 21655488

base_url = "https://portfoliomanager.energystar.gov/wstest/"
header = {"Content-Type": "application/xml"}

basic = requests.auth.HTTPBasicAuth(username, password)


def xml_create_account(
    username: str,
    password: str,
    firstname: str,
    lastname: str,
    adress: str,
    city: str,
    state: str,
    postalcode,
    country: str,
    email: str,
    jobtitle: str,
    phone: int,
    org_name: str,
    primary_buisness: str = "Other",
    other_buisness: str = "other",
):
    response = requests.post(
        "{}account".format(base_url),
        header=header,
        auth=basic,
        data="""
        <account>
            <username>{}</username>
            <password>{}</password>
            <webserviceUser>true</webserviceUser>
            <searchable>true</searchable>
            <billboardMetric>score</billboardMetric>
            <contact>
                <firstName>{}</firstName>
                <lastName>{}</lastName>
                <address address1="{}" city="{}" state="{}" postalCode="{}" country="{}"/>
                <email>{}</email>
                <jobTitle>{}</jobTitle>
                <phone>{}</phone>
            </contact>
            <organization name="{}">
                <primaryBusiness>{}</primaryBusiness>
                <otherBusinessDescription>{}</otherBusinessDescription>
                <energyStarPartner>true</energyStarPartner>
                <energyStarPartnerType>Service and Product Providers</energyStarPartnerType>
            </organization>
        </account>
        """.format(
            username,
            password,
            firstname,
            lastname,
            adress,
            city,
            state,
            postalcode,
            country,
            email,
            jobtitle,
            phone,
            org_name,
            primary_buisness,
            other_buisness,
        ),
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/xml"


def xml_get_properties_meter():
    """
    This web service returns a list of meters that are associated to a specific property.
    """
    response = requests.get(
        "{}/association/property/{}/meter".format(base_url, propertyId),
        headers=header,
        auth=basic,
    )
    assert response.status_code == 200
    return response.text


def xml_get_meter_data():
    """
    This web service retrieves information for a specific meter. The meter must already be shared with you.
    """
    response = requests.get(
        "{}/meter/{}".format(base_url, energy_meterId), headers=header, auth=basic,
    )
    assert response.status_code == 200
    return response.text


print(xml_get_meter_data())
