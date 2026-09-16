from backend.models import Gateway
from backend.ranking.engine import score,priority,rank
def test_score_range():assert 0<=score(Gateway("X","T",.2,5,40,3,"DEGRADED"))<=100
def test_priority():assert priority(10)=="LOW" and priority(60)=="HIGH" and priority(80)=="CRITICAL"
def test_visit_rule():assert rank(Gateway("X","T",.3,10,100,0,"DEGRADED")).decision=="VISIT"
def test_monitor_rule():assert rank(Gateway("X","T",.01,0,1,30,"HEALTHY")).decision=="MONITOR"
