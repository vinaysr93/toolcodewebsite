import os
import pandas as pd
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA = None

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "toolcodes.sqlite3")
    DATA = pd.read_excel("./static/assets/tool_price.xlsx")
    DEBUG = True