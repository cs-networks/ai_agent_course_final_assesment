import pytest
from tools.time_tool import get_current_time
from pytz import all_timezones

# tools/test_time_tool.py

def test_get_current_time_default_timezone():
    """Test the function with the default timezone (UTC)."""
    result = get_current_time()
    assert "Aktuelle Zeit in UTC:" in result# Print the result for debugging
    assert "T" in result  # ISO 8601 format contains 'T'

def test_get_current_time_valid_timezone():
    """Test the function with a valid timezone."""
    timezone = 'Europe/Vienna'
    result = get_current_time(timezone)
    assert f"Aktuelle Zeit in {timezone}:" in result
    assert "T" in result  # ISO 8601 format contains 'T'

def test_get_current_time_invalid_timezone():
    """Test the function with an invalid timezone."""
    invalid_timezone = "Invalid/Timezone"
    result = get_current_time(invalid_timezone)
    assert result == f"Unbekannte Zeitzone: {invalid_timezone}. Bitte geben Sie eine gültige Zeitzone an."

@pytest.mark.parametrize("timezone", ["Asia/Tokyo", "America/New_York", "Australia/Sydney"])
def test_get_current_time_multiple_timezones(timezone):
    """Test the function with multiple valid timezones."""
    result = get_current_time(timezone)
    # Print the result for debugging
    print(f"Testing timezone: {timezone}")
    print(result)
    assert f"Aktuelle Zeit in {timezone}:" in result
    assert "T" in result  # ISO 8601 format contains 'T'

def test_get_current_time_all_timezones():
    """Test the function with all valid timezones from pytz."""
    for timezone in all_timezones[:10]:  # Limit to first 10 timezones for performance
        result = get_current_time(timezone)
        assert f"Aktuelle Zeit in {timezone}:" in result
        assert "T" in result  # ISO 8601 format contains 'T'