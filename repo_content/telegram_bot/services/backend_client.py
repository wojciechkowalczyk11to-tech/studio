import httpx
from typing import Optional, Dict, Any
from config import settings

class BackendClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.backend_url
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def close(self):
        await self.client.aclose()

    async def chat(self, token: str, query: str, mode: str) -> Dict[str, Any]:
        response = await self.client.post(
            "/api/v1/chat",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": query, "mode": mode}
        )
        response.raise_for_status()
        return response.json()

    async def upload_rag_document(self, token: str, filename: str, content: bytes) -> Dict[str, Any]:
        response = await self.client.post(
            "/api/v1/rag/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (filename, content)}
        )
        response.raise_for_status()
        return response.json()

    async def register_user(self, telegram_id: int, username: str, first_name: str, last_name: str) -> Dict[str, Any]:
        response = await self.client.post(
            "/api/v1/auth/register",
            json={
                "telegram_id": telegram_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name
            }
        )
        response.raise_for_status()
        return response.json()

    async def unlock_demo(self, telegram_id: int, code: str) -> Dict[str, Any]:
        response = await self.client.post(
            "/api/v1/auth/unlock",
            json={"telegram_id": telegram_id, "code": code}
        )
        response.raise_for_status()
        return response.json()

    async def get_pricing(self) -> Dict[str, Any]:
        response = await self.client.get("/api/v1/pricing")
        response.raise_for_status()
        return response.json()

    async def process_payment(self, token: str, product_id: str, amount: int) -> Dict[str, Any]:
        response = await self.client.post(
            "/api/v1/payments/process",
            headers={"Authorization": f"Bearer {token}"},
            json={"product_id": product_id, "amount": amount}
        )
        response.raise_for_status()
        return response.json()

def get_backend_client() -> BackendClient:
    return BackendClient()
