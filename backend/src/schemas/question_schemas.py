from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
import enum
from typing import Optional, List
from src.models.question_model import Status, Level


class TestCaseBase(BaseModel):
    id: int
    class Config:
        orm_mode = True


class TestCaseOut(BaseModel):
    value: str
    ans: str
    class Config:
        orm_mode = True


class TestCaseCreate(TestCaseOut):
    is_private: bool
    question_id: int


class TestCase(TestCaseCreate,TestCaseBase):
    created_at: datetime


class TopicBase(BaseModel):
    id: int
    class Config:
        orm_mode = True


class TopicCreate(BaseModel):
    
    topic: str
    class Config:
        orm_mode = True


class Topic(TopicCreate,TopicBase):
    id: Optional[int]
    topic: Optional[str]
    


class QuestionBase(BaseModel):
    id: int
    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    name: str
    description: str
    is_live: bool = True
    author_id: int
    level: Level
    topics: List[Topic]
    class Config:
        orm_mode = True


class Question(QuestionCreate, QuestionBase):
    created_at: datetime


class AnswerBase(BaseModel):
    id: int
    class Config:
        orm_mode = True


class AnswerOut(AnswerBase):
    value: str
    status: Status


class Answer(AnswerOut, AnswerBase):
    submission_id: int
    testcase_id: int
    created_at: datetime


class SubmissionBase(BaseModel):
    id:int
    class Config:
        orm_mode = True

class Language(str,enum.Enum):
    java="java"
    python3="python3"
    javaScript="javascript"

class SubmissionCreate(BaseModel):
    question_id: int
    code: str
    language:Language
    class Config:
        orm_mode = True
         
        



class TestCaseWithAnswerAndOutput(BaseModel):
    testcase_id: int
    value: str
    answer: str
    output: str
    status: Status
    class Config:
        orm_mode = True


class Submission(SubmissionCreate,SubmissionBase):
    details: str
    status: Status
    output: List[TestCaseWithAnswerAndOutput]


