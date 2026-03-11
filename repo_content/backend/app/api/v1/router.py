from fastapi import APIRouter
from pydantic import BaseModel

api_router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    mode: str

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}

@api_router.post("/chat")
async def chat(request: ChatRequest):
    return {"content": f"Mocked response for {request.query} in {request.mode} mode", "meta_footer": "Mocked footer"}

@api_router.post("/rag/upload")
async def upload_rag_document():
    return {"message": "Document uploaded successfully", "item_id": "mock_id", "chunk_count": 10}

class RegisterRequest(BaseModel):
    telegram_id: int
    username: str
    first_name: str
    last_name: str

@api_router.post("/auth/register")
async def register_user(req: RegisterRequest):
    return {"token": "mock_token"}

class UnlockRequest(BaseModel):
    telegram_id: int
    code: str

@api_router.post("/auth/unlock")
async def unlock_demo(req: UnlockRequest):
    return {"status": "unlocked"}

@api_router.get("/pricing")
async def get_pricing():
    return {
        "full_access_monthly": {
            "title": "FULL_ACCESS - 30 dni",
            "description": "Pełny dostęp do wszystkich funkcji + 1000 kredytów",
            "stars": 150,
        },
        "full_access_weekly": {
            "title": "FULL_ACCESS - 7 dni",
            "description": "Pełny dostęp do wszystkich funkcji + 250 kredytów",
            "stars": 50,
        },
        "deep_day": {
            "title": "DEEP Day Pass (24h)",
            "description": "Tryb DEEP na 24 godziny + 100 kredytów",
            "stars": 25,
        },
        "credits_100": {
            "title": "100 kredytów",
            "description": "Doładowanie 100 kredytów",
            "stars": 50,
        },
        "credits_500": {
            "title": "500 kredytów",
            "description": "Doładowanie 500 kredytów",
            "stars": 200,
        },
        "credits_1000": {
            "title": "1000 kredytów",
            "description": "Doładowanie 1000 kredytów",
            "stars": 350,
        },
    }

class PaymentProcessRequest(BaseModel):
    product_id: str
    amount: int

@api_router.post("/payments/process")
async def process_payment(req: PaymentProcessRequest):
    return {"status": "success", "message": f"Payment for {req.product_id} processed"}
