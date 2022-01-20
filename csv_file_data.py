import pandas as pd


def format(row):
    if row["Actual Or Estimated"] == "Actual":
        estimation = "true"
    else:
        estimation = "false"

    cost = row["Usage Cost Total"]

    # needs to go YYYY-MM-DD
    start_date = "Read Start Date"
    end_date = "Read End Date"

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
    df = pd.read_excel(data_file)
    df = df[df.filter(regex="^(?!Unnamed)").columns]

    df = df.head()

    df["formatted"] = df.apply(format, axis=1)

    data = "\n".join(list(df["formatted"]))

    xml = """
    <meterData>
        {}
    </meterData>
    """.format(
        data
    )

    return xml


print(read_data("sample_csv_files/St Marys Student Parish.xlsx"))
