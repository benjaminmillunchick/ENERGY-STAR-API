import requests

# initialize basic authentication
username = ""
password = ""
customer_username = ""
customer_password = ""

accountId = ""
customer_accountId = ""
propertyId = ""
propertyUseId = ""
energy_meterId = ""
water_meterId = ""
waist_meterId = ""

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

