## 📚 Flask Books API

A RESTful API built with Flask + flask_smorest, enabling user registration, JWT authentication, and full CRUD operations on books — including file upload & download! Plus, interactive Swagger docs for easy testing.

#### 🚀 Features

* 👤 User registration & authentication with JWT

* 📖 Create, read, update, delete books

* 📂 Upload & download book files securely

* 🔒 Protected endpoints requiring authentication

* 📜 Auto-generated Swagger documentation

*  🐳 Ready for Docker deployment


#### 🛠️ Getting Started
Prerequisites

*   Python 3.7+

*   pip

*   (Optional) Virtual environment

#### Installation
    git clone https://github.com/georgegozal/flask_books_api.git
    cd flask_books_api

    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

    pip install -r requirements.txt

#### Configuration
Edit .env file:

    FLASK_DEBUG=True — uses SQLite (default for dev)

    FLASK_DEBUG=False — configure PostgreSQL vars:
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=books

#### ⚡ Running
Development Server

    python3 main.py


Production Server
gunicorn 
    
    main:app -w 4 --threads 2 -b 0.0.0.0:5000

Access Swagger UI at: [http://localhost:5000](http://localhost:5000)

Redoc: [http://localhost:5000/redoc](http://localhost:5000/redoc)

Rapidoc: [http://localhost:5000/rapidoc](http://localhost:5000/rapidoc)


#### 🔗 API Endpoints
Auth

    POST /auth/register — Register new user

    POST /auth/login — Login and get JWT token

Public

    GET /api/books — List all books (no download links)

    GET /api/books/genre/:genre — Filter by genre

    GET /api/books/author/:author — Filter by author

Protected (JWT required)

    GET /api/books — List books with download URLs

    POST /api/books — Add new book (with file upload)

    PUT /api/books/{id} — Update book

    DELETE /api/books/{id} — Delete book


#### 👨‍💻 Author

[Giorgi Gozalishvili](https://www.linkedin.com/in/giorgi-gozalishvili/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
