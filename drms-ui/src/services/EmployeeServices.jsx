import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000';

class EmployeeService {

    addEmployee(name){
        return axios.post(API_BASE_URL + '/employee/add', name);
    }

    updateEmployee(u_id, updatedFields){
      return axios.put(API_BASE_URL + '/employee/update/' + u_id, updatedFields);
    }
    getEmployees(){
      return axios.get(API_BASE_URL + '/employees/getEmployees');
    }
    getEmployeeById(u_id){
      return axios.get(API_BASE_URL + '/employees/getEmployee/' + u_id)
    }
}

export default new EmployeeService()
