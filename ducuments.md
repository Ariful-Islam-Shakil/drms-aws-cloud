# ✅ Overview
This is a FastAPI-based backend project integrated with AWS services (DynamoDB and S3). It provides RESTful APIs for:

- Managing employee data.

- Uploading images with metadata.

- Tag-based image search using YOLOv8.

# 🔧 Tech Stack Used
## 🐍 FastAPI
- Framework for building RESTful APIs.

- Provides built-in validation with Pydantic models.

- Easy integration with file upload, CORS, etc.

## 📦 Pydantic
Used for input validation via BaseModel classes like EmployeeInput and UpdateEmployeeInput.

## 🌐 CORS Middleware
Enabled with:
```python
app.add_middleware(CORSMiddleware, allow_origins=[...])
```
- Allows requests from your frontend (e.g., `http://localhost:5173`) to access the backend.

## 🗄️ AWS DynamoDB
- NoSQL database used for storing both:

  - Employee records.

  - Image metadata.

- You fetch and modify items using `get_item`, `put_item`.

## ☁️ AWS S3
- Used to store image files.

- Files are uploaded using `upload_fileobj`.

- You generate temporary access URLs via presigned URLs.

## 🧠 YOLOv8 (via `yolo_api`)
- A custom module you created (not shown here) that detects:

  - Tags.

  - Dimensions.

  - Size of uploaded images.

# 🧑 Employee Services (`employee_services.py`)
### 🔨 `create_unique_id()`
Generates new employee IDs like `EMP001` , `EMP002`, etc.

- Ensures uniqueness by scanning existing IDs and incrementing the last one.

### ✅ add_employee()
- Validates name (non-empty, not all digits).

- Generates `u_id`, adds timestamp (`Asia/Dhaka`), and appends to `DynamoDB` under `id = Ariful_Islam`.

### ✏️ `update_employee()`
- Updates name of an employee if u_id exists.

### 📄 `get_employees()`
- Fetches only active employees.

### 🔍 `get_employee_by_id(emp_id)`
- Fetches one employee by u_id.

### ❌ `delete_employee_by_id(emp_id)`
- Performs soft delete (sets "active": False) instead of physically removing the employee.

# 🖼️ Image Services (`images_services.py`)
### 📁 `upload_to_s3()`
- Uploads UploadFile to a specific S3 folder.

- Automatically handles content-type and full file upload.

### 🔗 `generate_presigned_url()`
- Creates a temporary URL (valid for 5 mins) for downloading files.

### 🆔 `create_unique_img_id()`
- Like employee IDs, generates unique `IMG001`, `IMG002`... image IDs.

### 📤 `add_image_metadata(emp_id, file)`
- Gets image metadata (tags, size, dimension) from YOLO.

- Uploads the image to `S3`.

- Adds metadata to DynamoDB under `id = Arifs_images`.

### 🔎 `get_images_info(tags, emp_id)`
- Filters images that:

  - Match at least one given tag.

  - Optionally match a given employee ID.

- Returns image metadata + download link.

# 🔁 Main App Routing (`main2.py`)

### 🧑 Employee Routes

- `POST /employee/add`  
  ➤ Add a new employee.

- `PUT /employee/update/{u_id}`  
  ➤ Update employee name by unique ID.

- `GET /employees/getEmployees`  
  ➤ Retrieve all active employees.

- `GET /employees/getEmployee/{emp_id}`  
  ➤ Get employee details by ID.

- `DELETE /employees/delete/{emp_id}`  
  ➤ Soft delete an employee (mark as inactive).

---

### 🖼️ Image Routes

- `POST /images/upload/`  
  ➤ Upload an image and analyze metadata (tags, dimensions, size) using YOLOv8.

- `GET /images/query?tags=tag1,tag2&emp_id=EMP001`  
  ➤ Filter images by tags and/or employee ID.
