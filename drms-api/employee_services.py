from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


# Allow CORS from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Or ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dynamodb = boto3.resource('dynamodb')
employee_table = dynamodb.Table('team-alpha-ai')


# Pydantic model for input
class EmployeeInput(BaseModel):
    name: str


class UpdateEmployeeInput(BaseModel):
    name: str


#Creation of unique ID
def create_unique_id():
    employees = get_employees().get("employees", [])
    if not employees:
        return 'EMP001'

    # Sort employees by u_id
    employees.sort(key=lambda x: int(''.join(filter(str.isdigit, x['u_id']))))
    emp_id = employees[-1]['u_id']

    prefix = ''.join(filter(str.isalpha, emp_id))
    number = ''.join(filter(str.isdigit, emp_id))
    number = str(int(number) + 1).zfill(len(number))

    return prefix + number

# Add new employee 
def add_employee(data: EmployeeInput):
    try:
        # Validate name
        if not data.name.strip() or data.name.strip().isdigit():
            raise HTTPException(status_code=400, detail="Invalid name: must contain non-digit characters.")
        
        # u_id = str(uuid.uuid4())
        u_id = create_unique_id()
        created_time = datetime.now(ZoneInfo("Asia/Dhaka")).isoformat()

        new_item = {
            'u_id': u_id,
            'name': data.name,
            'created_time': created_time
        }

        response = employee_table.get_item(Key={'id': 'Ariful_Islam'})
        item = response.get('Item')

        if item and 'employee' in item:
            item['employee'].append(new_item)
        else:
            item = {
                'id': 'Ariful_Islam',
                'employee': [new_item]
            }

        employee_table.put_item(Item=item)
        return {"message": "Employee added successfully", "u_id": u_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update employee 
def update_employee(u_id: str, update_data: UpdateEmployeeInput):
    try:

        # Validate name
        if not update_data.name.strip() or update_data.name.strip().isdigit():
            raise HTTPException(status_code=400, detail="Invalid name: must contain non-digit characters.")

        response = employee_table.get_item(Key={'id': 'Ariful_Islam'})
        item = response.get('Item')

        if not item or 'employee' not in item:
            raise HTTPException(status_code=404, detail="Employee list not found")

        updated = False
        for emp in item['employee']:
            if emp['u_id'] == u_id:
                emp.update({"name": update_data.name})
                updated = True
                break

        if updated:
            employee_table.put_item(Item=item)
            return {"message": f"Employee with u_id {u_id} updated successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Employee with u_id {u_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all employees 
def get_employees():
    try:
        response = employee_table.get_item(Key={'id': 'Ariful_Islam'})
        item = response.get('Item')

        if not item or 'employee' not in item:
            return {"employees": []}
        return {"employees": item['employee']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all employee by id 
def get_employee_by_id(emp_id):
    try:
        response = employee_table.get_item(Key={'id': 'Ariful_Islam'})
        item = response.get('Item')

        if not item or 'employee' not in item:
            raise HTTPException(status_code=404, detail="Employee list not found")

        for emp in item['employee']:
            if emp['u_id'] == emp_id:
                return emp
        raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete Employee by ID 
def delete_employee_by_id(emp_id):
    try:
        response = employee_table.get_item(Key={'id':'Ariful_Islam'})
        item = response.get('Item')

        if not item or 'employee' not in item:
            raise HTTPException(status_code = 400, details="Employee list not found")
        
        deleted = False
        updated_item = []
        for emp in item['employee']:
            if emp['u_id'] != emp_id:
                updated_item.append(emp)
            else:
                deleted = True
        if deleted:
            employee_table.put_item(Item={
            'id': 'Ariful_Islam',
            'employee': updated_item
        })
            return {"message": f"Employee with u_id {emp_id} deleted successfully"}
        else:
            raise HTTPException(status_code = 400, details=f"Employee with id {emp_id} not found")
    except Exception as e:
        raise HTTPException(status_code = 500, details=str(e))