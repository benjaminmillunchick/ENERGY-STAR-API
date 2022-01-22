import pandas as pd


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
    )

    return xml


def read_data(data_file: str):
    """
    Reads excel data and formats it for API post

    Paramiters: path to excel file
    Returns: dictionary - {Meter #: xml meter data} 
    """
    df = pd.read_excel(data_file)
    # delete extra columns
    df = df[df.filter(regex="^(?!Unnamed)").columns]

    # for testing
    df = df.head()

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
        )

        r_dict[meter] = xml

    return r_dict

