from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB=Path.home()/'.nexus'/'costs.db'

def init_costs()->None:
    DB.parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(DB) as con:
        con.execute('CREATE TABLE IF NOT EXISTS costs(id INTEGER PRIMARY KEY, provider TEXT, model TEXT, input_tokens INTEGER, output_tokens INTEGER, cost_usd REAL, ts TEXT)')

def log_cost(provider:str,model:str,input_tokens:int,output_tokens:int,cost_usd:float)->None:
    init_costs()
    with sqlite3.connect(DB) as con:
        con.execute('INSERT INTO costs(provider,model,input_tokens,output_tokens,cost_usd,ts) VALUES(?,?,?,?,?,?)',(provider,model,input_tokens,output_tokens,cost_usd,datetime.now(tz=timezone.utc).isoformat()))

def stats()->list[tuple]:
    init_costs()
    with sqlite3.connect(DB) as con:
        return con.execute('SELECT provider,model,SUM(cost_usd) FROM costs GROUP BY provider,model').fetchall()
