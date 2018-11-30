import requests

ROOT_URL = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"
STATIONS_QUERY = "{ bikeRentalStations { id stationId name bikesAvailable spacesAvailable lat lon } }"


def list_stations():
    res = requests.post(ROOT_URL, json={"query": STATIONS_QUERY})
    return res.json()["data"]["bikeRentalStations"]
