import os
VISIT_COST_EUR=float(os.getenv("VISIT_COST_EUR","380"))
BROKEN_COST_PER_WEEK_EUR=float(os.getenv("BROKEN_COST_PER_WEEK_EUR","600"))
WEIGHTS={
 "failure_rate":float(os.getenv("WEIGHT_FAILURE","0.40")),
 "incidents":float(os.getenv("WEIGHT_INCIDENTS","0.25")),
 "downtime":float(os.getenv("WEIGHT_DOWNTIME","0.20")),
 "recency":float(os.getenv("WEIGHT_RECENCY","0.15"))
}
