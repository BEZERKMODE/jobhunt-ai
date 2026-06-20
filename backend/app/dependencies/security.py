from fastapi import Depends, HTTPException, status
from app.dependencies import get_current_user
from app.models.user import UserRole

def is_admin(_: None = Depends(get_current_user)) -> None:
    # This dependency ensures the current user is an admin.
    # It raises HTTP 403 if the user does not have admin role.
    def _inner(user = Depends(get_current_user)):
        if user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required",
            )
        return None
    return _inner
