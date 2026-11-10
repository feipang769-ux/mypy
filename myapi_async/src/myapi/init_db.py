from .models import Base
from .db import _engine
import asyncio


async def init_db_and_table():  
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('表已创建')

if __name__ == '__main__':
    asyncio.run(init_db_and_table()) 
    
    
