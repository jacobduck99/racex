
from services.utils import convert_to_kph

def test_convert_to_kph():
    assert convert_to_kph(10) == 36
