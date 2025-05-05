import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:8000/images';

class ImageServices {
    uploadImage(emp_id, file){
        const formData = new FormData();
        formData.append('emp_id', emp_id);
        formData.append('file', file);
        return axios.post(API_BASE_URL + '/upload/', formData,{
            headers: {
                'Content-Type':'multipart/form-data'
            }
        })
    }
}

export default new ImageServices()
