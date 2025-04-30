import React, { useEffect, useState } from 'react'
import EmployeeServices from '../services/EmployeeServices'
import { useNavigate } from 'react-router-dom'

const ViewEmployees = () => {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const response = await EmployeeServices.getEmployees()
        setEmployees(response.data.employees || [])
      } catch (error) {
        console.error('Failed to fetch employees:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchEmployees()
  }, [])

  const handleDelete = (e,empId) => {

    e.preventDefault();
    EmployeeServices.deleteEmployeeById(empId)
    .then((res)=>{
        if(employees){
            setEmployees((prevElement)=>{
                return prevElement.filter((emp)=> emp.u_id !== empId);
            });
        }
    });
};


  return (
    <div className="p-8 max-w-5xl mx-auto">
      <h2 className="text-3xl font-bold text-center mb-6 text-blue-700">Employee List</h2>

      {loading ? (
        <p className="text-center">Loading...</p>
      ) : employees.length === 0 ? (
        <p className="text-center text-gray-500">No employees found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-200 shadow rounded-lg">
            <thead className="bg-blue-500 text-white">
              <tr>
                <th className="py-3 px-6 text-left">Employee ID</th>
                <th className="py-3 px-6 text-left">Name</th>
                <th className="py-3 px-6 text-left">Created Time</th>
                <th className="py-3 px-6 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((emp, index) => (
                <tr key={emp.u_id} className="border-b hover:bg-gray-100">
                  <td className="py-3 px-6 text-left">{emp.u_id}</td>
                  <td className="py-3 px-6 text-left">{emp.name}</td>
                  <td className="py-3 px-6">{new Date(emp.created_time).toLocaleString()}</td>
                  <td className="py-3 px-6 flex gap-2">
                    <button
                      onClick={() => navigate('/editEmployee', { state: { emp } })}
                      className="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600"
                    >
                      Edit
                    </button>
                    <button
                      onClick={(e, empId) => handleDelete(e, emp.u_id)}
                      className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default ViewEmployees
