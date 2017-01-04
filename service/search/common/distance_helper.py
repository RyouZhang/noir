import math


__all__ = (
    'generate_geo_box',
    'convert_mi_to_km',
    'convert_km_to_mi',
)


def generate_geo_box(lat, lon, distance, is_km=False):
    if not is_km:
        distance = convert_mi_to_km(distance)
    
    distance = distance * 1.414

    lt_lat, lt_lon = _calculate_poi(lat, lon, distance, 315.0)
    rb_lat, rb_lon = _calculate_poi(lat, lon, 135.0)

    return (lt_lat, lt_lon), (rb_lat, rb_lon)


EARTH_R = 6378.1

def _calculate_poi(lat, lon, distance, angle=90):
    r = math.radians(angle)

    r_lat = math.radians(lat)
    r_lon = math.radians(lon)

    alpha = distance / EARTH_R
    
    sin_r = math.sin(r)
    cos_r = math.cos(r)

    sin_lat = math.sin(r_lat)
    cos_lat = math.cos(r_lat)

    sin_alpha = math.sin(alpha)
    cos_alpha = math.cos(alpha)


    res_lat = math.asin(sin_lat * cos_alpha + cos_lat * sin_alpha * cos_r)
    res_lon = r_lon + math.atan2(sin_r * sin_alpha * cos_lat, cos_alpha - sin_lat * math.sin(res_lat))

    return math.degrees(res_lat), math.degrees(res_lon)

def convert_mi_to_km(mi):
    return mi / 0.62137

def convert_km_to_mi(km):
    return 0.62137 * km