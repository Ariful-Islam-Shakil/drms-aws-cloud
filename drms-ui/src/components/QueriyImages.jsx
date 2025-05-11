import React, { useEffect, useState } from 'react';
import EmployeeServices from '../services/EmployeeServices';
import ImageServices from '../services/ImageServices';

const QueriyImages = () => {
  const [tags, setTags] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [selectEmployee, setSelectEmployee] = useState(null);
  const [searching, setSearching] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const response = await EmployeeServices.getEmployees();
        setEmployees(response.data.employees || []);
      } catch (error) {
        console.error('Failed to fetch Employees: ', error);
      }
    };
    fetchEmployees();
  }, []);

  const handleSearch = async () => {
    setSearching(true);
    setError('');
    setResults([]);
    try {
      const response = await ImageServices.queryImages(tags, selectEmployee?.u_id);
      setResults(response.data.images || []);
    } catch (error) {
      console.error(error);
      setError(error.response?.data?.detail || 'Failed to fetch images.');
    }
    setSearching(false);
  };

  return (
    <div className="bg-gray-700 text-white min-h-screen py-12 px-6 md:px-20">
    <div className="max-w-4xl mx-auto p-6 bg-gray-700 shadow-lg rounded-lg mt-6">
      <h2 className="text-2xl font-bold mb-4 text-center text-shadow-fuchsia-200">Query Images</h2>

      <div className="space-y-4">
        <div>
          <label className="block font-medium text-white mb-1">Enter Tags (comma separated)</label>
          <input
            type="text"
            name="tags"
            onChange={(e) =>
              setTags(
                e.target.value
                  .split(/[,\.\-_ ]+/)
                  .map(tag => tag.trim())
                  .filter(tag => tag !== '')
              )
            }
            placeholder="e.g. person,dog,cat"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-400 outline-none"
          />
        </div>

        <div>
          <label className="block font-medium text-gray-700 mb-1">Select Employee (Optional)</label>
          <select
            onChange={(e) =>
              setSelectEmployee(employees.find((emp) => emp.u_id === e.target.value))
            }
            className="w-full p-2 border border-gray-300 rounded-md"
          >
            <option value="" className='bg-gray-400 text-white'>-- Choose Employee --</option>
            {employees.map((emp) => (
              <option 
              className='bg-gray-400 text-white'
              key={emp.u_id} value={emp.u_id}>
                {emp.u_id} - {emp.name}
              </option>
            ))}
          </select>
        </div>

        <div className="flex justify-center">
          <button
            onClick={handleSearch}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
            disabled={searching || tags.length === 0}
          >
            {searching ? 'Searching...' : 'Search'}
          </button>
        </div>

        {error && (
          <div className="text-red-600 text-center mt-2">
            ⚠ {error}
          </div>
        )}
      </div>

      <div className="mt-8">
        <h3 className="text-xl font-semibold text-white mb-3">Query Results</h3>
        {results.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {results.map((img, index) => (
              <div key={index} className="border rounded-lg p-4 shadow-sm hover:shadow-md transition">
                <img
                  src={img.download_link || 'https://via.placeholder.com/150'}
                  alt={img.name || 'Image'}
                  className="w-full h-40 object-cover rounded-md mb-2"
                />
                <p className="text-gray-300"><strong>Image Id: </strong> {img.img_id}</p>
                <p className="text-gray-300"><strong>Employee ID:</strong> {img.emp_id}</p>
                <p className="text-gray-300"><strong>Tags:</strong> {img.tags?.join(', ')}</p>
                <p className="text-gray-300"><strong>Size:</strong> {img.size} KB - {img.dimension}</p>
              </div>
            ))}
          </div>
        ) : (
          !searching && <p className="text-gray-500 text-center">No images to display.</p>
        )}
      </div>
    </div>
    </div>
  );
};

export default QueriyImages;
