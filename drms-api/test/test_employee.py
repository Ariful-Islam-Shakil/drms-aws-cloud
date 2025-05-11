import pytest 
from fastapi import HTTPException
import employee_services
from unittest.mock import patch, MagicMock
from employee_services import add_employee, EmployeeInput



############### Testing Get Employees #############
@patch("employee_services.employee_table.get_item")
def test_get_employees_with_active_and_inactive(mock_get_item):
    mock_get_item.return_value = {
        'Item': {
            'id': 'Ariful Islam',
            'employee': [
                {"name": "Arif", "active": True},
                {"name": "Salma", "active": False},
                {"name": "Tuhin", "active": True}
            ]
        }
    }

    result = employee_services.get_employees()
    assert result == {
        "employees": [
            {"name": "Arif", "active": True},
            {"name": "Tuhin", "active": True}
        ]
    }

@patch("employee_services.employee_table.get_item")
def test_get_employees_with_no_employees_key(mock_get_item):
    mock_get_item.return_value = {'Item': {}}
    result = employee_services.get_employees()
    assert result == {"employees": []} # No employees

@patch("employee_services.employee_table.get_item")
def test_get_employees_with_no_item(mock_get_item):
    mock_get_item.return_value = {} # No items
    result = employee_services.get_employees()
    assert result == {"employees": []}

@patch("employee_services.employee_table.get_item")
def test_get_employees_with_exception(mock_get_item):
    mock_get_item.side_effect = Exception("DynamoDB failure")

    with pytest.raises(Exception) as excinfo:
        employee_services.get_employees()
    assert "DynamoDB failure" in str(excinfo.value)

############### Testing Get Employee by ID #############

# Valid id
@patch("employee_services.employee_table.get_item")
def test_get_employee_by_id_success(mock_get_item):
    mock_get_item.return_value = {
        'Item': {
            'id' : 'Ariful Islam',
            'employee': [
                {"u_id": "EMP001", "name": "Arif", "active": True},
                {"u_id": "EMP002", "name": "Shakil", "active": False}
            ]
        }
    }
    result = employee_services.get_employee_by_id("EMP001")
    assert result == {"u_id": "EMP001", "name": "Arif", "active": True} 

    with pytest.raises(HTTPException) as excinfo:
        employee_services.get_employee_by_id("EMP002")

    assert excinfo.value.status_code == 500
    assert "404: Employee not found" in str(excinfo.value.detail)

@patch("employee_services.employee_table.get_item")
def test_get_employee_by_id_no_employee_list(mock_get_item):
    mock_get_item.return_value = {'Item': {}} # Empty employee list

    with pytest.raises(HTTPException) as excinfo:
        employee_services.get_employee_by_id('EMP002')

    assert excinfo.value.status_code == 500
    assert "404: Employee list not found" in str(excinfo.value.detail)

@patch("employee_services.employee_table.get_item")
def test_get_employee_by_id_exception(mock_get_item):
    mock_get_item.side_effect = Exception("DynamoDB error")

    with pytest.raises(HTTPException) as excinfo:
        employee_services.get_employee_by_id("emp_001")

    assert excinfo.value.status_code == 500
    assert "DynamoDB error" in str(excinfo.value.detail)

################# ADD Employee ##################
    
@patch("employee_services.employee_table.put_item")
@patch("employee_services.employee_table.get_item")
@patch("employee_services.create_unique_id")
def test_add_employee_success(mock_create_id, mock_get_item, mock_put_item):
    mock_create_id.return_value = "emp_123"
    mock_get_item.return_value = {
        'Item': {
            'id' : "Ariful Islam",
            'employee': [
                {"u_id": "emp_001", "name": "Arif", "active": True}
            ]
        }
    }

    input_data = EmployeeInput(name="Shakil")
    result = add_employee(input_data)

    assert result["message"] == "Employee added successfully"
    assert result["u_id"] == "emp_123"
    mock_put_item.assert_called_once()
    saved_employees = mock_put_item.call_args[1]["Item"]["employee"]
    assert any(emp["u_id"] == "emp_123" for emp in saved_employees)


@patch("employee_services.employee_table.put_item")
@patch("employee_services.employee_table.get_item")
@patch("employee_services.create_unique_id")
def test_add_employee_creates_new_record(mock_create_id, mock_get_item, mock_put_item):
    mock_create_id.return_value = "emp_999"
    mock_get_item.return_value = {}  # No existing Item

    input_data = EmployeeInput(name="Rakib")
    result = add_employee(input_data)

    assert result["message"] == "Employee added successfully"
    mock_put_item.assert_called_once()
    saved_item = mock_put_item.call_args[1]["Item"]
    assert saved_item["id"] == "Ariful_Islam"
    assert saved_item["employee"][0]["u_id"] == "emp_999"

def test_add_employee_invalid_name_blank_or_digits():
    with pytest.raises(HTTPException) as excinfo:
        add_employee(EmployeeInput(name=" "))
    assert excinfo.value.status_code == 500
    assert "400: Invalid name: must contain non-digit characters." in excinfo.value.detail

    with pytest.raises(HTTPException) as excinfo:
        add_employee(EmployeeInput(name="12"))
    assert excinfo.value.status_code == 500
    assert "400: Invalid name: must contain non-digit characters." in excinfo.value.detail

@patch("employee_services.employee_table.get_item")
def test_add_employee_internal_error(mock_get_item):
    mock_get_item.side_effect = Exception("DynamoDB is down")

    with pytest.raises(HTTPException) as excinfo:
        add_employee(EmployeeInput(name="Farhan"))

    assert excinfo.value.status_code == 500
    assert "DynamoDB is down" in excinfo.value.detail

    
############### Update Employee #############
@patch("employee_services.employee_table.put_item")
@patch("employee_services.employee_table.get_item")
def test_update_employee_success(mock_get_item, mock_put_item):
    mock_get_item.return_value = {
        'Item': {
            'id' : 'Ariful_Islam',
            'employee': [
                {"u_id": "emp_001", "name": "Arif", "active": True}
            ]
        }
    }

    input_data = employee_services.UpdateEmployeeInput(name="Updated Name")
    result = employee_services.update_employee("emp_001", input_data)

    assert result["message"] == "Employee with u_id emp_001 updated successfully"
    mock_put_item.assert_called_once()
    updated_employees = mock_put_item.call_args[1]["Item"]["employee"]
    assert any(emp["u_id"] == "emp_001" and emp["name"] == "Updated Name" for emp in updated_employees)
 

@patch("employee_services.employee_table.get_item")
def test_update_employee_not_found(mock_get_item):
    mock_get_item.return_value = {
        'Item': {
            'id': 'Ariful_Islam',
            'employee': [
                {"u_id": "emp_002", "name": "Arif", "active": True}
            ]
        }
    }

    input_data = employee_services.UpdateEmployeeInput(name="Shakil")
    with pytest.raises(HTTPException) as excinfo:
        employee_services.update_employee("emp_999", input_data)

    assert excinfo.value.status_code == 500
    assert "404: Employee with u_id emp_999 not found" in excinfo.value.detail

@patch("employee_services.employee_table.get_item")
def test_update_employee_list_missing(mock_get_item):
    mock_get_item.return_value = {
        'Item': {}  # No 'employee' key
    }

    input_data = employee_services.UpdateEmployeeInput(name="Test")
    with pytest.raises(HTTPException) as excinfo:
        employee_services.update_employee("emp_001", input_data)

    assert excinfo.value.status_code == 500
    assert "404: Employee list not found" in excinfo.value.detail


def test_update_employee_invalid_name_blank():

    with pytest.raises(HTTPException) as excinfo:
        employee_services.update_employee("emp_001", employee_services.UpdateEmployeeInput(name="   "))
    assert excinfo.value.status_code == 500
    assert "400: Invalid name: must contain non-digit characters." in excinfo.value.detail

    with pytest.raises(HTTPException) as excinfo:
        employee_services.update_employee("emp_001", employee_services.UpdateEmployeeInput(name="   125"))
    assert excinfo.value.status_code == 500
    assert "400: Invalid name: must contain non-digit characters." in excinfo.value.detail



############### Delete Employee By ID #############
# Successfull deletion and employee not found
@patch("employee_services.employee_table.put_item")
@patch("employee_services.employee_table.get_item")
def test_delete_employee_success(mock_get_item, mock_put_item):
    mock_get_item.return_value = {
        "Item": {
            'id': 'Ariful_Islam',
            "employee": [
                {"u_id": "emp_123", "name": "John", "active": True},
                {"u_id": "emp_456", "name": "Jane", "active": True}
            ]
        }
    }

    result = employee_services.delete_employee_by_id("emp_123")
    
    assert result["message"] == "Employee with u_id emp_123 deleted successfully"
    mock_put_item.assert_called_once()

    updated_employees = mock_put_item.call_args[1]["Item"]["employee"]
    for emp in updated_employees:
        if emp["u_id"] == "emp_123":
            assert not emp["active"]
        else:
            assert emp["active"]
# for employee not found
    with pytest.raises(HTTPException) as excinfo:
        employee_services.delete_employee_by_id("emp_999")
    
    assert excinfo.value.status_code == 500
    assert "405: Employee with id emp_999 not found" in excinfo.value.detail

