from __future__ import annotations

import httpx


def ask_openrouter(endpoint:str,api_key:str,model:str,query:str)->str:
    try:
        headers={'Authorization': f'Bearer {api_key}'} if api_key else {}
        payload={'model':model,'messages':[{'role':'user','content':query}]}
        with httpx.Client(timeout=30.0) as c:
            r=c.post(endpoint,json=payload,headers=headers)
            r.raise_for_status()
            data=r.json()
        return str(data)
    except Exception as exc:
        raise RuntimeError(f'Błąd providera openrouter: {exc}') from exc
