import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = None

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "toolcodes.sqlite3")
    UPLOAD_FOLDER = basedir+"/csv_files"

    DEBUG = True