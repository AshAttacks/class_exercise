import logging

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from check_storage import BookStorage

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


class BookInput(BaseModel):
    title: str
    price: float = Field(ge=0)


class BookResponse(BookInput):
    id: int


app = FastAPI(title="Books Database API")
storage = BookStorage()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    book = storage.get_book(book_id)
    if book is None:
        logger.warning(f"Book not found: {book_id}")
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info(f"Retrieved book: id={book_id}")
    return book

@app.post("/books", response_model=BookResponse)
def add_book(book: BookInput):
    # TODO: use storage.add_book(), log the new ID at INFO,
    id = storage.add_book(title=book.title, price=book.price)
    # and return the stored record with storage.get_book().
    logger.info(f"Added book: title={book.title}, price={book.price}, id={id}.")
    return storage.get_book(id)


@app.get("/books", response_model=list[BookResponse])
def list_books(
    min_price: float = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1)
):
    # TODO: pass min_price and limit to storage.list_books().
    row = storage.list_books(min_price, limit)
    # Log the returned row count at INFO and return the list.
    logger.info(f"Listed books: {row}")
    return row

@app.get("/search/books", response_model=list[BookResponse])
def search_books(
    min_price: float = Query(ge=0),
    max_price: float = Query(ge=0)
):
    # TODO: if min_price > max_price, log WARNING and raise HTTPException
    if min_price > max_price:
        logger.warning(f"min_price > max_price: {min_price}, {max_price}")
        # with status 400 and detail (e.g., "min_price must not exceed max_price").
        raise HTTPException(status_code=400, detail="min_price must not exceed max_price")
    # Otherwise, call storage.search_books().
    else:
        rows = storage.search_books(min_price, max_price)
    # Log the returned row count at INFO and return the list.
    logger.info(f"Rows returned: {len(rows)}")
    return rows