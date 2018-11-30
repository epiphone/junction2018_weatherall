def is_point_in_grid(point, grid_corners):
    """
    Return True when `point` is inside a rectangle defined by `grid_corners`.

    >>> sample_grid_coords = [
        # longitude          latitude
        [24.887117874985439, 60.235394405060028], # top left
        [24.896140153753443, 60.235537781506437], # top right
        [24.896427824393964, 60.231051336794344], # bottom right
        [24.887406777052096, 60.230907986265876], # bottom left
        [24.887117874985439, 60.235394405060028], # top left again, ignored!
    ]
    >>> is_point_in_grid([24.89056, 60.23351], sample_grid_coords)
    True
    """
    top_left, top_right, bottom_right, bottom_left = (
        grid_corners[0],
        grid_corners[1],
        grid_corners[2],
        grid_corners[3],
    )
    max_lat = max(top_left[1], top_right[1])
    min_lat = min(bottom_right[1], bottom_left[1])
    max_lon = max(top_right[0], bottom_right[0])
    min_lon = min(top_left[0], bottom_left[0])

    lon, lat = point[0], point[1]
    return (min_lon <= lon <= max_lon) and (min_lat <= lat <= max_lat)
