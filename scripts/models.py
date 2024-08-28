from pydantic import BaseModel, field_serializer, Field
from datetime import datetime
from typing import Literal
import uuid

SeniorityLevel = Literal["junior", "mid", "senior"]
industries = ["tech", "finance", "retail", "healthcare", "manufacturing", "real_estate", "other"]
Industry = Literal["tech", "finance", "retail", "healthcare", "manufacturing", "real_estate", "other"]

class EmploymentStint(BaseModel):
    start_date: datetime
    end_date: datetime
    company: str
    seniority_level: SeniorityLevel
    industry: Industry
    achievements:list[str]
    
    

class Profile(BaseModel):
    uuid: str = Field(default_factory=uuid.uuid4)
    stints: list[EmploymentStint]

    @field_serializer("uuid")
    def serialize_uuid(self, uuid: str, _info) -> str:
        return str(uuid)