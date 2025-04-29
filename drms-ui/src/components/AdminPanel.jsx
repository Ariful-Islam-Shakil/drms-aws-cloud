import React from 'react'
import { useNavigate } from 'react-router-dom'

const AdminPanel = () => {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="bg-white shadow-xl rounded-2xl p-8 max-w-md w-full text-center">
        <h1 className="text-3xl font-bold text-blue-600 mb-6">Admin Panel</h1>

        <div className="space-y-4">
          <button
            onClick={() => navigate('/add-employee')}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 rounded-lg transition duration-300"
          >
            ➕ Add Employee
          </button>

          <button
            onClick={() => navigate('/view-employees')}
            className="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-lg transition duration-300"
          >
            👀 View Employees
          </button>

          <button
            onClick={() => navigate('/queries')}
            className="w-full bg-purple-500 hover:bg-purple-600 text-white font-semibold py-3 rounded-lg transition duration-300"
          >
            ❓ Queries
          </button>
        </div>
      </div>
    </div>
  )
}

export default AdminPanel
