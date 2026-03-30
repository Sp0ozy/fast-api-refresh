from typing import Optional

from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="The ID of the book. This will be auto-generated.", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0, lt=2027)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Example Book",
                "author": "Example Author",
                "description": "Example Description",
                "rating": 5,
                "published_date": 2020
            }
        }
    }

BOOKS = [
    Book(1, "Title 1", "Author 1", "Description 1", 5, 2020),
    Book(2, "Title 2", "Author 2", "Description 2", 4, 2021),
    Book(3, "Title 3", "Author 3", "Description 3", 3, 2022),
    Book(4, "Title 4", "Author 2", "Description 4", 2, 2022),
    Book(5, "Title 5", "Author 2", "Description 5", 1, 2024),
    Book(6, "Title 6", "Author 3", "Description 6", 5, 2022),
    Book(7, "Title 7", "Author 2", "Description 7", 4, 2026),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_filter(book_rating: Optional[int] = Query(gt=0, lt=6, default=None), published_date: Optional[int] = Query(gt=0, lt=2027, default=None)):
    books_to_return = BOOKS
    if book_rating is not None:
        books_to_return = [b for b in books_to_return if b.rating == book_rating]
    if published_date is not None:
        books_to_return = [b for b in books_to_return if b.published_date == published_date]
    return books_to_return

@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    #     book.id=BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_request.id:
            BOOKS[i] = Book(**book_request.model_dump())
            return {"message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            del BOOKS[i]
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")