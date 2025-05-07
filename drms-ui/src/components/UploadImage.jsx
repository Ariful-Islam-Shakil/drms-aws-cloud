import React, { useEffect, useState } from 'react'; 
import EmployeeServices from '../services/EmployeeServices';
import ImageServices from '../services/ImageServices';

const UploadImage = () => {
  const [employees, setEmployees] = useState([]);
  const [selectedEmp, setSelectedEmp] = useState(null);
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [responseMsg, setResponseMsg] = useState('');

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

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handleUpload = async () => {
    if (!selectedEmp || !image) return;
    setLoading(true);
    setResponseMsg('');
    try {
      const res = await ImageServices.uploadImage(selectedEmp.u_id, image);
      setResponseMsg(res.message || '✅ Uploaded successfully!');
    } catch (error) {
      setResponseMsg('❌ Upload failed.');
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div className="bg-gray-700 text-white min-h-screen py-12 px-6 md:px-20">

    <div className="p-6 max-w-3xl mx-auto bg-gray-700 rounded-xl shadow-md space-y-6">
      <h2 className="text-2xl font-bold text-center text-shadow-white">Upload Employee Image</h2>

      <div className="space-y-4">
        <label className="block text-white font-medium">Select Employee:</label>
        <select
          onChange={(e) =>
            setSelectedEmp(employees.find((emp) => emp.u_id === e.target.value))
          }
          className="w-full p-2 border border-gray-300 rounded-md"
          >
          <option value=""
            className='bg-gray-400 text-white'
          >-- Choose Employee --</option>
          {employees.map((emp) => (
            <option
              className='bg-gray-400 text-white'
            key={emp.u_id} value={emp.u_id}>
              {emp.u_id} - {emp.name}
            </option>
          ))}
        </select>
      </div>

      <div className="space-y-4">
        <label className="block text-gray-700 font-medium">Select Image:</label>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="w-full p-2 border border-gray-300 rounded-md"
          />

        {previewUrl && (
          <img
          src={previewUrl}
          alt="Preview"
            className="max-w-xs mx-auto rounded shadow"
          />
        )}
      </div>

      <div className="flex justify-center">
        <button
          onClick={handleUpload}
          disabled={loading || !image || !selectedEmp}
          className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
          >
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </div>

      {responseMsg && (
        <p className="text-center font-medium text-green-600">{responseMsg}</p>
      )}
    </div>
    </div> 
  );
};

export default UploadImage;
