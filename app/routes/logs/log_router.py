from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.common.schema.models import User, Log
from firebase import send_push_notification
from app.common.schema.common import response_maker, APIResponse, LogCreate, LogDTO


router = APIRouter(prefix="/log", tags=["log"])

def api_response(data=None, message="success", success=True, error_code=0):
    return APIResponse(
        success=success,
        message=message,
        error_code=error_code,
        data=data
    )
  
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/", 
    response_model=LogDTO,
    responses=response_maker([404, 400])
)
def receive_log(log: LogCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.app_id == log.app_id).first()

    if not user:
        return api_response(message="User not found", success=False, error_code=404)

    db_log = Log(
        level=log.level,
        message=log.message,
        user_id=user.id
    )

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    if log.level.lower() in ("info", "debug", "error", "warn", "critical"):
        if user.fcm_token:
            send_push_notification(
                token=user.fcm_token,
                title=f"[{log.level}] Error Log",
                body=log.message
            )

    return api_response(data=db_log)
