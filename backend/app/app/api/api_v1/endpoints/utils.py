from typing import Any
import logging 

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email

router = APIRouter()

logger = logging.getLogger("api")

@router.post("/infer/", response_model=schemas.Msg, status_code=201)
def test_infer(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test neuralnets inference.
    """
    celery_app.send_task("app.worker.infer", args=[])
    return {"msg": "Word received"}

@router.post("/test-pytorch/", response_model=schemas.Msg, status_code=201)
def test_pytorch(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker and Pytorch.
    """
    celery_app.send_task("app.worker.test_pytorch", args=[msg.msg])
    return {"msg": "Word received"}

@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
