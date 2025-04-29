import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import EmployeeServices from '../services/EmployeeServices'

const EditEmployee = () => {
  const { state } = useLocation()
  const emp = state?.emp

  const [name, setName] = useState(emp?.name || '')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const response = await EmployeeServices.updateEmployee(emp.u_id, { name })
      setMessage(`✅ ${response.data.message || 'Employee updated successfully.'}`)
    } catch (error) {
      console.error('❌ Error updating employee:', error)
      setMessage('❌ Failed to update employee')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setName(emp?.name || '')
    setMessage('')
  }

  return (
    <div className="max-w-md mx-auto mt-8 p-4 border rounded shadow bg-white">
      <h2 className="text-2xl font-bold mb-4">Edit Employee</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter employee name"
            className="w-full px-3 py-2 border rounded outline-none focus:ring-2 focus:ring-blue-400"
            required
          />
        </div>

        <div className="flex space-x-4">
          <button
            type="submit"
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            disabled={loading}
          >
            {loading ? 'Updating...' : 'Update'}
          </button>

          <button
            type="button"
            onClick={handleClear}
            className="px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500"
          >
            Reset
          </button>
        </div>
      </form>

      {message && <p className="mt-4 text-center">{message}</p>}
    </div>
  )
}

export default EditEmployee
