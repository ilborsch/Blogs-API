from fastapi import APIRouter, BackgroundTasks, Depends
from ..oauth2 import get_current_user
from app.blog.repository.tasks import send_greeting_email_task, get_valid_email
from ..schemas import ShowUser
from fastapi import status


router = APIRouter(
    tags=['Tasks'],
    prefix="/task"
)


@router.get("/greet")
async def get_greet_email(background: BackgroundTasks, user: ShowUser = Depends(get_current_user)):
    background.add_task(send_greeting_email_task, username=user.username, user_email=get_valid_email(user.email))
    return {
        "status": status.HTTP_200_OK,
        "data": "Email sent",
        "details": None
    }

