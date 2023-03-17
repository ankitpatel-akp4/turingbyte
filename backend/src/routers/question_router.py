from fastapi import Depends, HTTPException, APIRouter, status, Response
from src.services.auth_service import get_current_active_user

from src.schemas import question_schemas
from src.models import question_model
from typing import List
import src.commons.parameters as parameters

question_router = APIRouter(prefix="/questions",tags=["Question"])



@question_router.post("/",response_model=question_schemas.Question)
async def create_question(question:question_schemas.QuestionCreate):
    """
    level: 1 = easy, 2 = medium, 3 = hard, 4 = expert
    """
    # print(question.dict())
    new_question = question_model.Question(**question.dict())
    topics = []
    for x in new_question.topics:
        topic:question_model.Topic = await question_model.Topic.get(x.id)
        if topic:
            topics.append(topic)
        else:
            topics.append(question_model.Topic(topic=x.topic))
    new_question.topics.clear()
    await new_question.update()
    new_question.topics += topics 
    await new_question.update()
    new_question: question_model.Question = await question_model.Question.get(new_question.id,eager_load=["topics"])
    return new_question

@question_router.put("/")
async def update_question(question:question_schemas.Question):
    """
    level: 1 = easy, 2 = medium, 3 = hard, 4 = expert
    """
    found_question:question_model.Question = await question_model.Question.get(question.id,eager_load=["topics"])
    if not found_question:
        raise HTTPException(
            status_code=400, detail=f"no record found by id: {question.id}")
    topics = []
    for x in question.topics:
        topic:question_model.Topic = await question_model.Topic.get(x.id)
        if topic:
            topics.append(topic)
        else:
            topics.append(question_model.Topic(topic=x.topic))
    question.topics = topics
    await found_question.update(question.dict())
    return found_question


def filter(id: int = None, name: str = None):
    return {"id": id, "name": name}
@question_router.get("/",response_model=list[question_schemas.Question])
async def search_question(filter: dict = Depends(filter),page: dict = Depends(parameters.page),sort:str = parameters.sort()):
    return await question_model.Question.search(filter=filter,page=page,sort=sort)



# testcase_router = APIRouter(prefix="/testcases",tags=["Testcase"])
@question_router.post("/testcases",response_model=question_schemas.TestCase)
async def create_testcase(testcase:question_schemas.TestCaseCreate):
    new_testcase = question_model.TestCase(**testcase.dict())
    await new_testcase.save()
    return new_testcase

@question_router.put("/testcases",response_model=question_schemas.TestCase)
async def update_testcase(testcase:question_schemas.TestCase):
    found_testcase:question_model.TestCase = await question_model.TestCase.get(testcase.id)
    if not found_testcase:
        raise HTTPException(
            status_code=400, detail=f"no record found by id: {found_testcase.id}")
    await found_testcase.update(testcase.dict())
    return found_testcase


topic_router = APIRouter(prefix="/topics",tags=["Topic"])
@topic_router.post("/",response_model=question_schemas.Topic)
async def create_topic(topic:question_schemas.TopicCreate):
    new_topic = question_model.Topic(**topic.dict())
    await new_topic.save()
    return new_topic

def filter(id: int = None, topic: str = None):
    return {"id": id, "topic": topic}
@topic_router.get("/",response_model=list[question_schemas.Topic])
async def search_topic(filter: dict = Depends(filter),page: dict = Depends(parameters.page),sort:str = parameters.sort()):
    return await question_model.Topic.search(filter=filter,page=page,sort=sort)

