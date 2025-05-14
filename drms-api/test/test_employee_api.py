import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
import employee_services, copy


client = TestClient(app)
demo_db_const = {
        'Item' : {
            'id' : 'Ariful_Islam',
            'employee': [
                {
                    'u_id': 'EMP001',
                    'name' : 'Arif',
                    'active': True
                },
                {
                    'u_id': 'EMP002',
                    'name' : 'Shakil',
                    'active': False
                },
                {
                    'u_id': 'EMP003',
                    'name' : 'Tuhin',
                    'active': True
                }
            ]
        }
    }

active_demo_db = [
            {
                'u_id': 'EMP001',
                'name' : 'Arif',
                'active': True
            },
            {
                'u_id': 'EMP003',
                'name' : 'Tuhin',
                'active': True
            }
        ]



################ Testing Add Employee API ###########################
@patch("employee_services.employee_table") 
def test_add_employee(mock_table):
    # mock_create_id.return_value = 'EMP001'
    mock_table.get_item.return_value = {}
    mock_table.put_table.return_value = {}

    payload = {'name': 'Ariful Islam'}
    response = client.post("/employee/add", json=payload)
    assert response.status_code == 200
    assert response.json()['message'] == "Employee added successfully"
    assert response.json()['u_id'] == 'EMP001'

    demo_db = copy.deepcopy(demo_db_const)
    mock_table.get_item.return_value = demo_db
    payload = {'name': 'Ariful Islam Shakil'}
    response = client.post("/employee/add", json=payload)
    assert response.status_code == 200
    assert response.json()['message'] == "Employee added successfully"
    assert response.json()['u_id'] == 'EMP004'


def test_add_employee_invalid():
    payload = {'name': '12'}
    response = client.post('/employee/add', json=payload)
    assert response.status_code == 500
    assert '400: Invalid name: must contain non-digit characters.' in response.json()['detail']

    payload = {'name': ' '}
    response = client.post('/employee/add', json=payload)
    assert response.status_code == 500
    assert '400: Invalid name: must contain non-digit characters.' in response.json()['detail']




################ Testing Get Employees API ###########################
@patch('employee_services.employee_table')
def test_get_employees(mock_table):

    demo_db = copy.deepcopy(demo_db_const)
    mock_table.get_item.return_value = demo_db
    response = client.get('/employees/getEmployees')
    assert response.status_code == 200
    assert response.json()['employees'] == active_demo_db

    mock_table.get_item.side_effect = Exception('DynamoDB Failure')
    response = client.get('/employees/getEmployees')
    assert response.status_code == 500
    assert "DynamoDB Failure" in response.json()['detail']

@patch('employee_services.employee_table')
def test_get_employee_by_id(mock_table):
    demo_db = copy.deepcopy(demo_db_const)
    mock_table.get_item.return_value = demo_db
    response = client.get('/employees/getEmployee/EMP001')
    assert response.status_code == 200
    assert response.json() == active_demo_db[0]

    response = client.get('/employees/getEmployee/EMP002')
    assert response.status_code == 500
    assert '404: Employee not found' in response.json()['detail']

    mock_table.get_item.return_value = {}
    response = client.get('/employees/getEmployee/EMP002')
    assert response.status_code == 500
    assert '404: Employee list not found' in response.json()['detail']



################ Testing Update Employees API ##########################
@patch('employee_services.employee_table')
def test_update_employee(mock_table):
    demo_db = copy.deepcopy(demo_db_const)
    mock_table.get_item.return_value = demo_db
    response = client.put("/employee/update/EMP001", json={'name': 'Shakil Updated'})
    assert response.status_code == 200
    assert "Employee with u_id EMP001 updated successfully" in response.json()['message']

    demo_db = copy.deepcopy(demo_db_const)
    mock_table.get_item.return_value = demo_db
    response = client.put("/employee/update/EMP002", json={'name': 'Shakil Updated'})
    assert response.status_code == 500
    assert"404: Employee with u_id EMP002 not found" in response.json()['detail']


################ Testing Delete Employees API ##########################
@patch('employee_services.employee_table')
def test_delete_employee(mock_table):
    demo_db = copy.deepcopy(demo_db_const)
    mock_table.get_item.return_value = demo_db
    mock_table.put_table.return_value = {}
    response = client.delete('/employees/delete/EMP001')
    assert response.status_code == 200
    assert response.json()['message'] == 'Employee with u_id EMP001 deleted successfully'

    demo_db = copy.deepcopy(demo_db_const)
    mock_table.get_item.return_value = demo_db
    mock_table.put_table.return_value = {}
    response = client.delete('/employees/delete/EMP005')
    assert response.status_code == 500
    assert response.json()['detail'] == '405: Employee with id EMP005 not found'

    mock_table.get_item.return_value = {} 
    response = client.delete('/employees/delete/EMP005')
    assert response.status_code == 500
    assert response.json()['detail'] == '404: Employee list not found'

    
    ######################## Testing Images services #################
    