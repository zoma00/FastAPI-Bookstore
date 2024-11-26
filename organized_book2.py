from fastapi import FastAPI, HTTPException  # Importing FastAPI and HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()  # Initialize the FastAPI application

# Book model representing a book entity
class Book:
    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

# Request model for creating or updating a book
class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "This is a description of the new book.",
                "rating": 5
            }
        }

# Sample book data
BOOKS = [
    Book(1, 'Computer Science Pro', 'Codingwithruby', 'A very nice book', 5),
    Book(2, 'Be Fast with FastAPI', 'Codingwithruby', 'A great book', 5),
    Book(3, 'Master Endpoints', 'Codingwithruby', 'Awesome book', 5),
    Book(4, 'HP1', 'Codingwithruby', 'A very nice book', 2),
    Book(5, 'HP2', 'Codingwithruby', 'A very nice book', 3),
    Book(6, 'HP3', 'Codingwithruby', 'A very nice book', 1)
]

# Endpoint to retrieve all books
@app.get("/books")
async def read_all_books():
    return BOOKS

# Endpoint to retrieve a book by its ID
@app.get("/book/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:  # Check if the book ID matches
            return book
    return {"error": "book not found"}  # Return error if book not found

# Endpoint to filter books by rating
@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    book_to_return = []  # Initialize an empty list to collect matching books
    for book in BOOKS:
        if book.rating == book_rating:  # Compare book rating with the provided rating
            book_to_return.append(book)  # Add matching book to the list
    return book_to_return

# Endpoint to update an existing book
@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:  # Check if the book ID matches
            BOOKS[i] = book  # Update the book information

# Function to find a new ID for a book
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1  # Assign new ID based on existing books
    return book

# Endpoint to create a new book
@app.post("/create-book")
async def create_book(book_request: BookRequest):
    # Check if the ID already exists
    if any(book.id == book_request.id for book in BOOKS):
        raise HTTPException(status_code=400, detail="Book ID already exists.")

    # Validate rating range
    if book_request.rating < 1 or book_request.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

    new_book = Book(**book_request.dict())  # Create a new book instance
    BOOKS.append(find_book_id(new_book))  # Add the new book to the collection
    return new_book  # Return the newly created book


""" don't use body anymore it doesn't allow for validation.
Pydantics is a python library that is used for data modeling, data parsing, and has efficient error
We are also going to be adding pedantic field data validation on each variable and element of the request.

so you just want to change dot dictionary two dot model dump.

Asterisk is a way for us to expand this dictionary.
So we're saying dictionary, which is going to return all of the variables into a dictionary format.
In This allows us to expand those dictionary keys and values into the keyword arguments that are needed
for our constructor.
So really what we're saying is create a new book inside our book, inside our book constructor.
We are going to grab our book request, turn it into a dictionary, which will have a name value pair,
In this asterisk in the front allows us to now assign those into our keyword arguments and then new book

"""

"""
code
--------
book.id = BOOKS[-1].id +1

we want to just sign our book ID to the last element in the list, its ID plus one.
If not, we just want to create a new book with a book ID of one, because it's going to be the first
Your understanding is correct! Let's break down the line of code `book.id = BOOKS[-1].id + 1` for clarity:

### Explanation

1. **Accessing the Last Element**:
   - `BOOKS[-1]` is a way to access the last element in the list `BOOKS`. In Python, negative indexing allows you to 
   count from the end of a list. So, `-1` refers to the last item, `-2` would refer to the second last item, and so on.

2. **Getting the Last Book ID**:
   - `BOOKS[-1].id` retrieves the `id` attribute of the last book in the `BOOKS` list. This assumes that each book object
    in the list has an `id` attribute.

3. **Creating a New ID**:
   - By adding `1` to the last book's ID (`BOOKS[-1].id + 1`), you generate a new unique ID for the book you are creating. 
   This ensures that the new book ID is always one greater than the ID of the last book in the list.

### Summary

- If there are existing books in the `BOOKS` list, the new book's ID will be one more than the ID of the most recently
 added book.
- If the list is empty (`len(BOOKS) == 0`), the new book's ID is set to `1`.

This method helps maintain unique IDs for each book in your collection. 

### Example

Here's a quick example for clarity:

- **Existing Books**: 
  - Book 1: ID = 1
  - Book 2: ID = 2
  - Book 3: ID = 3
- **New Book Creation**:
  - `BOOKS[-1].id` would be `3`, so the new book ID will be `3 + 1 = 4`.

Feel free to ask if you have any more questions!
"""

"""
swagger result after create a new book with a new id is :
------------------------------------------------------------


Response body
Download
[
  {
    "id": 1,
    "title": "Computer Science Pro",
    "author": "Codingwithruby",
    "description": "A very nice book",
    "rating": 5
  },
  {
    "id": 2,
    "title": "Be Fast with FastAPI",
    "author": "Codingwithruby",
    "description": "A great book",
    "rating": 5
  },
  {
    "id": 3,
    "title": "Master Endpoints",
    "author": "Codingwithruby",
    "description": "Awesome book",
    "rating": 5
  },
  {
    "id": 4,
    "title": "HP1",
    "author": "Codingwithruby",
    "description": "A very nice book",
    "rating": 2
  },
  {
    "id": 5,
    "title": "HP2",
    "author": "Codingwithruby",
    "description": "A very nice book",
    "rating": 3
  },
  {
    "id": 6,
    "title": "HP3",
    "author": "Codingwithruby",
    "description": "A very nice book",
    "rating": 1
  },
  {
    "id": 7,
    "title": "string",
    "author": "string",
    "description": "string",
    "rating": 3
  }
]
"""

"""
conint is a utility from the pydantic library used for defining constrained integer types. 
It allows you to create integer fields with specific constraints, such as minimum and maximum values. 
This is particularly useful for
 validating input data in models, ensuring that the values meet certain criteria.

Key Features of conint
Constraints: You can specify constraints like:

ge: Greater than or equal to a specified value.
le: Less than or equal to a specified value.
gt: Greater than a specified value.
lt: Less than a specified value.


=================

In the context of the Pydantic Field definition, when you specify min_length=1 for the author field in your BookRequest
 model, it means that the author’s name must contain at least one character. This does not necessarily mean one word; 
 it simply means that the string must be at least one character long.
"""

"""
@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    book_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)
    return book_to_return
** Explain why we use book.rating == book_rating   (how the book.rating work in python code?
** Explain why we use book_to_return = [ ] , otherwise if we use get method with id we will not use the list [ ] ?

Answer:
---------
Let's break down your questions regarding the `read_book_by_rating` function in your FastAPI application.

### 1. Understanding `book.rating == book_rating`

In the line `if book.rating == book_rating:`, you're comparing the rating of each book in the `BOOKS` list to the 
`book_rating` parameter provided in the request. Here’s how it works:

- **`book`**: This variable represents an instance of the `Book` class (or whatever structure you have for books) within
 the `BOOKS` list.
- **`book.rating`**: This accesses the `rating` attribute of the `book` instance. In Python, attributes of an object are 
accessed using dot notation. So, if `book` is an instance of a class that has a `rating` attribute, `book.rating` 
retrieves that attribute's value.
- **Comparison**: The comparison `book.rating == book_rating` checks if the rating of the current book matches the
 `book_rating` passed as a query parameter in the request. If they match, the book is added to the `book_to_return` list.

### 2. Why Use `book_to_return = []`?

The line `book_to_return = []` initializes an empty list to store books that match the specified rating. Here’s why this 
approach is used:

- **Collecting Matches**: Since you are potentially dealing with multiple books that could have the same rating, you 
need a way to collect all of them. An empty list is a suitable structure for this purpose.
- **Dynamic Population**: As you iterate through the `BOOKS` list, you can append each book that meets the condition 
(`book.rating == book_rating`) to `book_to_return`. This allows you to return all matching books at once.

### Example of How It Works

Here’s a simplified example to illustrate:

```python
BOOKS = [
    {"id": 1, "title": "Book One", "rating": 5},
    {"id": 2, "title": "Book Two", "rating": 4},
    {"id": 3, "title": "Book Three", "rating": 5},
]

def read_book_by_rating(book_rating: int):
    book_to_return = []  # Initialize an empty list
    for book in BOOKS:
        if book['rating'] == book_rating:  # Compare the rating
            book_to_return.append(book)  # Add matching book to the list
    return book_to_return  # Return the list of matching books

# Example usage
print(read_book_by_rating(5))  # Would return Book One and Book Three
```

### When Using an ID

If you were to implement a `get` method that retrieves a book by its ID, you would typically not need a list because
 you expect to find either one book or none. For example:

```python
@app.get("/books/{book_id}")
async def read_book_by_id(book_id: int):
    for book in BOOKS:
        if book['id'] == book_id:
            return book  # Return the single book found
    return {"error": "Book not found"}
```

In this case, you directly return the book if found, or an error message if not, without needing to collect multiple 
items into a list.

### Summary

- **`book.rating == book_rating`**: This comparison checks if the current book's rating matches the provided rating.
- **Using `book_to_return = []`**: This initializes an empty list to collect all books that match the rating condition, 
allowing for multiple results to be returned.
- **Single Item Retrieval**: When fetching by ID, you typically return a single item or an error without needing a
 collection, as each ID should uniquely identify one book.
"""

"""
The difference between using `if book.id == id` and `if book['id'] == id` lies in how you access the `id` attribute of
 the `book` object. Here’s a detailed explanation of both approaches:

### 1. Accessing Attributes with Dot Notation: `book.id`

- **Usage**: `if book.id == id`
- **Context**: This approach assumes that `book` is an instance of a class (e.g., a Pydantic model or a custom class) 
that has an attribute named `id`.
- **Type Safety**: When you use dot notation, you benefit from type checking and autocomplete features in many IDEs, 
as the attribute is defined in the class.
- **Example**:
    ```python
    class Book:
        def __init__(self, id, title):
            self.id = id
            self.title = title

    book = Book(1, "Sample Book")
    if book.id == 1:
        print("Book found!")
    ```

### 2. Accessing Elements with Dictionary Notation: `book['id']`

- **Usage**: `if book['id'] == id`
- **Context**: This approach assumes that `book` is a dictionary (or an object that supports item access, like a 
`NamedTuple` or a `dataclass` with `__getitem__` defined) 
and you are accessing the value associated with the key `'id'`.
- **Flexibility**: This method is more flexible for data structures like dictionaries, where keys can be dynamically
 added or changed.
- **Example**:
    ```python
    book = {"id": 1, "title": "Sample Book"}
    if book['id'] == 1:
        print("Book found!")
    ```

### Summary of Differences

| Feature                   | `book.id`                    | `book['id']`                  |
|---------------------------|------------------------------|-------------------------------|
| **Type**                  | Attribute of an object/class | Key in a dictionary           |
| **Error Handling**        | Raises `AttributeError` if `id` does not exist | Raises `KeyError` if `id` key is not found |
| **Type Checking**         | Supported by IDEs            | No type checking (dynamic)    |
| **Use Case**              | Object-oriented programming   | Data manipulation with dictionaries |

### When to Use Each

- **Use `book.id`** when working with objects that have a defined structure (like classes or models) and you want to 
leverage the benefits of object-oriented programming.
- **Use `book['id']`** when working with dictionaries or when you need flexibility in your data structure, such as when
 the data is not strictly typed or when it comes from external sources (like JSON).

### Conclusion

The choice between dot notation and dictionary notation depends on the context of your data structure and the design of 
your application. Each method has its use cases and advantages, so it's essential to choose based on your 
specific needs.
"""