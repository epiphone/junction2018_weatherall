import glob
import json

ROOT = "/home/aleksi/Documents/junction2018"

MONTHS = [
    {"folder": "stations_201809", "days_in_month": 30},
    {"folder": "stations_201810", "days_in_month": 31},
]


def files_per_hour(month, day, hour):
    month_str = str(month).zfill(2)
    day_str = str(day).zfill(2)
    hour_str = str(hour).zfill(2)
    return glob.glob(
        f"{ROOT}/stations_2018{month_str}/stations_2018{month_str}{day_str}T{hour_str}*"
    )


def hour_stats(month, day, hour):
    res = {}
    for f in files_per_hour(month, day, hour):
        try:
            stations = json.load(open(f, "r"))["result"]
            for s in stations:
                key = s["name"]
                if not key in res:
                    res[key] = {
                        "total_slots": s["total_slots"],
                        "free_slots": [],
                        "avl_bikes": [],
                    }
                res[key]["free_slots"].append(s["free_slots"])
                res[key]["avl_bikes"].append(s["avl_bikes"])
        except json.JSONDecodeError:
            print("ERROR: invalid JSON at", f)
            continue
        except KeyError:
            print("ERROR: invalid format at", f)
            continue

    for k, v in res.items():
        res[k]["free_slots"] = sum(res[k]["free_slots"]) // len(res[k]["free_slots"])
        res[k]["avl_bikes"] = sum(res[k]["avl_bikes"]) // len(res[k]["avl_bikes"])

    return [{"name": k, **v} for k, v in res.items()]


def main():
    for month in [9, 10]:
        days_n = 30 if month == 9 else 31
        for day in range(1, days_n + 1):
            for hour in range(0, 24):
                h_stats = hour_stats(month, day, hour)
                out_f_name = f"./citybike_averages/citybikes-2018-{str(month).zfill(2)}-{str(day).zfill(2)}:{str(hour).zfill(2)}.json"
                print("writing", out_f_name, "stations n:", len(h_stats))
                with open(out_f_name, "w") as out_f:
                    json.dump(h_stats, out_f)

