from __future__ import annotations
from typing import Optional, List, Text
import enum
from pydantic import validate_arguments
from sqlalchemy import (
    Column,  ForeignKey,
    String, Table, UniqueConstraint
)

from sqlalchemy.types import Enum
from sqlalchemy.orm import (
    relationship, mapped_column, 
    Mapped, validates
)

from src.cruds.database import Base
from src.models import user_model



questions_topics = Table(
    "questions_topics",
    Base.metadata,
    Column("question_id", ForeignKey(
        "questions.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column("topic_id", ForeignKey("topics.id",
           ondelete="CASCADE", onupdate="CASCADE")),
    UniqueConstraint('question_id', 'topic_id')
    
)


class Topic(Base):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    topic: Mapped[str] = mapped_column(String, nullable=False, unique=True)



class TestCase(Base):
    __tablename__ = "testcases"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    timeout: Mapped[int] = mapped_column()
    value: Mapped[Text] = mapped_column()
    ans: Mapped[Text] = mapped_column()
    is_private: Mapped[bool] = mapped_column()
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id",ondelete="CASCADE",onupdate="CASCADE"),default=0)


class Level(enum.Enum):
    easy = 1
    medium = 2
    hard = 3
    expert = 4

class Question(Base):
    __tablename__="questions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    is_live: Mapped[bool] = mapped_column(default=True, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="SET DEFAULT",onupdate="CASCADE"),default=0)
    topics: Mapped[List[Topic]] = relationship(secondary=questions_topics, lazy="raise")
    testcases: Mapped[List[TestCase]] = relationship(lazy="raise")
    level: Mapped[enum.Enum] = mapped_column(Enum(Level))
    
    
    @validates("topics")
    def _map_dict_to_topic(self, _, value) -> Topic:
        print(value)
        if isinstance(value,Topic):
            return value
        return Topic(**value)
        

class Status(enum.Enum):
    accepted = 1
    wrong_anwer = 2
    runtime_error = 3
    compile_error = 4
    partially_accepted = 5
    pending = 6




class Answer(Base):
    __tablename__="answers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    submission_id: Mapped[int] = mapped_column(ForeignKey("submissions.id",ondelete="SET DEFAULT",onupdate="CASCADE"),default=1)
    testcase_id: Mapped[int] = mapped_column(ForeignKey("testcases.id",ondelete="SET DEFAULT",onupdate="CASCADE"),default=1)
    value: Mapped[Text] = mapped_column()
    status: Mapped[enum.Enum] = mapped_column(Enum(Status))
        

class Submission(Base):
    __tablename__="submissions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    details: Mapped[str] = mapped_column(String(250))
    status: Mapped[enum.Enum] = mapped_column(Enum(Status))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="SET DEFAULT",onupdate="CASCADE"),default=1)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id",ondelete="SET NULL",onupdate="CASCADE"),nullable=True)   
    
    



