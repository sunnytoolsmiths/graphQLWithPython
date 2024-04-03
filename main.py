from graphene import Schema, ObjectType, String, Int, List, Field
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler

from sqlalchemy import create_engine, Column, Integer, String as saString, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DB_URL = "postgresql+psycopg://postgres:gGAhrVYEWKlMHEEkoAbagxMtRMDQZKIp@monorail.proxy.rlwy.net:57833/railway"
engine = create_engine(DB_URL)

Base = declarative_base()

class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True)
    name = Column(saString)
    contact_email = Column(saString)
    industry = Column(saString)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    jobs = relationship ("Job", back_populates="employer")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(saString)
    description =  Column(saString)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs")


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

# emp1 = Employer(id=1, name='MetaTechA', contact_email="hey@andybek.com", industry ="Tech")
# session.add(emp1)

# static data
employers_data = [
    {"id": 1, "name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"id": 2, "name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"id": 1, "title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"id": 2, "title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    {"id": 3, "title": "Accountant", "description": "Manage financial records", "employer_id": 2},
]

for employer in employers_data: 
    #** --> unpack the dictionary
    emp = Employer(**employer)
    session.add(emp)

for job in jobs_data:
    session.add(Job(**job))

session.commit()

class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return [job for job in jobs_data if job ["employer_id"] == root["id"]]

class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root, info):
        return next((employer for employer in employers_data if employer ["id"]== root["employer_id"]), None)

class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs (root, info):
        return jobs_data
    
    def resolve_employers (root, info):
        return employers_data
    

schema = Schema(query=Query) 

app = FastAPI()

app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))
