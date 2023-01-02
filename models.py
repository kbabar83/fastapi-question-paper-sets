from datetime import datetime
from typing import Union
from typing import Optional
from pydantic import BaseModel, HttpUrl

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Questionset(Base):
    __tablename__ = "questionsets"
    
    questionset_id = Column(Integer, primary_key=True, index=True)
    set_name = Column(String, index=True)
    set_slug  = Column(String, index=True)
    enable_negative_marking = Column(Boolean, default=False)
    negative_marking_percentage = Column(Integer,index=True)
    IdealTimetoComplete = Column(Integer,index=True)
    
    groupquestions = relationship("GroupQuestion", back_populates="questionsets")
    
class GroupQuestion(Base):
    __tablename__ = "groupquestions"
    
    groupquestion_id = Column(Integer,primary_key=True)
    questionset_id = Column(Integer, ForeignKey("questionsets.questionset_id"))
    group_name = Column(String, index=True)
    
    questionsets = relationship("Questionset",back_populates="groupquestions",foreign_keys=[questionset_id])
    questions = relationship("Question",back_populates="groupquestions")


class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer,primary_key=True)
    groupquestion_id = Column(Integer, ForeignKey("groupquestions.groupquestion_id"))
    question_text  = Column(String, index=True)
    question_image = Column(String, index=True)
    question_type  = Column(String, index=True)
    question_order = Column(Integer,index=True)
    question_marks = Column(Integer,index=True)
    
    groupquestions = relationship("GroupQuestion",back_populates="questions",foreign_keys=[groupquestion_id])
    questionoptions = relationship("QuestionOption",back_populates="questions")

    
class QuestionOption(Base):
    __tablename__ = "questionoptions"
    
    questionoption_id = Column(Integer,primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    option_text = Column(String, index=True)
    option_image = Column(String, index=True)
    option_order  = Column(Integer, index=True, default=1)
    correct_answer = Column(Boolean, default=False)
    marks = Column(Integer, index=True, default=None)
    
    questions = relationship("Question",back_populates="questionoptions",foreign_keys=[question_id])
    

##---------------------------------------------------------------------------------------------------------##    
    
# class GrouplineQuestions(Base):
#     __tablename__ = "grouplinequestions"
    
#     grouplinequestion_id = Column(Integer,primary_key=True)
#     groupquestion_id = Column(Integer, ForeignKey("groupquestions.groupquestion_id"))
#     question_id = Column(Integer, ForeignKey("questions.question_id"))
#     question_order = Column(Integer,index=True)
#     question_marks = Column(Integer,index=True)
    
#     questions = relationship("Question",back_populates="grouplinequestions",foreign_keys=[question_id])
#     groupquestions = relationship("GroupQuestion",back_populates="grouplinequestions",foreign_keys=[groupquestion_id])
    
    
    ##Questionset-->Group Question--> Question --> Question Options 