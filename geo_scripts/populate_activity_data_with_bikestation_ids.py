import csv
import json


def main():
    bikestation_zone_list = json.load(open("./bikestation_to_zone_mapping.json", "r"))
    mapping = {str(b["zone_id"]): b for b in bikestation_zone_list}

    rows = [["dominant_zone", "time", "count", "station_id", "station_name"]]

    with open(
        "/home/aleksi/Documents/junction2018/Uusimaa_activity_data_hourly_20_min_break_MTC_201806.txt",
        "r",
    ) as csvinput:
        reader = csv.reader(csvinput, delimiter=",")
        next(reader)
        for row in reader:
            if not row[0] in mapping:
                continue
            zone = mapping[row[0]]
            rows.append(row + [zone["station_id"], zone["station_name"]])

    with open(
        "Uusimaa_activity_data_hourly_20_min_break_with_bikestations_MTC_201806.txt",
        "w",
    ) as csvoutput:
        writer = csv.writer(csvoutput, lineterminator="\n", delimiter=",")
        writer.writerows(rows)

