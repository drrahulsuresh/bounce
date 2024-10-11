from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Define a database model for the survey data
class SurveyData(Base):
    __tablename__ = 'survey_data'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    demographic = Column(String)
    response_type = Column(String)
    response_value = Column(String)

# Database connection
engine = create_engine('sqlite:///survey_data.db')
Base.metadata.create_all(engine)
