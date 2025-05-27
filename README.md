# **Digital Resource Management System (DRMS)**
# ✅ Overview

This is a **full-stack web application** built using **FastAPI** for the backend and **React.js with Tailwind CSS** for the frontend. It integrates **AWS DynamoDB** and **S3** for cloud storage and database operations. The application supports:

- Employee data management
- Image upload with automatic metadata extraction
- Tag- and employee-based image search using **YOLOv8**

---

# 🔧 Tech Stack Used

## 🖥️ Frontend – React.js + Tailwind CSS

- **React Router DOM** – Client-side routing and navigation
- **Axios** – Handling API calls
- **Tailwind CSS** – Utility-first CSS framework for responsive UI
- **React Hooks** – For state management and navigation (`useState`, `useEffect`, `useNavigate`, etc.)

##  Backend – FastAPI

- Lightweight, fast Python framework for building REST APIs
- **Pydantic** for input validation
- CORS middleware enabled for frontend-backend communication

## 🗄️ AWS DynamoDB

- NoSQL database used to store:
  - Employee data
  - Image metadata

## ☁️ AWS S3

- Stores uploaded image files
- Presigned URLs used to securely access files

## 🧠 YOLOv8 (via custom `yolo_api`)

- Used for:
  - Object/tag detection
  - Extracting image dimensions and size

---

# 👤 Employee Services (`employee_services.py`)

- **`create_unique_id()`** – Generates unique employee IDs (e.g., `EMP001`)
- **`add_employee()`** – Validates and adds new employee to DynamoDB
- **`update_employee()`** – Updates employee name by ID
- **`get_employees()`** – Returns all active employees
- **`get_employee_by_id(emp_id)`** – Fetches employee details
- **`delete_employee_by_id(emp_id)`** – Soft-deletes employee (`active: False`)

---

# 🖼️ Image Services (`images_services.py`)

- **`upload_to_s3()`** – Uploads image files to S3 bucket
- **`generate_presigned_url()`** – Generates temporary (5-min) access links
- **`create_unique_img_id()`** – Generates image IDs (e.g., `IMG001`)
- **`add_image_metadata(emp_id, file)`**:
  - Analyzes image with YOLOv8
  - Stores metadata in DynamoDB
  - Uploads image to S3
- **`get_images_info(tags, emp_id)`**:
  - Filters by tags and/or employee ID
  - Returns all images if no filters are provided

---

# 🔁 API Routing (`main.py`)

## 🧑 Employee Routes

| Method | Endpoint                              | Description                     |
|--------|---------------------------------------|---------------------------------|
| POST   | `/employee/add`                       | Add a new employee              |
| PUT    | `/employee/update/{u_id}`             | Update employee name by ID      |
| GET    | `/employees/getEmployees`             | Fetch all active employees      |
| GET    | `/employees/getEmployee/{emp_id}`     | Fetch employee by ID            |
| DELETE | `/employees/delete/{emp_id}`          | Soft delete employee            |

## 🖼️ Image Routes

| Method | Endpoint                                              | Description                               |
|--------|-------------------------------------------------------|-------------------------------------------|
| POST   | `/images/upload/`                                     | Upload image and extract metadata         |
| GET    | `/images/query?tags=tag1,tag2&emp_id=EMP001`          | Search by tags and/or employee ID         |
| GET    | `/images/query`          | If both empty, returns all image metadata |

---

# 🚀 How to Run the Project

## ✅ Environment setup

1. Clone the repo and navigate to backend:
   ```bash
   git clone https://github.com/Ariful-Islam-Shakil/drms-aws-cloud.git

2. setup virtual environment environemt using `python3.12`
    ```bash
      python3.12 -m venv .venv
    ```
3. Activate virtual environment:
    ```bash
    .\.venv\Scripts\activate
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up AWS credentials (via .env or environment variables).
## **Take parallaly two terminals**

### **Terminal-1: Run Backend Server**

- Move current directory to `drms-api`:
    ```bash 
    cd .\drms-api\ 
    ```
- Run the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
    ➡️ The backend will run at: http://127.0.0.1:8000

    ➡️ API Testing with swagger: http://127.0.0.1:8000/docs

## 💻 Frontend (React.js)
1. Navigate to frontend directory:

    ```bash 
    cd .\drms-ui\ 
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Start the development server:
    ```bash
    npm run dev
    ```
    ➡️ The frontend will run at: http://localhost:5173