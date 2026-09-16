from dataclasses import dataclass
@dataclass
class Gateway:
    gateway_id:str
    name:str
    failure_rate:float
    incidents_30d:int
    downtime_hours_30d:float
    days_since_last_incident:int
    status:str
