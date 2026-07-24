# 🛒 E-Commerce FastAPI Boilerplate
**Version:** Beta 0.1

A fully functional, asynchronous API for an online store. This project serves as a solid foundation (Boilerplate) for building modern backend applications. Made as next junior project for diving into Python Development world.

## ✨ Key Features
* **User Management:** Registration, secure password hashing (Bcrypt).
* **JWT Authentication:** Advanced token-based login system (OAuth2).
* **Product Management:** Input/output data validation, categorization.
* **Shopping Cart & Orders:** Automatic order assignment to the logged-in user based on their JWT token.
* **Database:** Relational structure using SQLAlchemy (ready for SQLite/PostgreSQL).

## 🛠️ Tech Stack
* **Python 3.10+**
* **FastAPI** - A blazing fast framework for building APIs.
* **SQLAlchemy** - Powerful ORM for database interactions.
* **Pydantic** - Data validation and serialization.
* **PyJWT & Passlib** - Security, password hashing, and authentication.

## 🚀 How to run locally?

1. Clone the repository to your local machine.
2. Install the required dependencies (FastAPI, Uvicorn, SQLAlchemy, Pydantic, etc.).
   pip install -r /path/to/requirements.txt

3. Run the development server using Uvicorn:
   uvicorn main:app --reload