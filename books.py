from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title 1", "author": "Author 1", "category": "Category 1"},
    {"title": "Title 2", "author": "Author 2", "category": "Category 2"},
    {"title": "Title 3", "author": "Author 3", "category": "Category 3"},
    {"title": "Title 4", "author": "Author 4", "category": "Category 4"},
    {"title": "Title 5", "author": "Author 5", "category": "Category 5"},
    {"title": "Title 6", "author": "Author 6", "category": "Category 6"},
]

@app.get("/api-endpoint")
async def first_api():
    return {"message": "Hello, World!"}

@app.get("/books")
async def get_books():
    return BOOKS

@app.get("/books/mybook")
async def get_my_book():
    return {"My Book": "This is my favourite book"}

@app.get("/books/{dynamic_parameter}")
async def get_book_by_title(dynamic_parameter: str):
    for book in BOOKS:
        if book["title"] == dynamic_parameter:
            return book
    return {"message": "Book not found"}

@app.get("/books/")
async def get_book_by_category(category: str):
    books_to_return = []
    for book in BOOKS:
        if book["category"] == category:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/author/")
async def get_books_by_author_query(author_name: str ):
    books_to_return = []
    for book in BOOKS:
        if book["author"].casefold() == author_name.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{author_name}/")
async def get_book_by_author(author_name: str, category: str = None):
    books_to_return = []
    for book in BOOKS:
        if book["author"].casefold() == author_name.casefold():
            if category is None or book["category"] == category:
                books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return {"message": "Book added successfully"}

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"] == updated_book["title"]:
            BOOKS[i].update(updated_book)
            return {"message": "Book updated successfully"}
    return {"message": "Book not found"}

@app.delete("/books/delete_book/{title}")
async def delete_book(title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"] == title:
            del BOOKS[i]
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}

#  Fetch all books by a specific author using path or query parameters
@app.get("/books/author/{author_name}")
async def get_books_by_author(author_name: str):
    books_to_return = []
    for book in BOOKS:
        if book["author"].casefold() == author_name.casefold():
            books_to_return.append(book)
    return books_to_return

