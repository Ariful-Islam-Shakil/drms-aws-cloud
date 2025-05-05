# main2.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from models import EmployeeInput, UpdateEmployeeInput
import employee_services, images_services
import yolo_api
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/employee/add")
def add_employee(data: EmployeeInput):
    return employee_services.add_employee(data)

@app.put("/employee/update/{u_id}")
def update_employee(u_id: str, data: UpdateEmployeeInput):
    return employee_services.update_employee(u_id, data)

@app.get("/employees/getEmployees")
def get_employees():
    return employee_services.get_employees()

@app.get("/employees/getEmployee/{emp_id}")
def get_employee_by_id(emp_id: str):
    return employee_services.get_employee_by_id(emp_id)

@app.delete("/employees/delete/{emp_id}")
def delete_employee_by_id(emp_id: str):
    return employee_services.delete_employee_by_id(emp_id)


#Images Services
@app.post("/images/upload/")
async def detect_tags(emp_id:str = Form(...),  file: UploadFile = File(...)): 
    return images_services.add_image_metadata(emp_id, file)

    
