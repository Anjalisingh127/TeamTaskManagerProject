from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "email": current_user.email,
        "role": current_user.role
    }


@router.get("/admin")
def admin_only(user=Depends(require_admin)):
    return {"message": "Welcome Admin!"}