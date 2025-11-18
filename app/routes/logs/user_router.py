from fastapi import APIRouter
from pydantic import BaseModel
from firebase import register_token

router = APIRouter(tags=["User"])

class TokenRegisterRequest(BaseModel):
    user_id: int
    token: str

@router.post("/register-token")
async def register_fcm_token(req: TokenRegisterRequest):
    await register_token(req.user_id, req.token)
    return {"success": True, "message": "Token registered!"}
