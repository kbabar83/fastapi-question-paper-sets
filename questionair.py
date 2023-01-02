from fastapi import FastAPI, Request, Depends, BackgroundTasks, status
import models
from models import Questionset,Question,QuestionOption,GroupQuestion
from pydantic import BaseModel, HttpUrl
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Optional, List
from typing import Union
from sqlalchemy.orm import joinedload


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class QuestionsetRequest(BaseModel):
    questionset_id : int
    set_name : str
    set_slug : str
    enable_negative_marking : bool
    negative_marking_percentage : int
    IdealTimetoComplete : int
    
    class Config:
        orm_mode = True
#--------------------------------------------
class GroupQuestionRequest(BaseModel):
    groupquestion_id : int
    questionset_id : int
    group_name : str
    
    class Config:
        orm_mode = True
    
#--------------------------------------------        
class QuestionRequest(BaseModel):
    question_id : int
    groupquestion_id : int
    question_text : str
    question_image : str
    question_type : str
    question_order : int
    question_marks : int
    
    class Config:
        orm_mode = True
#-----------------------------------------------
        
class QuestionOptionRequest(BaseModel):
    questionoption_id : int
    question_id : int
    option_text : str
    option_image :str
    option_order : int
    correct_answer : bool
    marks : int
    
    class Config:
        orm_mode = True


#--------------------------List Schemas---------------------------------#        
# class ListQuestionsetRequest(QuestionsetRequest):
#     groupquestions : GroupQuestionRequest
    
#     class Config:
#         orm_mode = True
        
# class ListGroupQuestionRequest(GroupQuestionRequest):
#     questionsets : QuestionsetRequest
#     questions : QuestionRequest
    
#     class Config:
#         orm_mode = True
        
# class ListQuestionRequest(QuestionRequest):
#     groupquestions : GroupQuestionRequest
#     questionoptions :QuestionOptionRequest

#     class Config:
#         orm_mode = True
    
# class ListQuestionOptionRequest(QuestionOptionRequest):
#     questions : QuestionRequest

#     class Config:
#         orm_mode = True
   
class ListQuestionPaper(BaseModel):
    questionsets : QuestionsetRequest
    groupquestions : GroupQuestionRequest
    questions : QuestionRequest
    questionoptions : QuestionOptionRequest
    
    class Config:
        orm_mode = True
#--------------------------------Dependencies-------------------------------------------------------#

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#----------------------------------Endpoint for Questionset -------------------------------------------#

@app.post("/add_questionset/")
async def create_questionset(questionset_request:QuestionsetRequest,db:Session = Depends(get_db)):
    
    questionset = models.Questionset(**questionset_request.dict())

    db.add(questionset)
    db.commit()
    db.refresh(questionset)
    return{"code":"success","questionset":questionset}

@app.get("/get_questionset/")
async def fetch_questionset(questionset_id:int):
    
    db = SessionLocal()
    questionset = db.query(Questionset).filter(Questionset.questionset_id==questionset_id).first()
    return{"questionset":questionset}

@app.get("/all-questionset/")
# async def get_questionsets(db: Session = Depends(get_db)):
async def fetch_all_questionset():
    
    db = SessionLocal()
    questionset = db.query(Questionset).options(joinedload(models.Questionset.groupquestions)).all()
    return{"questionset":questionset}

#----------------------------------Endpoint for GroupQuestion-----------------------------------------#

@app.post("/add_group_question/")
async def create_groupquestion(groupquestion_request:GroupQuestionRequest,db:Session = Depends(get_db)):
    
    groupquestion = models.GroupQuestion(**groupquestion_request.dict())

    db.add(groupquestion)
    db.commit()
    db.refresh(groupquestion)
    return{"code":"success","groupquestion":groupquestion}
    
@app.get("/get_group_question/")
async def fetch_groupquestion(groupquestion_id:int):
    
    db = SessionLocal()
    groupquestion = db.query(GroupQuestion).filter(GroupQuestion.groupquestion_id==groupquestion_id).first()
    return{"groupquestion":groupquestion}

@app.get("/all-group_question/")
async def fetch_all_groupquestion():
    
    db = SessionLocal()
    groupquestion = db.query(GroupQuestion).options(joinedload(models.GroupQuestion.questions)).all()
    return{"groupquestion":groupquestion}


#-------------------------------Endpoint for Question-----------------------------------------------------#

@app.post("/add_question/")
async def create_question(question_request:QuestionRequest,db:Session = Depends(get_db)):
    question = models.Question(**question_request.dict())
    
    db.add(question)
    db.commit()
    db.refresh(question)
    return{"question":question}

@app.get("/get_question/")
async def fetch_questions(question_id:int):
    db = SessionLocal()
    question = db.query(Question).filter(Question.question_id==question_id).first()
    return{"question":question}

@app.get("/all-question/")
async def fetch_all_question():
    
    db = SessionLocal()
    question = db.query(Question).options(joinedload(models.Question.questionoptions)).all()
    return{"question":question}
    

#------------------------------Endpoint for QuestionOption--------------------------------------------------#

@app.post("/add_question_option/")
async def create_question_option(questionoption_request:QuestionOptionRequest,db:Session = Depends(get_db)):
    questionoption = models.QuestionOption(**questionoption_request.dict())
    
    db.add(questionoption)
    db.commit()
    db.refresh(questionoption)
    return{"questionoption":questionoption}

@app.get("/get_question_option/")
async def fetch_questionoption(questionoption_id:int):
    
    db = SessionLocal()
    questionoption = db.query(QuestionOption).filter(QuestionOption.questionoption_id==questionoption_id).first()
    return{"questionoption":questionoption}

@app.get("/all-question-option/")
async def fetch_all_questionoption():
    
    db = SessionLocal()
    questionoption = db.query(QuestionOption).all()
    return{"questionoption":questionoption}

#-------------------------------Endpoint for QuestionPaper----------------------------------------------------#

@app.get("/get_question_paper/")
async def fetch_questionpaper():

    db = SessionLocal()
    questionset = db.query(Questionset).options(
        joinedload(models.Questionset.groupquestions).
        joinedload(models.GroupQuestion.questions).
        joinedload(models.Question.questionoptions)).all()
    
    return{"questionset":questionset}

#------------------------------Endpoint for Particular QuestionPaper--------------------------------------------#

@app.get("/particular_question_paper/")
async def fetch_particular_questionpaper(questionset_id:int):
    
    db = SessionLocal()
    questionset = db.query(Questionset).filter(Questionset.questionset_id==questionset_id).options(
        joinedload(models.Questionset.groupquestions).
        joinedload(models.GroupQuestion.questions).
        joinedload(models.Question.questionoptions)).first()
    
    return{"questionset":questionset}
    
    






    
