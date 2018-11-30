import csv


def unique_grid_ids():
    grid_ids = set()
    with open(
        "/home/aleksi/Documents/junction2018/Uusimaa_activity_data_hourly_20_min_break_MTC_201805.txt",
        "r",
    ) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            grid_ids.add(row[0])
        return list(grid_ids)
