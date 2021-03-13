from typing import Union, Optional


def mps_to_bft(wind_speed: float) -> Optional[int]:
    if wind_speed is None:
        return None
    elif wind_speed < 0.2:
        return 0
    elif wind_speed < 1.5:
        return 1
    elif wind_speed < 3.3:
        return 2
    elif wind_speed < 5.4:
        return 3
    elif wind_speed < 7.9:
        return 4
    elif wind_speed < 10.7:
        return 5
    elif wind_speed < 13.8:
        return 6
    elif wind_speed < 17.1:
        return 7
    elif wind_speed < 20.7:
        return 8
    elif wind_speed < 24.4:
        return 9
    elif wind_speed < 28.4:
        return 10
    elif wind_speed < 32.6:
        return 11
    else:
        return 12


def mps_to_kph(speed: float) -> Optional[int]:
    if speed is None:
        return None
    else:
        return round(speed * 3.6)
