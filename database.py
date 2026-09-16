from pathlib import Path
import csv,sqlite3
from .models import Gateway
BASE=Path(__file__).resolve().parent.parent
CSV=BASE/"data/gateways.csv"; DB=BASE/"gateway.db"
def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
    c=conn()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS gateways(
      gateway_id TEXT PRIMARY KEY,name TEXT NOT NULL,failure_rate REAL NOT NULL,
      incidents_30d INTEGER NOT NULL,downtime_hours_30d REAL NOT NULL,
      days_since_last_incident INTEGER NOT NULL,status TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS audit_log(
      id INTEGER PRIMARY KEY AUTOINCREMENT,action TEXT NOT NULL,
      gateway_id TEXT,details TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
    ''')
    if c.execute("SELECT COUNT(*) FROM gateways").fetchone()[0]==0: load_csv(c)
    c.commit();c.close()
def load_csv(c=None):
    own=c is None
    if own:c=conn()
    with CSV.open(newline="",encoding="utf-8") as f:
        rows=[(r["gateway_id"].strip(),r["name"].strip(),float(r["failure_rate"]),
        int(r["incidents_30d"]),float(r["downtime_hours_30d"]),
        int(r["days_since_last_incident"]),r["status"].strip().upper()) for r in csv.DictReader(f)]
    c.executemany("INSERT OR REPLACE INTO gateways VALUES(?,?,?,?,?,?,?)",rows)
    if own:c.commit();c.close()
def replace_rows(rows):
    c=conn()
    try:
        c.execute("BEGIN");c.execute("DELETE FROM gateways")
        c.executemany("INSERT INTO gateways VALUES(?,?,?,?,?,?,?)",rows)
        c.execute("INSERT INTO audit_log(action,details) VALUES(?,?)",("CSV_UPLOAD",f"Imported {len(rows)} records"))
        c.commit()
    except Exception:c.rollback();raise
    finally:c.close()
def audit(action,details,gateway_id=None):
    c=conn();c.execute("INSERT INTO audit_log(action,gateway_id,details) VALUES(?,?,?)",(action,gateway_id,details));c.commit();c.close()
def gateways():
    c=conn();r=c.execute("SELECT * FROM gateways ORDER BY gateway_id").fetchall();c.close()
    return [Gateway(**dict(x)) for x in r]
def gateway(gid):
    c=conn();r=c.execute("SELECT * FROM gateways WHERE gateway_id=?",(gid,)).fetchone();c.close()
    return Gateway(**dict(r)) if r else None
def audit_rows():
    c=conn();r=c.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT 50").fetchall();c.close()
    return [dict(x) for x in r]
