from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.study_planner import generate_study_plan

router = APIRouter(
    prefix="/study",
    tags=["Study Planner"]
)


class StudyRequest(BaseModel):
    document_text: str


@router.post("/")
def study_plan(request: StudyRequest):

    plan = generate_study_plan(
        request.document_text
    )

    return plan