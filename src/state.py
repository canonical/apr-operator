import dataclasses

class AprStateBackend:
    @staticmethod
    def temperature_in_delft():
        # todo: curl "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
        return 4.2  # brr



@dataclasses.dataclass
class AprState:
    is_up: bool
    temperature_in_delft: int
