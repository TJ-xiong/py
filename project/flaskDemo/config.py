import os

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 默认数据库
SQLALCHEMY_DATABASE_URI = (
    '{driver}://{user}:{pwd}@{host}:{port}/{db}?charset=utf8mb4'.format(
        driver='mysql+pymysql',
        user=os.getenv('MYSQL_USER'),
        pwd=os.getenv('MYSQL_PWD'),
        host=os.getenv('MYSQL_HOST'),
        port=os.getenv("MYSQL_PORT"),
        db=os.getenv('MYSQL_DB')
    )
)

SQLALCHEMY_TRACK_MODIFICATIONS=False