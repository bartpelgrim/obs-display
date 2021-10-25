import pytest

from app.exception import UnknownWeatherCodeException
from app.conversions import ww_text, weather_code_to_text
from app.language import Language


class TestConversions:
    def test_weather_code_to_text_has_values_for_all_languages(self):
        for ww, text in ww_text.items():
            for lang in Language:
                assert text.get(lang.value) is not None

    def test_weather_code_to_text_returns_correct_result_nl(self):
        assert weather_code_to_text(60, Language.NL) == 'Regen'

    def test_weather_code_to_text_returns_correct_result_en(self):
        assert weather_code_to_text(60, Language.EN) == 'Rain'

    def test_weather_code_to_text_raises_exception_with_unknown_code(self):
        with pytest.raises(UnknownWeatherCodeException):
            weather_code_to_text(100, Language.NL)
