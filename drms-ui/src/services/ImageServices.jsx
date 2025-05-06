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

    queryImages(tags, emp_id){
        const params = new URLSearchParams();
        tags.forEach(tag => {params.append('tags', tag)});
        if (emp_id){params.append('emp_id', emp_id)};
        return axios.get(API_BASE_URL + '/query', {params})
    }
}

export default new ImageServices()
