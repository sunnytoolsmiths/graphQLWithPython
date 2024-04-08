from graphene import ObjectType, List
from app.gql.types import JobObject, EmployerObject
from app.db.data import employers_data, jobs_data
from app.db.database import retrive_data
from app.db.models import Job, Employer
from sqlalchemy.orm import joinedload
from app.db.database import Session

class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs (root, info):
        #return retrive_data(Job)
        return Session().query(Job).options(joinedload(Job.employer)).all()
    
    def resolve_employers (root, info):
        return retrive_data(Employer)