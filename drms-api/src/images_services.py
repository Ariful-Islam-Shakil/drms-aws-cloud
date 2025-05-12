# images_service.py
from fastapi import HTTPException, FastAPI, UploadFile, File 
from datetime import datetime
from zoneinfo import ZoneInfo
import boto3, yolo_api
from datetime import timezone, timedelta
from typing import List, Optional

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
image_table = dynamodb.Table('team-alpha-ai')  # Update table name if different
s3 = boto3.client('s3')

#Upload image to s3 folder
def upload_to_s3(file: UploadFile, bucket_name: str, s3_folder_path: str):
    try:
        fileName = file.filename
        s3_path = f"{s3_folder_path}/{fileName}"
        
        # Get content type from UploadFile (FastAPI's UploadFile has it)
        content_type = file.content_type or 'application/octet-stream'
        file.file.seek(0)

        s3.upload_fileobj(
            file.file,
            bucket_name,
            s3_path,
            ExtraArgs={'ContentType': content_type}
        )

        print(f"✅ File uploaded successfully to {bucket_name}/{s3_path}")
        return s3_path #, generate_presigned_url(bucket_name, s3_path)
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

# Generate image url for downloading image
def generate_presigned_url(bucket_name: str, s3_path: str, expiration: int = 300):
    try:
        url = s3.generate_presigned_url (
            'get_object',
            Params={'Bucket': bucket_name, 'Key':s3_path},
            ExpiresIn = expiration
        )
        return url
    except Exception as e:
        print(f"❌ Failed to generate presigned URL: {e}")
        return None


# Utility to generate unique image ID
def create_unique_img_id(images):
    if not images:
        return 'IMG001'

    images.sort(key=lambda x: int(''.join(filter(str.isdigit, x['img_id']))))
    last_id = images[-1]['img_id']
    prefix = ''.join(filter(str.isalpha, last_id))
    number = ''.join(filter(str.isdigit, last_id))
    new_number = str(int(number) + 1).zfill(len(number))
    return prefix + new_number


# ✅ Add Image Metadata
def add_image_metadata(emp_id: str, file: UploadFile):
    try:
        # created_time = datetime.now(ZoneInfo("Asia/Dhaka")).isoformat()
        created_time = datetime.now(timezone(timedelta(hours=6))).isoformat()

        response = image_table.get_item(Key={'id': 'Arifs_images'})
        item = response.get('Item')

        images = item.get('images_data', []) if item and 'images_data' in item else []
        img_id = create_unique_img_id(images)
        tags, dimension, size = yolo_api.get_image_tags_yolov8_file(file)
        s3_path = upload_to_s3(file, 'alpha-ai-new', 'Ariful_Islam')

        new_image = {
            'img_id': img_id,
            'emp_id': emp_id,
            'size': size,
            'dimension': dimension,
            'created_time': created_time,
            'tags': tags,
            's3path': s3_path
        }

        if item and 'images_data' in item:
            item['images_data'].append(new_image)
        else:
            item = {
                'id': 'Arifs_images',
                'images_data': [new_image]
            }

        image_table.put_item(Item = item)

        return {"message": "Image metadata added successfully", "img_id": img_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


 # Query images information
def get_images_info(tags: list[str], emp_id: Optional[str] = None):
    try:
        response = image_table.get_item(Key={'id':'Arifs_images'})
        item = response.get('Item')
        if not item or 'images_data' not in item:
            raise HTTPException(status_code=404, detail='No images found')
        output_images = []
        tags = set(x.lower() for x in tags)
        for img in item['images_data']:
            db_tags = set(x.lower() for x in img.get('tags', []))
            if db_tags & tags:
                if emp_id:
                    if emp_id == img.get('emp_id'):
                        img['download_link'] = generate_presigned_url('alpha-ai-new', img.get('s3path'))
                        output_images.append(img)
                else:
                    img['download_link'] = generate_presigned_url('alpha-ai-new', img.get('s3path'))
                    output_images.append(img)
        if output_images:
            return {'images': output_images}
        else:
            raise HTTPException(status_code=404, detail='Tags or Employee not matched')

    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))
       
 