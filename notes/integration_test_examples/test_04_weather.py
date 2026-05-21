import importlib.util, sys, pathlib
from unittest.mock import MagicMock, call
import pytest

spec = importlib.util.spec_from_file_location(
    "weather",
    pathlib.Path(__file__).parent / "../src/04_esempio_weather.py",
)
weather = importlib.util.module_from_spec(spec)
sys.modules["weather"] = weather
spec.loader.exec_module(weather)

# ============================================================
# STRATEGIA TOP-DOWN : parto da AlertService, stubbando tutto
# ============================================================

class StubWeatherProvider:
    """Stub del provider meteo. Ritorna sempre il forecast che gli dico io."""
    def __init__(self, forecast):
        self._forecast = forecast
        self.calls = []  # ogni chiamata viene registrata (stub 'spia')

    def get_forecast(self, city):
        self.calls.append(city)
        return self._forecast


class StubNotificationSender:
    """Stub del notificatore. Non manda nulla davvero, conta le chiamate."""
    def __init__(self, fake_sent=0):
        self.fake_sent = fake_sent
        self.calls = []

    def notify_city(self, city, subject, body):
        self.calls.append((city, subject, body))
        return self.fake_sent


