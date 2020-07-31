import math
from math import pow, cos, asin, sin


class CaculateDistance:
    EARTH_RADIUS = 6378.137

    @staticmethod
    def _rad(d: float):
        return d * math.pi / 180.0

    @staticmethod
    def getDistance(lat1: float, lng1: float, lat2: float, lng2: float):
        radLat1 = CaculateDistance._rad(lat1)
        radLat2 = CaculateDistance._rad(lat2)
        a = radLat1 - radLat2
        b = CaculateDistance._rad(lng1) - CaculateDistance._rad(lng2)
        s = 2 * asin(math.sqrt(
            pow(math.sin(a / 2), 2) + cos(radLat1) * cos(radLat2) * pow(math.sin(b / 2), 2)))
        s = s * CaculateDistance.EARTH_RADIUS
        s = (s * 10000) / 10
        return s


if __name__ == '__main__':
    distance = CaculateDistance.getDistance(28.6756122, 121.3628220, 30.2261922, 120.0317733)
    print(distance)
