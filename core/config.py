import os


class Config:
    SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')
    THREADS_PER_PAGE = 10
