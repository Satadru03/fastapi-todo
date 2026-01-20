# FastAPI Todo Service (JWT + PostgreSQL + Docker)

A containerized FastAPI backend with:

- 🔐 JWT Authentication  
- 🗄 PostgreSQL database  
- 🐳 Docker + Docker Compose  
- 👤 User-scoped todos  
- 📄 Automatic Swagger docs (`/docs`)  
- 📝 Request logging middleware  

This project demonstrates a production-style FastAPI architecture suitable for real-world backend applications.

---

## 🛠 Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **JWT (python-jose)**
- **Passlib (bcrypt)**
- **Docker & Docker Compose**
- **Uvicorn**

---

## 🚀 Features

### Users
- `POST /users` — Register user  
- `GET /users` — List all users  
- `GET /user/{username}` — Get single user  
- `PUT /users/{username}` — Update user  
- `DELETE /users/{username}` — Delete user  

### Auth
- `POST /login` — Get JWT access token  

### Todos (protected by JWT)
- `POST /todos` — Create todo  
- `GET /todos` — Get todos for logged-in user  
- `PUT /todos?id={id}` — Update todo  
- `DELETE /todos/{id}` — Delete todo  

---

## 🐳 Run with Docker (recommended)

### 1️⃣ Create `.env`

Create a file named `.env` in the project root:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123@Password
POSTGRES_DB=company_db

DATABASE_URL=postgresql://postgres:123@Password@postgres:5432/company_db
