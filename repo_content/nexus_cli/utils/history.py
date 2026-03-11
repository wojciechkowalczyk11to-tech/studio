from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB=Path.home()/'.nexus'/'history.db'

def init_history() -> None:
    DB.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB) as con:
        con.execute('CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY, session TEXT, role TEXT, message TEXT, ts TEXT)')

def add_message(session:str,role:str,message:str)->None:
    init_history()
    with sqlite3.connect(DB) as con:
        con.execute('INSERT INTO history(session,role,message,ts) VALUES(?,?,?,?)',(session,role,message,datetime.now(tz=timezone.utc).isoformat()))

def list_sessions()->list[str]:
    init_history()
    with sqlite3.connect(DB) as con:
        return [r[0] for r in con.execute('SELECT DISTINCT session FROM history ORDER BY id DESC LIMIT 20').fetchall()]

def clear_history()->None:
    init_history()
    with sqlite3.connect(DB) as con:
        con.execute('DELETE FROM history')
