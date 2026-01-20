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
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=your_database_name

DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
```

> Note: Inside Docker, the host is `postgres`, not `localhost`.

---

### 2️⃣ Start everything

```bash
docker compose up --build
```

Then open:

```
http://localhost:8000/docs
```

---

## 🔐 How to authenticate (Swagger)

1. Go to `/docs`
2. Call `POST /login`
3. Copy the `access_token`
4. Click **Authorize (🔐)**
5. Paste:

```
Bearer <your-token>
```

6. Now you can use all `/todos` endpoints.

---

## 📁 Project Structure

```
fastapi-todo/
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── crud.py
│   ├── schema.py
│   ├── auth.py
│   └── logging_config.py
├── docker-compose.yml
├── Dockerfile
├── .env
├── requirements.txt
└── README.md
```

---

## 🎯 What I learned building this

* Designing REST APIs with FastAPI
* Securing endpoints using JWT
* Working with PostgreSQL via SQLAlchemy
* Containerizing apps with Docker Compose
* Writing middleware for logging

---

## 📜 License

```
MIT License.
```

---
