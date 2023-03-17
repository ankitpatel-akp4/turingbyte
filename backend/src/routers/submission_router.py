from fastapi import Depends, HTTPException, APIRouter, status, Response
from src.services.auth_service import get_current_active_user
from src.schemas import question_schemas
from src.services import submission_service
import subprocess
import asyncio


submission_router = APIRouter(prefix="/submissions",tags=["Submission"])

@submission_router.post("/")
async def submit(submission_req:question_schemas.SubmissionCreate):
    await submission_service.submit(submission_req)