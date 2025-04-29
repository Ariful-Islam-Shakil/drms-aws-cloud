import React, { useState } from 'react'
import EmployeeServices from '../services/EmployeeServices'

const AddEmployee = () => {
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const response = await EmployeeServices.addEmployee({"name" : name})
      setMessage(`✅ ${response.data.message}`)
      setName('')
    } catch (error) {
      console.error('❌ Error adding employee:', error)
      setMessage('❌ Failed to add employee')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setName('')
    setMessage('')
  }

  return (
    <div className="max-w-md mx-auto mt-8 p-4 border rounded shadow bg-white">
      <h2 className="text-2xl font-bold mb-4">Add Employee</h2>

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
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? 'Submitting...' : 'Submit'}
          </button>

          <button
            type="button"
            onClick={handleClear}
            className="px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500"
          >
            Clear
          </button>
        </div>
      </form>

      {message && <p className="mt-4 text-center">{message}</p>}
    </div>
  )
}

export default AddEmployee
