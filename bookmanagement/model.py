from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from sqlalchemy import create_engine, ForeignKey, select, delete, event

from typing import List


class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "tblAuthor"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    books: Mapped[List["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Author: {self.name}>"

class Book(Base):
    __tablename__ = "tblBook"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    isbn: Mapped[str] = mapped_column(nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("tblAuthor.id", ondelete='CASCADE'))
    genre_id: Mapped[int] = mapped_column(ForeignKey("tblGenre.id", ondelete="CASCADE"))
    
    genre = relationship('Genre', back_populates="books")
    author: Mapped[Author] = relationship(back_populates="books")
    
    def __repr__(self):
        return f"<Title: {self.title}; AuthorID: {self.author_id}>"

class Genre(Base):
    __tablename__ = "tblGenre"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    books = relationship('Book', back_populates="genre")

    def __repr__(self):
        return f"<Genre: {self.name}>"


class DatabaseAPI:
    def __init__(self, connection_string: str = "sqlite:///books.db"):
        self.engine = create_engine(connection_string)
        self._enable_sqlite_foreign_keys()
        Base.metadata.create_all(self.engine)

    def _enable_sqlite_foreign_keys(self):
        @event.listens_for(self.engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

    def delete_book_by_name(self, title: str) -> int:
        book = self.get_book_by_name(title)
        if book:
            with Session(self.engine) as session:
                query = delete(Book).where(Book.id == book.id)
                result = session.execute(query)
                session.commit()
                return result.rowcount
        else:
            return 0
        
    def delete_author_by_name(self, author_name: str) -> int:
        author = self.get_author_by_name(author_name)
        if author:
            with Session(self.engine) as session:
                query = delete(Author).where(Author.id == author.id)
                result = session.execute(query)
                session.commit()
                return result.rowcount
        else:
            return 0

    def get_author_by_name(self, author_name: str) -> Author:
        with Session(self.engine) as session:
            query = select(Author).where(Author.name == author_name)
            found = session.scalars(query).first()
        return found
    
    def get_book_by_name(self, title: str) -> Book:
        with Session(self.engine) as session:
            query = (select(Book)
                     .join(Book.genre)
                     .join(Book.author)
                     .options(
                         selectinload(Book.author),
                         selectinload(Book.genre)
                     )
                     .where(Book.title == title)
                    )
            #select(Book).where(Book.title == title)
            found = session.scalars(query).first()
        return found
    
    def get_books_by_author(self, author_name: str) -> List[Book]:
        with Session(self.engine) as session:
            author = (select(Author)
                      .where(Author.name == author_name)
                      .options(selectinload(Author.books)))
            found = session.scalars(author).first()
            return found.books if found else []
        
    def get_books_by_genre(self, genre_name: str) -> List[Book]:
        with Session(self.engine) as session:
            genre = (select(Book)
                     .join(Book.genre)
                     .join(Book.author)
                     .options(
                         selectinload(Book.author),
                         selectinload(Book.genre)
                     )
                     .where(Genre.name == genre_name)
                    )
            return list(session.scalars(genre))
        
    def get_all_books(self) -> List[Book]:
        with Session(self.engine) as session:
            genre = (select(Book)
                     .join(Book.genre)
                     .join(Book.author)
                     .options(
                         selectinload(Book.author),
                         selectinload(Book.genre)
                     )
                    )
            return list(session.scalars(genre))

    def get_genre_by_name(self, genre_name: str) -> Genre:
        with Session(self.engine) as session:
            query = select(Genre).where(Genre.name == genre_name)
            found = session.scalars(query).first()
        return found
    
    def get_all_genre(self) -> list:
        with Session(self.engine) as session:
            query = select(Genre)
            return list(session.scalars(query))     

    def get_all_authors(self) -> list:
        with Session(self.engine) as session:
            query = select(Author)
            return list(session.scalars(query)) 
                     
    def add_genre(self, genre_name: str) -> Genre:
        found = self.get_genre_by_name(genre_name)
        if not found:
            with Session(self.engine) as session:
                genre = Genre(name=genre_name)
                session.add(genre)
                session.commit()
                session.refresh(genre)
        else:
            genre = found
        return genre

    def add_author(self, author_name: str) -> Author:
        found = self.get_author_by_name(author_name)
        if not found:
            with Session(self.engine) as session:
                author = Author(name=author_name)
                session.add(author)
                session.commit()
                session.refresh(author)
        else:
            author = found
        return author
    
    def add_book(self, title: str, author_name: str, genre_name: str, isbn: str | None = None) -> Book:
        author = self.add_author(author_name)
        genre = self.add_genre(genre_name)
        found = self.get_book_by_name(title)
        if not found:
            with Session(self.engine) as session:
                book = Book(title=title, author=author, genre=genre, isbn=isbn)
                session.add(book)
                session.commit()
                session.refresh(book)
        else:
            book = found
        return book
    
    def update_book(self, book_id: int, new_title: str, new_author_name: str, new_genre_name: str) -> None:
        with Session(self.engine) as session:
            book = session.get(Book, book_id)
            if not book:
                raise ValueError(f"Buch mit ID {book_id} nicht gefunden.")

            # Hole oder erstelle Autor und Genre
            author = self.add_author(new_author_name)
            genre = self.add_genre(new_genre_name)

            # Update der Felder
            book.title = new_title
            book.author = author
            book.genre = genre

            session.commit()



if __name__ == "__main__":
    db = DatabaseAPI()
    buch = db.get_book_by_name("Niemandsland")
    print(buch.genre)
    print(buch.author)
    # result = db.add_book(title="Der Herr der Ringe", author_name="J.R.R. Tolkien", genre_name="Fantasy")
    # print(result)
    # result = db.add_book(title="Niemandsland", author_name="Neil Gaiman", genre_name="Fantasy")
    # print(result)
    # result = db.add_book(title="American Gods", author_name="Neil Gaiman", genre_name="Fantasy")
    # print(result)
    # result = db.get_author_by_name('Neil Gaiman')
    # print(result)
    # result = db.add_book(title="Harry Potter und der Feuerkelch", author_name="J.K. Rowling", genre_name="Fantasy")
    # result = db.add_book(title="Praxiswissen Docker", author_name="Sean Kane", genre_name="Fachbuch")

    # print(db.get_books_by_author('Neil Gaiman'))
    # print(db.get_books_by_genre("Fantasy"))
    # print(db.get_books_by_genre("Fachbuch"))