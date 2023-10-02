## Flask Books API
The Flask Books API is a RESTful web service built using Flask, allowing users to register, authenticate, and manage their books. Authenticated users can add, delete, update books and access download URL

### Features
  * User registration and authentication.
  * Create, read, update, and delete (CRUD) operations for books.
  * Secure endpoints with JSON Web Tokens (JWT) for authentication.
  * Generate download URLs for books (authenticated users only).
 

### Getting Started
Follow these steps to get the Flask Books API up and running on your local machine:

#### Prerequisites
 * Python 3.7+
 * pip
 * Virtual environment (optional but recommended)

### Installation
1. Clone the repository:
    ```
    git clone https://github.com/georgegozal/flask_books_api.git
    
    cd flask_books_api

2. Create a virtual environment (optional but recommended):
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    ```
    pip install -r requirements.txt

## Configuration
 Change a .env file in the project root directory  with the following variables:

 The application can be configured using the following environment variables:

- `FLASK_DEBUG`: Set this variable to `False` for production. If `True`, SQLite3 will be used as the database, and other PostgreSQL variables are not required.

If `FLASK_DEBUG` is set to `True`, the application will use SQLite3. No additional PostgreSQL variables are needed.

If `FLASK_DEBUG` is set to `False`, you must configure the following PostgreSQL variables:

 
* POSTGRES_HOST=localhost
* POSTGRES_PORT=5432
* POSTGRES_USER=postgres
* POSTGRES_PASSWORD=postgres
* POSTGRES_DB=books



## Usage

Start the Flask development server:

    python3 main.py

Start the Flask production server:

    gunicorn main:app -w 4 --threads 2 -b 0.0.0.0:5000


## Access the API at http://localhost:5000.


### API Endpoints

- **POST /auth/register**: Register a new user.
- **POST /auth/login**: Log in with an existing user.

#### Public Endpoints
- GET /api/books: Retrieve books
- **GET /api/books/genre/<genre>**: Retrieve books by genre (public).
- **GET /api/books/author/<author>**: Retrieve books by author (public).

#### Protected Endpoints

The following endpoints require authentication using a JSON Web Token (JWT). Include the JWT token in the `Authorization` header of your requests.

- **GET /api/books**: Retrieve a list of books. Authenticated users can see books with download URLs.

- **POST /api/books**: Add a new book (authenticated users only).
- **PUT /api/books/{id}**: Update an existing book (authenticated users only).
- **DELETE /api/books/{id}**: Delete a book (authenticated users only).

## Author
[Giorgi Gozalishvili](https://www.linkedin.com/in/giorgi-gozalishvili/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Feedback
If you have any feedback or questions, feel free to open an issue or reach out to us.

## Acknowledgments
Thank you for using Flask Books API!
