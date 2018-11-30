from influxdb import InfluxDBClient

WXT536_BASE_NAME = "urn:dev:vaisala:WXT530:P3110408_"

client = InfluxDBClient(
    host="ws-hackjunction2018.vaisala-testbed.net",
    username="hackjunction2018",
    password="hj2018readonly",
    database="hackjunction2018",
    ssl=True,
)


def get_latest_reading():
    """
    Return the latest set of readings from Vaisala device DB.
    Check return value codes at https://ws-hackjunction2018.vaisala-testbed.net/
    """
    query_str = "select * from senml WHERE bn ='{}' ORDER BY time DESC LIMIT 1".format(
        WXT536_BASE_NAME
    )
    raw_reading = next(client.query(query_str).get_points())
    return raw_reading
