# FastAPI-Bookstore
A simple yet powerful API for managing a collection of books using FastAPI.  This project allows users to create, read, update, and filter books based on various criteria.


# FastAPI Bookstore

![FastAPI](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

## Description

FastAPI Bookstore is a RESTful API built with [FastAPI](https://fastapi.tiangolo.com/) that allows users to manage a collection of books. With this API, you can create, read, update, and filter books based on their ratings.

## Features

- **Create a new book**: Add a book to the collection with title, author, description, and rating.
- **Retrieve all books**: Get a list of all books in the collection.
- **Retrieve a book by ID**: Access a specific book's details using its unique ID.
- **Filter books by rating**: Find books that match a specific rating.
- **Update an existing book**: Modify details of an existing book.

## Getting Started

### Prerequisites

- Python 3.7 or later
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fastapi-bookstore.git
   cd fastapi-bookstore
   ```

2. Install the required packages:
   ```bash
   pip install fastapi[all]
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

### API Endpoints

| Method | Endpoint                      | Description                                |
|--------|-------------------------------|--------------------------------------------|
| GET    | `/books`                      | Retrieve all books                         |
| GET    | `/book/{book_id}`             | Retrieve a book by its ID                  |
| GET    | `/books?book_rating={rating}` | Filter books by rating                     |
| POST   | `/create-book`                | Create a new book                          |
| PUT    | `/books/update_book`          | Update an existing book                    |

## Example Usage

### Create a New Book

```http
POST /create-book HTTP/1.1
Content-Type: application/json

{
    "title": "A new book",
    "author": "codingwithroby",
    "description": "This is a description of the new book.",
    "rating": 5
}
```

### Retrieve All Books

```http
GET /books HTTP/1.1
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used.
