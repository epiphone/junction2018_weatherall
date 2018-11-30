import json

from point_in_grid import is_point_in_grid


def main():
    res = []
    stations = json.load(open("../data/citybike-stations-2018-11-24-1316.json", "r"))[
        "stations"
    ]
    zones = json.load(open("./uusimaa_zones.json", "r"))

    for s in stations:
        for z in zones:
            if is_point_in_grid([s["longitude"], s["latitude"]], z["coordinates"]):
                res.append(
                    {
                        "station_id": s["extra"]["uid"],
                        "station_name": s["name"],
                        "zone_id": z["id"],
                    }
                )
                break

    with open("bikestation_to_zone_mapping.json", "w") as out:
        json.dump(res, out)
