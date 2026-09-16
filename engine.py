from dataclasses import dataclass
from ..config import VISIT_COST_EUR,BROKEN_COST_PER_WEEK_EUR,WEIGHTS
@dataclass
class Result:
    risk_score:float;priority:str;estimated_avoidable_cost:float
    decision:str;confidence:str;reasons:list[str]
def clamp(x):return max(0,min(100,x))
def score(g):
    f=clamp(g.failure_rate*100);i=clamp(g.incidents_30d/10*100)
    d=clamp(g.downtime_hours_30d/100*100)
    r=clamp((30-g.days_since_last_incident)/30*100)
    return round(clamp(f*WEIGHTS["failure_rate"]+i*WEIGHTS["incidents"]+
                       d*WEIGHTS["downtime"]+r*WEIGHTS["recency"]),2)
def priority(s):
    if s>=80:return "CRITICAL"
    if s>=60:return "HIGH"
    if s>=30:return "MEDIUM"
    return "LOW"
def rank(g):
    s=score(g);p=priority(s)
    cost=BROKEN_COST_PER_WEEK_EUR if p in {"HIGH","CRITICAL"} else 0
    decision="VISIT" if cost>VISIT_COST_EUR else "MONITOR"
    reasons=[]
    if g.failure_rate>=.15:reasons.append("Failure rate is elevated.")
    if g.incidents_30d>=5:reasons.append("Repeated incidents occurred in the last 30 days.")
    if g.downtime_hours_30d>=40:reasons.append("Downtime is significant.")
    if g.days_since_last_incident<=7:reasons.append("A recent incident increases priority.")
    if cost>VISIT_COST_EUR:reasons.append("One week of recurring cost exceeds the visit cost.")
    if not reasons:reasons.append("Current indicators do not cross the visit threshold.")
    conf="HIGH" if len(reasons)>=3 else "MEDIUM" if len(reasons)==2 else "LOW"
    return Result(s,p,round(cost,2),decision,conf,reasons)
