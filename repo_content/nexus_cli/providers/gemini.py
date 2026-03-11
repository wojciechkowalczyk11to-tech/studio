from __future__ import annotations

from google import genai

from nexus_shared.thinking import build_genai_config


def ask_gemini(api_key:str,model:str,system_prompt:str,query:str)->str:
    try:
        client=genai.Client(api_key=api_key or None)
        cfg=build_genai_config(system_prompt,query,command='nexus')
        resp=client.models.generate_content(model=model,contents=query,config=cfg)
        return resp.text or 'Brak odpowiedzi modelu.'
    except Exception as exc:
        raise RuntimeError(f'Błąd Gemini: {exc}') from exc
