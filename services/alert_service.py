# services/alert_service.py

class AlertService:
    def __init__(self, settings):
        self.settings = settings
        self.thresholds = {}
        self.alerts = {}

    def set_threshold(self, threshold: float, city: str):
        # Set the alert threshold for a given city
        self.thresholds[city] = threshold

    def check_alert(self, weather_data):
        # Check the weather data and, if it exceeds the threshold, add an alert.
        city = weather_data.city
        if city in self.thresholds and weather_data.temp > self.thresholds[city]:
            if city not in self.alerts:
                self.alerts[city] = []
            self.alerts[city].append(weather_data)

    def get_daily_summary(self, city: str, weather_data_list: list):
        # Calculate a daily summary (average, min, max temperature) from a list of weather data entries.
        temps = [data.temp for data in weather_data_list if data.city == city]
        if temps:
            return {
                "avg_temp": sum(temps) / len(temps),
                "min_temp": min(temps),
                "max_temp": max(temps)
            }
        return {}

    def get_alerts(self, city: str):
        # Return any alerts for the given city
        return self.alerts.get(city, [])
