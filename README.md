# 💖  - Backend API

FastAPI-based backend for the **Stellar Spark Match** dating application.
Handles authentication, profiles, messaging, media, and real-time communication.

---

## 🚀 Tech Stack

* **Backend:** Python, FastAPI
* **Database:** PostgreSQL
* **ORM / Migrations:** Prisma (optional)
* **Authentication:** JWT
* **Server:** Uvicorn

---

## 📁 Project Structure

```
backend/
│
├── python/              # FastAPI application
│   ├── main.py
│   ├── routes/
│   ├── models/
│   └── core/
│
├── prisma/              # Prisma schema & migrations (optional)
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Prerequisites

* Python **3.10+**
* PostgreSQL **14+**
* Node.js (for Prisma, optional)

---

### 2. Clone Repository

```bash
git clone https://github.com/tarun08pareta/JODI_BACKEND.git
cd JODI_BACKEND/backend/python
```

---

### 3. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Environment Variables

```bash
cp .env.example .env
```

Update `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/stellar_spark
JWT_SECRET=your_secret_key
PORT=8000
```

---

### 6. Database Setup

#### Option A: Manual PostgreSQL

```bash
createdb stellar_spark
```

---

#### Option B: Using Prisma (Recommended)

```bash
cd ../prisma

npx prisma migrate dev --name init
npx prisma generate
```

---

## ▶️ Run FastAPI Server

```bash
cd ../python

uvicorn main:app --reload
```

### 🌐 Server URLs

* API Base: http://localhost:8000
* Swagger Docs: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

---

## 📦 API Modules

### 🔐 Authentication

* `POST /api/auth/register`
* `POST /api/auth/login`
* `GET /api/auth/me`
* `POST /api/auth/logout`

---

### 👤 Profiles

* `GET /api/profiles/`
* `GET /api/profiles/{user_id}`
* `GET /api/profiles/me/profile`
* `PUT /api/profiles/me/profile`

---

### 🖼️ Gallery

* `GET /api/gallery/?user_id={id}`
* `POST /api/gallery/`
* `DELETE /api/gallery/{id}`

---

### 💬 Messaging

* `GET /api/messages/`
* `GET /api/messages/conversation/{partner_id}`
* `POST /api/messages/`
* `PUT /api/messages/{id}/read`

---

### 📞 Calls (WebRTC)

* `GET /api/calls/signals`
* `POST /api/calls/signals`
* `DELETE /api/calls/signals/{room_id}`
* `GET /api/calls/messages/{room_id}`
* `POST /api/calls/messages`

---

## 🧪 Running Tests

```bash
# (Add your test framework here)
pytest
```

---

## 🔐 Security Notes

* Never commit `.env`
* Use `.env.example` for sharing config
* Keep secrets (JWT, DB credentials) secure

---

## 📌 Development Tips

* Use `--reload` only in development
* Use proper logging in production
* Add rate limiting for auth APIs
* Use Docker for deployment (recommended)

---

## 🚀 Future Improvements

* WebSocket support for real-time chat
* Notification system
* Matching algorithm
* Media storage (S3 / Cloudinary)
* CI/CD pipeline

---

## 👨‍💻 Author

**Tarun Pareta**

---

## 📄 License

This project is licensed under the MIT License.
