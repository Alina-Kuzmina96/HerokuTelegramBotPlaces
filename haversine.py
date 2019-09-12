from math import pi,sqrt,sin,cos,atan2

def haversine(lat1, lon1, lat2, lon2):
    lat1 = float(lat1)
    long1 = float(lon1)
    lat2 = float(lat2)
    long2 = float(lon2)

    degree_to_rad = float(pi / 180.0)

    d_lat = (lat2 - lat1) * degree_to_rad
    d_long = (long2 - long1) * degree_to_rad

    a = pow(sin(d_lat / 2), 2) + cos(lat1 * degree_to_rad) * cos(lat2 * degree_to_rad) * pow(sin(d_long / 2), 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    km = 6367 * c

    return km
