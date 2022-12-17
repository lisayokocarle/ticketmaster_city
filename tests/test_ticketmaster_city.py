from ticketmaster_city import ticketmaster_city
import pytest

def test_for_api_get():
    with pytest.raises(TypeError):
        ticketmaster_city.apiget(city='Chicago')
    
def test_for_api_get2():
    with pytest.raises(TypeError):
        ticketmaster_city.apiget()

def test_apiget_with_only_one_value():
    with pytest.raises(TypeError):
        ticketmaster_city.apiget(city="Chicago")

def test_class_city():
    with pytest.raises(ValueError):
        ticketmaster_city.City(cityname = "")

def test_class_city():
    with pytest.raises(ValueError):
        ticketmaster_city.City()