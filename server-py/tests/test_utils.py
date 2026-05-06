import pytest
from services.utils import convert_to_kph, convert_to_meters

def test_convert_to_kph():
    assert convert_to_kph(10) == 36

def test_convert_to_meteres():
    assert convert_to_meters(6143, 0.000487) == pytest.approx(2.9916, abs=0.001)
