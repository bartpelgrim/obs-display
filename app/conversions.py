from typing import Optional

from app.exception import UnknownWeatherCodeException
from app.language import Language


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


ww_text = {
    0: {'NL': 'Onbewolkt', 'EN': 'No clouds'},
    1: {'NL': 'Afnemende bewolking', 'EN': 'Clouds generally dissolving'},
    2: {'NL': 'Bewolking onveranderd', 'EN': 'State of sky unchanged'},
    3: {'NL': 'Toenemende bewolking', 'EN': 'Clouds generally developing'},
    4: {'NL': 'Heiigheid of rook', 'EN': 'Visibility reduced by smoke'},
    5: {'NL': 'Heiigheid of rook', 'EN': 'Haze'},
    10: {'NL': 'Nevel', 'EN': 'Mist'},
    11: {'NL': 'IJsnaalden', 'EN': 'Ice needles'},
    12: {'NL': 'Onweer op afstand', 'EN': 'Thunderstorm at a distance'},
    18: {'NL': 'Squalls', 'EN': 'Squalls'},
    20: {'NL': 'Mist', 'EN': 'Fog'},
    21: {'NL': 'Neerslag', 'EN': 'Precipitation'},
    22: {'NL': 'Motregen of motsneeuw', 'EN': 'Drizzle or light snow'},
    23: {'NL': 'Regen', 'EN': 'Rain'},
    24: {'NL': 'Sneeuw', 'EN': 'Snow'},
    25: {'NL': 'Onderkoelde (mot)regen', 'EN': 'Freezing rain or drizzle'},
    26: {'NL': 'Onweer', 'EN': 'Thunderstorm'},
    30: {'NL': 'Mist', 'EN': 'Fog'},
    31: {'NL': 'Mistbanken', 'EN': 'Fog patches'},
    32: {'NL': 'Mist, dunner geworden', 'EN': 'Fog is becoming thinner'},
    33: {'NL': 'Mist, onveranderd', 'EN': 'Fog, no change'},
    34: {'NL': 'Mist, dikker geworden', 'EN': 'Fog has become thicker'},
    35: {'NL': 'Mist met aanzetting van ruige rijp', 'EN': 'Fog, depositing rime'},
    40: {'NL': 'Neerslag', 'EN': 'Precipitation'},
    41: {'NL': 'Neerslag, licht of middelmatig', 'EN': 'Light to moderate precipitation'},
    42: {'NL': 'Neerslag, zwaar', 'EN': 'Heavy precipitation'},
    50: {'NL': 'Motregen', 'EN': 'Drizzle'},
    51: {'NL': 'Lichte motregen', 'EN': 'Light drizzle'},
    52: {'NL': 'Matige motregen', 'EN': 'Moderate drizzle'},
    53: {'NL': 'Dichte motregen', 'EN': 'Heavy drizzle'},
    54: {'NL': 'Lichte ONDERKOELDE motregen', 'EN': 'Light FREEZING drizzle'},
    55: {'NL': 'Matige ONDERKOELDE motregen', 'EN': 'Moderate FREEZING drizzle'},
    56: {'NL': 'Dichte ONDERKOELDE motregen', 'EN': 'Heavy FREEZING drizzle'},
    57: {'NL': 'Lichte motregen en regen', 'EN': 'Light rain and drizzle'},
    58: {'NL': 'Matige of zware motregen en regen', 'EN': 'Moderate or heavy rain and drizzle'},
    60: {'NL': 'Regen', 'EN': 'Rain'},
    61: {'NL': 'Lichte regen', 'EN': 'Light rain'},
    62: {'NL': 'Matige regen', 'EN': 'Moderate rain'},
    63: {'NL': 'Zware regen', 'EN': 'Heavy rain'},
    64: {'NL': 'Lichte ONDERKOELDE regen', 'EN': 'Light FREEZING rain'},
    65: {'NL': 'Matige ONDERKOELDE regen', 'EN': 'Moderate FREEZING rain'},
    66: {'NL': 'Zware ONDERKOELDE regen', 'EN': 'Heavy FREEZING rain'},
    67: {'NL': 'Lichte regen of motregen en sneeuw', 'EN': 'Light mix of snow and rain or drizzle'},
    68: {'NL': 'Matige of zware regen of motregen en sneeuw', 'EN': 'Moderate or heavy mix of snow and rain or drizzle'},
    70: {'NL': 'Sneeuw', 'EN': 'Snow'},
    71: {'NL': 'Lichte sneeuwval', 'EN': 'Snow, slight'},
    72: {'NL': 'Matige sneeuwval', 'EN': 'Snow, moderate'},
    73: {'NL': 'Zware sneeuwval', 'EN': 'Snow, heavy'},
    74: {'NL': 'Lichte ijsregen', 'EN': 'Ice pellets, slight'},
    75: {'NL': 'Matige ijsregen', 'EN': 'Ice pellets, moderate'},
    76: {'NL': 'Zware ijsregen', 'EN': 'Ice pellets, heavy'},
    77: {'NL': 'Motsneeuw', 'EN': 'Granular snow'},
    78: {'NL': 'IJskristallen', 'EN': 'Ice crystals'},
    80: {'NL': 'Bui of onderbroken regen', 'EN': 'Shower or intermittent rain'},
    81: {'NL': 'Lichte regenbui', 'EN': 'Rain shower, slight'},
    82: {'NL': 'Matige regenbui', 'EN': 'Rain shower, moderate'},
    83: {'NL': 'Zware regenbui', 'EN': 'Rain shower, heavy'},
    84: {'NL': 'Wolkbreuk', 'EN': 'Rain shower, very heavy'},
    85: {'NL': 'Lichte sneeuwbui', 'EN': 'Snow shower, slight'},
    86: {'NL': 'Matige sneeuwbui', 'EN': 'Snow shower, moderate'},
    87: {'NL': 'Zware sneeuwbui', 'EN': 'Snow shower, heavy'},
    89: {'NL': 'Hagelbui', 'EN': 'Hail shower'},
    90: {'NL': 'Onweer', 'EN': 'Thunderstorm'},
    91: {'NL': 'Onweer zonder neerslag', 'EN': 'Thunderstorm without precipitation'},
    92: {'NL': 'Onweer met regen of sneeuw', 'EN': 'Thunderstorm with rain or snow'},
    93: {'NL': 'Onweer met hagel', 'EN': 'Thunderstorm with hail'},
    94: {'NL': 'Zwaar onweer zonder neerslag', 'EN': 'Heavy thunderstorm without precipitation'},
    95: {'NL': 'Zwaar onweer met regen of sneeuw', 'EN': 'Heavy thunderstorm with rain or snow'},
    96: {'NL': 'Zwaar onweer met hagel', 'EN': 'Heavy thunderstorm with hail'},
    99: {'NL': 'Tornado', 'EN': 'Tornado'},
}


def weather_code_to_text(ww: int, language: Language) -> str:
    if text := ww_text.get(ww):
        return text[language.value]
    raise UnknownWeatherCodeException(f'Unknown weather code: {ww}')
