import random

from app import MOCK_STATION_STATS


def predict_bike_demand(weather_data):
    """
    Return a mapping of bike station ids to the predicted number of bikes needed,
    e.g.

        >>> weather_data = {
                "temperature": -4.9,
                "precipitation": 0.0,
                "wind_speed": 12
            }
        >>> predict_bike_demand(weather_data)
        {
            '011': 4,
            '012': 0,
            '165': 12,
            # ...
        }
    """
    # TODO: connect to the real deal!
    return {s["extra"]["uid"]: random.randint(0, 11) for s in MOCK_STATION_STATS}
