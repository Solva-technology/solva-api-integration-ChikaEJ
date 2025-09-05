import pytest

from app.services.weather_client import API_KEY, get_weather_of_city


@pytest.mark.asyncio
async def test_get_weather_of_city():
    result = await get_weather_of_city("almaty", API_KEY)

    assert "Алматы" in result
    assert isinstance(result, str)
