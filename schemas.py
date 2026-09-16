from pydantic import BaseModel,Field
class GatewayResponse(BaseModel):
    gateway_id:str; name:str; failure_rate:float; incidents_30d:int
    downtime_hours_30d:float; days_since_last_incident:int; status:str
class RecommendationResponse(BaseModel):
    gateway_id:str; name:str; risk_score:float; priority:str
    estimated_avoidable_cost:float; visit_cost:float; decision:str
    confidence:str; reasons:list[str]
class RecommendationRunResponse(BaseModel):
    generated_count:int; visit_count:int
    recommendations:list[RecommendationResponse]
class AnalyticsResponse(BaseModel):
    total_gateways:int; healthy:int; warning:int; degraded:int
    high_or_critical:int; visit_recommended:int
    average_risk_score:float; total_weekly_exposure:float
