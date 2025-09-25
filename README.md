# Mini Blog API (Tier 1 — In-Memory)

## 📌 Setup Instructions

### 1. Create & activate virtual environment
- **Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```
or
```powershell
.venv\Scripts\activate
```

- **Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install django djangorestframework
```

### 3. Run the development server
```bash
python manage.py runserver
```

---

## 📌 Example Requests & Responses

### 1. List Posts (Initially Empty)
**Request:**
```
GET http://127.0.0.1:8000/api/posts/
```
**Response:**
```json
[]
```

---

### 2. Create Post (Authentication Required)
**Request:**
```
POST http://127.0.0.1:8000/api/posts/
Headers:
  Authorization: Token abc123
  Content-Type: application/json

Body:
{
  "title": "Introduction to Mini Blog",
  "content": "This is the first test post to verify the API functionality."
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Introduction to Mini Blog",
  "content": "This is the first test post to verify the API functionality.",
  "author": 1,
  "created_at": "2025-09-24T18:27:35.071049Z"
}
```

**Unauthorized Example:**
```json
{
  "detail": "Authentication required"
}
```
Status: `401 Unauthorized`

---

### 3. Add Comment to a Post (Authentication Required)
**Request:**
```
POST http://127.0.0.1:8000/api/posts/3/comments/
Headers:
  Authorization: Token abc123
  Content-Type: application/json

Body:
{
  "text": "Nice post!"
}
```

**Response:**
```json
{
  "id": 1,
  "post": 3,
  "text": "Nice post!",
  "author": 1,
  "created_at": "2025-09-24T18:32:03.841280Z"
}
```

---

### 4. List All Posts (Latest-First)
**Request:**
```
GET http://127.0.0.1:8000/api/posts/
```
**Response:**
```json
[
  {
    "id": 6,
    "title": "Final Post",
    "content": "Final post to check that latest posts appear first and pagination works.",
    "author": 1,
    "created_at": "2025-09-24T18:29:13.167681Z"
  },
  {
    "id": 5,
    "title": "Pagination Test",
    "content": "We are now testing pagination using multiple posts.",
    "author": 1,
    "created_at": "2025-09-24T18:29:04.241767Z"
  }
]
```

---

### 5. Get Single Post with Comments
**Request:**
```
GET http://127.0.0.1:8000/api/posts/3/
```
**Response:**
```json
{
  "id": 3,
  "title": "API Authentication",
  "content": "Checking that unauthorized requests fail and authorized requests succeed.",
  "author": 1,
  "created_at": "2025-09-24T18:28:45.378235Z",
  "comments": [
    {
      "id": 1,
      "post": 3,
      "text": "Nice post!",
      "author": 1,
      "created_at": "2025-09-24T18:32:03.841280Z"
    }
  ]
}
```

---

### 6. Pagination Example
**Request:**
```
GET http://127.0.0.1:8000/api/posts/?page=1&page_size=5
```
**Response:**
```json
[
  {
    "id": 6,
    "title": "Final Post",
    "content": "Final post to check that latest posts appear first and pagination works.",
    "author": 1,
    "created_at": "2025-09-24T18:29:13.167681Z"
  },
  {
    "id": 5,
    "title": "Pagination Test",
    "content": "We are now testing pagination using multiple posts.",
    "author": 1,
    "created_at": "2025-09-24T18:29:04.241767Z"
  }
]
```

---

### 7. Input Validation (Empty Title)
**Request:**
```
POST http://127.0.0.1:8000/api/posts/
Headers:
  Authorization: Token abc123
  Content-Type: application/json

Body:
{
  "title": "",
  "content": "Hello world!"
}
```

**Response:**
```json
{"title":"Title is required."}
```

---

### 8. Input Validation (Empty Content)
**Request:**
```
POST http://127.0.0.1:8000/api/posts/
Headers:
  Authorization: Token abc123
  Content-Type: application/json

Body:
{
  "title": "Shubham Vharamble",
  "content": ""
}
```

**Response:**
```json
{"content":"Content is required."}
```

---

## ✅ Features Implemented
- Input validation (title & content required, non-empty).
- Authentication with token (`abc123`).
- Posts ordered latest first.
- Pagination (`?page=1&page_size=5`).
- Comment system.
- Clean, readable code with comments.





#####         ############        ##########        ############            ############






## Optional Bonus

- Replace in-memory storage with SQLite/MySQL using Django ORM.

Migrations:
1) python manage.py makemigrations
2) python manage.py migrate

## Setup
1. Install SimpleJWT
```
pip install djangorestframework-simplejwt
```

## Update settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}



## Create a superuser (to log in and get tokens)
```
python manage.py createsuperuser
```
# so you can easily manage posts, comments



## Run the development server
python manage.py runserver

Server will start:
http://127.0.0.1:8000/


## Get JWT tokens
POST → http://127.0.0.1:8000/api/token/
Body → JSON:

{
  "username": "shubham",
  "password": "ccqpv7755r"
}

You’ll receive:

{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1ODg1OTczNSwiaWF0IjoxNzU4NzczMzM1LCJqdGkiOiJiMzViMTE4YjdhMjE0ZTllYTIzMWZkMjVhYmVlOTY0MCIsInVzZXJfaWQiOiIxIn0.R3vWnRmDL-VqF8_q3iOvb9hOL9NDMUnCJQEqEyVHGpI","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4Nzc1MTM1LCJpYXQiOjE3NTg3NzMzMzUsImp0aSI6IjQ2NGViMjNhYjBhZDQzNzZiODI1ZGQ2YjE0ZGFlMTIzIiwidXNlcl9pZCI6IjEifQ.KzaiIU-sFIWkh976WyRhajbh-nVRzbtQ3V2j-OyUVO0"}



## We can use JWT access token in headers
For all protected requests (POST /api/posts/, POST /api/posts/<id>/comments/)

Headers →

Authorization: Bearer <access_token>




## Refresh token

POST http://127.0.0.1:8000/api/token/refresh/
Body → JSON:

{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1ODg1OTczNSwiaWF0IjoxNzU4NzczMzM1LCJqdGkiOiJiMzViMTE4YjdhMjE0ZTllYTIzMWZkMjVhYmVlOTY0MCIsInVzZXJfaWQiOiIxIn0.R3vWnRmDL-VqF8_q3iOvb9hOL9NDMUnCJQEqEyVHGpI"
}

You will receive:
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4Nzc4MjI4LCJpYXQiOjE3NTg3NzY0MjgsImp0aSI6IjEzNGEyODlmZGFmYTQ3ZjE5ZGQwNTVkYzA2NjdhMDBhIiwidXNlcl9pZCI6IjEifQ.q0x1W5OAfbWmpKv4pqbsXvvIUawxXSeDe1GlG70EX14"
}


## Create Post

POST http://127.0.0.1:8000/api/posts/
Body → JSON:
{
  "title": "My First Post",
  "content": "This is the content of my first post."
}

You will receive:
{"id":1,"title":"My First Post","content":"This is the content of my first post.","author":"shubham","created_at":"2025-09-25T05:03:30.483508Z","comments":[]}




## GET/PUT(UPDATE)/DELETE Single post detail
1. PUT http://127.0.0.1:8000/api/posts/1/
Body → JSON:
{
  "title": "Updated Blog Title",
  "content": "This is the updated content of the blog post."
}

You will get:
{"id":1,"title":"Updated Blog Title","content":"This is the updated content of the blog post.","author":"shubham","created_at":"2025-09-25T05:03:30.483508Z","comments":[]}


2. DELETE http://127.0.0.1:8000/api/posts/1/


## PUT(UPDATE)/DELETE Single comment detail

1. PUT http://127.0.0.1:8000/api/comments/2/
Body → JSON:
{
  "text": "Updated Comment Text"
}

You will get:
{"id":2,"text":"Updated Comment Text","created_at":"2025-09-25T15:41:06.689277Z"}

2. DELETE http://127.0.0.1:8000/api/comments/1/



## All the example screenshots are available in the assets/screenshots & assets/sqlite-ss folders.