from fastapi import FastAPI

from users.router import router as user_router
from books.router import router as books_router
from borrowed_books.router import router as borrowed_books_router

app = FastAPI()

app.include_router(user_router)
app.include_router(books_router)
app.include_router(borrowed_books_router)