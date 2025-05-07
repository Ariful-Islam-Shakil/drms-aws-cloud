import React from 'react'
import { useNavigate } from 'react-router-dom'

const NavBar = () => {
    const navigate = useNavigate();
  return (
    <nav className="bg-gray-800 text-white shadow-md sticky top-0 z-50">
    <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
      {/* Left: Brand */}
      <div className="text-xl font-bold">
        Digital Resource Management
      </div>

      {/* Right: Navigation Links */}
      <div className="flex space-x-4">
        <button
          onClick={() => navigate('/')}
          className="hover:text-blue-400 transition"
        >
          🏠 Home
        </button>
        <button
          onClick={() => navigate('/add-employee')}
          className="hover:text-blue-400 transition"
        >
          ➕ Add Employee
        </button>
        <button
          onClick={() => navigate('/view-employees')}
          className="hover:text-green-400 transition"
        >
          👀 View Employees
        </button>
        <button
          onClick={() => navigate('/uploadImage')}
          className="hover:text-red-400 transition"
        >
          📤 Upload Images
        </button>
        <button
          onClick={() => navigate('/queryImages')}
          className="hover:text-purple-400 transition"
        >
          ❓ Queries
        </button>
      </div>
    </div>
  </nav>
  )
}

export default NavBar