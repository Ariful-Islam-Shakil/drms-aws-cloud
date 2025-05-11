# models.py
from pydantic import BaseModel

class EmployeeInput(BaseModel):
    name: str

class UpdateEmployeeInput(BaseModel):
    name: str
