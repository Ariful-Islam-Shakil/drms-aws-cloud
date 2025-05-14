from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
import copy
from io import BytesIO

client = TestClient(app)

demo_image_data_const = {
    'Item': {
        'id': 'Arifs_images',
        'images_data': [
            {
                'img_id': 'IMG001',
                'emp_id': 'EMP001',
                'size': '125 kb',
                'dimension': '32 x 32',
                'created_time': '12:12:2025',
                'tags': ['person', 'cat'],
                's3path': 'Ariful Islam/images1.jpg'
            },
            {
                'img_id': 'IMG002',
                'emp_id': 'EMP005',
                'size': '256 kb',
                'dimension': '64 x 64',
                'created_time': '11:12:2025',
                'tags': ['dog', 'cat'],
                's3path': 'Ariful Islam/images2.jpg'
            }
        ]
    }
}


############## Testing Upload images ####################
@patch('images_services.image_table')
@patch('images_services.upload_to_s3', return_value='Ariful_Islam/image3.jpg')
@patch('yolo_api.get_image_tags_yolov8_file', return_value=(["bird", "cat"], '300x200', '520 kb'))
def test_add_image_metadata(mock_yolo, mock_upload_s3, mock_image_table):
    demo_image_data = copy.deepcopy(demo_image_data_const)
    mock_image_table.get_item.return_value = demo_image_data
    mock_image_table.put_item.return_value = {}

    file = BytesIO(b"fake image bytes")
    file.name = "test.jpg"

    response = client.post(
        "/images/upload/",
        data={"emp_id": "EMP006"},
        files={"file": ("test.jpg", file, "image/jpeg")}
    )

    assert response.status_code == 200
    assert response.json()['message'] == 'Image metadata added successfully'
    assert response.json()['img_id'] == 'IMG003'

    mock_image_table.get_item.return_value = {}
    response = client.post(
        "/images/upload/",
        data={"emp_id": "EMP006"},
        files={"file": ("test.jpg", file, "image/jpeg")}
    )
    assert response.status_code == 200
    assert response.json()['message'] == 'Image metadata added successfully'
    assert response.json()['img_id'] == 'IMG001'

    mock_image_table.get_item.side_effect = Exception("DynamoDB Error")
    response = client.post(
        "/images/upload/",
        data={"emp_id": "EMP006"},
        files={"file": ("test.jpg", file, "image/jpeg")}
    )
    assert response.status_code == 500
    assert response.json()['detail'] == 'DynamoDB Error'
 


############### Testing Query Images ###########################
@patch('images_services.image_table')
@patch('images_services.generate_presigned_url', return_value='http://download/link/image3')
def test_query_image(mock_url, mock_table):
    demo_image_data = copy.deepcopy(demo_image_data_const)
    mock_table.get_item.return_value = demo_image_data
    response = client.get("/images/query", params=[("tags", "cat"), ("tags", "person")])
    assert response.status_code == 200
    assert response.json()['images'] == demo_image_data['Item']['images_data']

    response = client.get("/images/query", params=[("tags", "cat"), ("emp_id", "EMP001")])
    assert response.status_code == 200
    assert response.json()['images'] == [demo_image_data['Item']['images_data'][0]]

    response = client.get("/images/query", params=[("tags", "person"), ("emp_id", "EMP005")])
    assert response.status_code == 500
    assert response.json()['detail'] == '404: Tags or Employee not matched'