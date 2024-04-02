# long_term_memory_app/config.py

import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///long_term_memory.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
