from fastapi import APIRouter, BackgroundTasks, Depends
from app.blog.oauth2 import get_current_user
from app.blog.repository.tasks import send_greeting_email_task, get_valid_email
from app.blog.schemas import ShowUser
from fastapi import status


router = APIRouter(
    tags=['Tasks'],
    prefix="/api/task"
)


@router.get("/greet")
async def get_greet_email(user: ShowUser = Depends(get_current_user)):
    send_greeting_email_task.delay(username=user.username, user_email=get_valid_email(user.email))
    return {
        "status": "DONE",
        "data": "Email sent",
        "details": None
    }

