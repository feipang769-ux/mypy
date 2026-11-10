from .config import get_settings
from sqlalchemy import make_url, create_engine, text
from .models import Base
from .db import _engine


def init_db_and_table():
    settings = get_settings()
    db_url = make_url(str(settings.database_url))
    target_db_name = db_url.database
    db_name = db_url.set(database='postgres')
    engine = create_engine(db_name, isolation_level='AUTOCOMMIT')

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{target_db_name}'"))
        exists = result.scalar()

        if not exists:
            conn.execute(text(f'CREATE DATABASE "{target_db_name}"'))
        else:
            print(f'数据库 {target_db_name} 已存在')

    engine.dispose()


    Base.metadata.create_all(_engine)
    print('表已创建')

if __name__ == '__main__':
    init_db_and_table()
    
    
