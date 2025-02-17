# [REST API application Pythongram](README.md)

This project is a REST API application that allows users to share photos. It includes user authentication, photo uploading, photo changing, commenting, and role-based access control.

## [Built With](README.md)

* [![Python][Python]][Python-url]
* [![FastAPI][FastAPI]][FastAPI-url]
* [![SQLAlchemy][SQLAlchemy]][SQLAlchemy-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
* [![Redis][Redis]][Redis-url]
* [![Cloudinary][Cloudinary]][Cloudinary-url]

## [Main Features](README.md)

- User registration and authentication with JWT tokens
- User roles (admin, moderator, user) with different access levels
- Photo uploading and transformation
- Commenting on photos
- QR code generation for photo URLs
- Cloudinary integration for photo storage
- Redis for caching
- PostgreSQL database for data storage
- Email verification and password reset

## [Implementation of the Project](README.md)

A file is required for the project to work `/.env` with environment variables.
Create it with this content and substitute your values.

```dotenv
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=

SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}

SECRET_KEY=
ALGORITHM=

MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=

redis_host=
redis_port=
redis_password=

CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

## [Instalation](README.md)

1. Install Docker
2. Clone project
```bash
git clone https://github.com/oleksandr-study/Project-Pythongram.git
cd Project-Pythongram
```
3. Install the dependencies:
```bash
pip install poetry
poetry shell
poetry update
```
4. Create .env and add info as at example
5. Apply database migrations
```bash
alembic upgrade head
```
6. Start Docker images
```bash
docker-compose up
```
7. Run the application:
```bash
python main.py
```
8. GOTO [127.0.0.1:8000](http://127.0.0.1:8000/)
9. Enjoy

## [Project made by Brains Team:](README.md)

* [Oleksandr Velychko](https://github.com/oleksandr-study/)
* [Anna Pashkova](https://github.com/777sleepy777)
* [Yevheniia Shabanova](https://github.com/Vrokmoit)
* [Bohdan Datsko](https://github.com/skwet)
* [Kostiantyn Litvinov](https://github.com/Kollos777)
* [Yunusov Grigory](https://github.com/Grigory-Yunusov)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/python-FFD700?style=for-the-badge&logo=python&logoColor=#3776AB
[Python-url]: https://www.python.org/
[FastAPI]: https://img.shields.io/badge/fastapi-black?style=for-the-badge&logo=fastapi&logoColor=#009688
[FastAPI-url]: https://fastapi.tiangolo.com/
[SQLAlchemy]: https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=SQLAlchemy&logoColor=#D71F00
[SQLAlchemy-url]: https://www.sqlalchemy.org/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-C5C6D0?style=for-the-badge&logo=PostgreSQL&logoColor=4169E1
[PostgreSQL-url]: https://www.postgresql.org/
[Redis]: https://img.shields.io/badge/Redis-FF4438?style=for-the-badge&logo=Redis&logoColor=white
[Redis-url]: https://redis.io/
[Cloudinary]: https://img.shields.io/badge/Cloudinary-7F7D9C?style=for-the-badge&logo=Cloudinary&logoColor=3448C5
[Cloudinary-url]: https://cloudinary.com/