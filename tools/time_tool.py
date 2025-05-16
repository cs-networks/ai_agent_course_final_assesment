# tools/time_tool.py
from datetime import datetime
from langchain.agents import Tool
from pytz import timezone as pytz_timezone, UnknownTimeZoneError


def get_current_time(timezone: str = "UTC") -> str:
    """
    Gibt die aktuelle Zeit in UTC zurück.
    Args:
        timezone (str): Zeitzone, in der die Zeit zurückgegeben werden soll. Standardmäßig UTC.
    Returns:
        str: Aktuelle Zeit in ISO 8601-Format.
    """
    current_time = datetime.now().astimezone().isoformat()

    #Remove ' from the timezone string
    timezone = timezone.replace("'", "")

    if timezone != "UTC":
        # Hier könnte eine Umrechnung in die angegebene Zeitzone erfolgen
        # Für den Moment geben wir einfach die aktuelle Zeit zurück
        try:
            tz = pytz_timezone(timezone)
            # Aktuelle Zeit in der angegebenen Zeitzone
            current_time = datetime.now(tz).isoformat()
        except UnknownTimeZoneError:
            return f"Unbekannte Zeitzone: {timezone}. Bitte geben Sie eine gültige Zeitzone an."
    return f"Aktuelle Zeit in {timezone}: {current_time}"


time_tool = Tool(
    name="current_time",
    func=get_current_time,
    description="Gibt die aktuelle UTC-Zeit zurück. Optional: Geben Sie eine andere Zeitzone an, um die Zeit in dieser Zeitzone zu erhalten."
)