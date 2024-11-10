class Config:
    MYSQL_HOST = 'db'
    MYSQL_USER = 'root'
    MYSQL_PORT = 3306
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'myflaskapp'
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'

