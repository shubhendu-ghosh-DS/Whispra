# Whispra - Backend Chat API

Whispra is a lightweight, containerized backend chat API built with **FastAPI** and deployed on **Hugging Face Spaces**. It powers the core functionality of a secure and minimalistic messaging platform. Whispra handles user authentication, message passing, and friend management, and is designed to serve as the backend for any frontend interface or service integration.

---

## 🌐 Live Demo

Access the live API here:  
🔗 [https://shubhendu-ghosh-whispra.hf.space](https://shubhendu-ghosh-whispra.hf.space)

---

## 📁 Project Structure

```
.
├── Dockerfile
├── requirements.txt
└── app
    ├── api.py              # Defines API endpoints
    ├── config.py           # Configuration (e.g., DB credentials)
    ├── crud.py             # Database operations
    ├── database.py         # MongoDB client setup
    ├── main.py             # Application entry point
    ├── models.py           # Pydantic models (schemas)
```

---

## 🚀 Features

- **User Registration & Login**
- **Account Activation Check**
- **Send & Scan Messages**
- **Save & Retrieve Friend Usernames**
- **Password Authentication with Bcrypt**
- **MongoDB Integration**
- **Dockerized & Easily Deployable**

---

## 🔐 API Endpoints

### Root

- `GET /`  
  Health check for the API.

---

### Authentication

- `POST /signup`  
  Registers a new user. Requires:
  - `username`
  - `email`
  - `password`

- `POST /login`  
  Authenticates a user and checks account activation.

---

### Messaging

- `POST /send_message`  
  Sends a message from one user to another.

- `POST /scan_messages`  
  Retrieves and deletes unread messages for a user.

---

### Friends Management

- `POST /save_friends`  
  Saves a friend username to the user's list.

- `GET /get_friends?username=<>&password=<>`  
  Returns a list of saved friends for the user.

---

## ⚙️ Tech Stack

- **FastAPI** - Web Framework  
- **MongoDB** - Database  
- **Pydantic** - Data validation  
- **Uvicorn** - ASGI server  
- **Docker** - Containerization  
- **Hugging Face Spaces** - Deployment

---

## 🛠 Installation & Local Development

### Prerequisites

- Python 3.8+
- Docker (optional for containerized runs)
- MongoDB instance (local or cloud)

### Clone the Repo

```bash
git clone https://github.com/yourusername/whispra.git
cd whispra
```

### Run Locally (Without Docker)

1. Create a virtual environment and install dependencies:

```bash
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Set your MongoDB URI in `config.py` or use `.env`

3. Run the app:

```bash
uvicorn app.main:app --reload
```

---

### Run with Docker

```bash
docker build -t whispra .
docker run -p 8000:8000 whispra
```

---

## 👤 Author

**Shubhendu Ghosh**  
🔗 [LinkedIn](https://www.linkedin.com/in/shubhendu-ghosh-ds/)

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgments

- Inspired by simple, secure messaging systems.
- Built using FastAPI for rapid development.
