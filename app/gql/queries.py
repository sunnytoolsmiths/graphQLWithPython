from graphene import ObjectType, List
from app.gql.types import JobObject, EmployerObject
from app.db.data import employers_data, jobs_data


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs (root, info):
        return jobs_data
    
    def resolve_employers (root, info):
        return employers_data