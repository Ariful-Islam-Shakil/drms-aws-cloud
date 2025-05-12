import pytest
from unittest.mock import patch, MagicMock
from fastapi import UploadFile, HTTPException
from io import BytesIO
from images_services import upload_to_s3, add_image_metadata, get_images_info

# ✅ Dummy UploadFile to simulate FastAPI file upload
class DummyUploadFile:
    def __init__(self, filename, content_type="image/jpeg", content=b"dummy_data"):
        self.filename = filename
        self.content_type = content_type
        self.file = BytesIO(content)

# ✅ Test case: successful upload
@patch("images_services.s3.upload_fileobj")
def test_upload_to_s3_success(mock_upload):
    dummy_file = DummyUploadFile("test.jpg")
    bucket_name = "alpha-ai-new"
    s3_folder = "Ariful_Islam"

    path = upload_to_s3(dummy_file, bucket_name, s3_folder)

    mock_upload.assert_called_once()
    assert path == "Ariful_Islam/test.jpg"


# ❌ Test case: upload failure (e.g., network or auth error)
@patch("images_services.s3.upload_fileobj", side_effect=Exception("S3 Error"))
def test_upload_to_s3_failure(mock_upload):
    dummy_file = DummyUploadFile("test.jpg")
    bucket_name = "alpha-ai-new"
    s3_folder = "Ariful_Islam"

    path = upload_to_s3(dummy_file, bucket_name, s3_folder)

    mock_upload.assert_called_once()
    assert path is None



# 🧪 Dummy UploadFile
class DummyUploadFile:
    def __init__(self, filename="test.jpg", content_type="image/jpeg"):
        self.filename = filename
        self.content_type = content_type
        self.file = BytesIO(b"fake_image_data")

# ✅ Test: Successful metadata addition
@patch("images_services.image_table.put_item")
@patch("images_services.upload_to_s3", return_value="s3://alpha-ai-new/Ariful_Islam/test.jpg")
@patch("images_services.yolo_api.get_image_tags_yolov8_file", return_value=(["person"], "800x600", "2MB"))
@patch("images_services.image_table.get_item")
@patch("images_services.create_unique_img_id", return_value="img_001")
def test_add_image_metadata_success(mock_img_id, mock_get_item, mock_yolo, mock_upload, mock_put_item):
    mock_get_item.return_value = {
        "Item": {
            'id': 'Arifs_Images',
            "images_data": []
        }
    }

    dummy_file = DummyUploadFile()
    result = add_image_metadata("emp_123", dummy_file)

    assert result["message"] == "Image metadata added successfully"
    assert result["img_id"] == "img_001"
    mock_put_item.assert_called_once()


    
# ✅ Test: No existing item (first time metadata)
@patch("images_services.image_table.put_item")
@patch("images_services.upload_to_s3", return_value="s3://alpha-ai-new/Ariful_Islam/test.jpg")
@patch("images_services.yolo_api.get_image_tags_yolov8_file", return_value=(["car"], "1024x768", "1.5MB"))
@patch("images_services.image_table.get_item", return_value={})
@patch("images_services.create_unique_img_id", return_value="img_002")
def test_add_image_metadata_first_entry(mock_img_id, mock_get_item, mock_yolo, mock_upload, mock_put_item):
    dummy_file = DummyUploadFile()
    response = add_image_metadata("emp_456", dummy_file)

    assert response["message"] == "Image metadata added successfully"
    assert response["img_id"] == "img_002"
    item = mock_put_item.call_args[1]["Item"]
    assert item["id"] == "Arifs_images"
    assert len(item["images_data"]) == 1
    assert item["images_data"][0]["emp_id"] == "emp_456"

# ❌ Test: Exception during DB read
@patch("images_services.image_table.get_item", side_effect=Exception("DB Error"))
def test_add_image_metadata_failure(mock_get_item):
    dummy_file = DummyUploadFile()
    with pytest.raises(HTTPException) as exc_info:
        add_image_metadata("emp_789", dummy_file)

    assert exc_info.value.status_code == 500
    assert "DB Error" in exc_info.value.detail

################### Query images #######################
# Dummy image data
mock_image_data = [
    {
        "img_id": "img_001",
        "emp_id": "emp_123",
        "tags": ["Person", "Hat"],
        "s3path": "Ariful_Islam/img1.jpg"
    },
    {
        "img_id": "img_002",
        "emp_id": "emp_456",
        "tags": ["Car"],
        "s3path": "Ariful_Islam/img2.jpg"
    }
]

# ✅ Test: Tags match without emp_id
@patch("images_services.generate_presigned_url", return_value="https://s3-url.com/img1.jpg")
@patch("images_services.image_table.get_item")
def test_get_images_info_by_tags(mock_get_item, mock_presign):
    mock_get_item.return_value = {
        "Item": {"images_data": mock_image_data}
    }

    result = get_images_info(["person"])

    assert len(result["images"]) == 1
    assert result["images"][0]["img_id"] == "img_001"
    assert "download_link" in result["images"][0]


# ✅ Test: Tags match with emp_id
@patch("images_services.generate_presigned_url", return_value="https://s3-url.com/img1.jpg")
@patch("images_services.image_table.get_item")
def test_get_images_info_by_tags_and_emp_id(mock_get_item, mock_presign):
    mock_get_item.return_value = {
        "Item": {"images_data": mock_image_data}
    }

    result = get_images_info(["hat"], emp_id="emp_123")

    assert len(result["images"]) == 1
    assert result["images"][0]["emp_id"] == "emp_123"

# ❌ Test: No tags or emp_id matched
@patch("images_services.image_table.get_item")
def test_get_images_info_no_match(mock_get_item):
    mock_get_item.return_value = {
        "Item": {"images_data": mock_image_data}
    }

    with pytest.raises(HTTPException) as exc_info:
        get_images_info(["dog"])
    
    assert exc_info.value.status_code == 500
    assert "404: Tags or Employee not matched" in str(exc_info.value.detail)


# ❌ Test: No image data found
@patch("images_services.image_table.get_item", return_value={"Item": {}})
def test_get_images_info_no_data(mock_get_item):
    with pytest.raises(HTTPException) as exc_info:
        get_images_info(["car"])
    
    assert exc_info.value.status_code == 500
    assert "404: No images found" in str(exc_info.value.detail)

# ❌ Test: Exception handling (e.g., DB failure)
@patch("images_services.image_table.get_item", side_effect=Exception("DynamoDB error"))
def test_get_images_info_exception(mock_get_item):
    with pytest.raises(HTTPException) as exc_info:
        get_images_info(["car"])
    
    assert exc_info.value.status_code == 500
    assert "DynamoDB error" in str(exc_info.value.detail)