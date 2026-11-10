# # # # # from typing import List
# # # # # from typing import Optional
# # # # # from sqlalchemy import ForeignKey
# # # # # from sqlalchemy import String
# # # # # from sqlalchemy.orm import DeclarativeBase
# # # # # from sqlalchemy.orm import Mapped
# # # # # from sqlalchemy.orm import mapped_column
# # # # # from sqlalchemy.orm import relationship

# # # # # #声明模型
# # # # # class Base(DeclarativeBase):
# # # # #     pass

# # # # # class User(Base):
# # # # #     __tablename__ = 'user_account'

# # # # #     id: Mapped[int] = mapped_column(primary_key=True)
# # # # #     name: Mapped[str] = mapped_column(String(30))
# # # # #     fullname: Mapped[Optional[str]]

# # # # #     addresses: Mapped[List["Address"]] = relationship(
# # # # #         back_populates='user',cascade='all, delete-orphan'
# # # # #     )

# # # # #     def __repr__(self) -> str:
# # # # #         return f'User(id={self.id!r}, name={self.name!r},fullname={self.fullname!r})'

# # # # # class Address(Base):
# # # # #     __tablename__ = 'address'

# # # # #     id: Mapped[int] = mapped_column(primary_key=True)
# # # # #     email_address: Mapped[str]
# # # # #     user_id: Mapped[int] = mapped_column(ForeignKey('user_account.id'))

# # # # #     user: Mapped['User'] = relationship(back_populates='addresses')

# # # # #     def __repr__(self) -> str:
# # # # #         return f'Address(id={self.id!r}, email_address={self.email_address!r})'




# # # # # #创建引擎
# # # # # from sqlalchemy import create_engine
# # # # # engine = create_engine('sqlite://', echo=True)




# # # # # #创建对象并持久化
# # # # # from sqlalchemy.orm import Session

# # # # # with Session(engine) as session:
# # # # #     spongebob = User(
# # # # #         name='spongebob',
# # # # #         fullname='Spongebob Squarepants',
# # # # #         addresses=[Address(email_address='spongebob@sqlalchemy.org')],
# # # # #     )
# # # # #     sandy = User(
# # # # #         name='sandy',
# # # # #         fullname='Sanddy cheeks',
# # # # #         address=[
# # # # #             Address(email_address='sandy@sqlalchemy.org'),
# # # # #             Address(email_address='sandy@squirrelpower.org'),
# # # # #         ]
# # # # #     )
# # # # #     patrick = User(name='patrick',fullname='Patrick Star')

# # # # #     session.add_all([spongebob,sandy,patrick])

# # # # #     session.commit()




# # # # # #查询
# # # # # from sqlalchemy import select

# # # # # session = Session(engine)

# # # # # stmt = select(User).where(User.name.in_(['spongebob','sandy']))

# # # # # for user in session.scalars(stmt):
# # # # #     print(user)

# # # # # stmt = (
# # # # #     select(Address)                  
# # # # #     .join(Address.user)               
# # # # #     .where(User.name == 'sandy')
# # # # #     .where(Address.email_address == 'sandy@sqlalchemt.org')
# # # # # )
# # # # # sandy_address = session.scalars(stmt).one()


# SELECT address.id, address.user_id, address.email_address
# FROM address
# JOIN user ON user.id = address.user_id
# WHERE user.name = ?
#   AND address.email_address = ?


# # # # # #更改
# # # # # stmt = select(User).where(User.name == 'patrick')
# # # # # patrick = session.scalars(stmt).one()

# # # # # patrick.addresses.append(Address(email_address='patrickstar@sqlalchemy.org'))

# # # # # sandy_address.email_address = 'sandy_cheeks@sqlalchemy.org'

# # # # # session.commit()





# # # # # # 删除
# # # # # sandy = session.get(User,2)
# # # # # sandy.addresses.remove(sandy_address)
# # # # # session.flush()

# # # # # session.delete(patrick)
# # # # # session.commit()




# # # # #概要-core
# # # # import asyncio

# # # # from sqlalchemy import Column
# # # # from sqlalchemy import MetaData
# # # # from sqlalchemy import select
# # # # from sqlalchemy import String
# # # # from sqlalchemy import Table
# # # # from sqlalchemy.ext.asyncio import create_async_engine

# # # # #收集表定义
# # # # meta = MetaData()

# # # # t1 = Table('t1',meta,Column('name',String(50),primary_key=True))

# # # # async def async_main() -> None:
# # # #     engine = create_async_engine('sqlite+aiosqlite://',echo=True)

# # # # #建表
# # # #     async with engine.begin() as conn:
# # # #         await conn.run_sync(meta.drop_all)
# # # #         await conn.run_sync(meta.create_all)

# # # #         await conn.execute(
# # # #             t1.insert(),[{'name':'some name 1'}, {'name':'some name 2'}]
# # # #         )

# # # # #查表
# # # #     async with engine.connect() as conn:
# # # #             result = await conn.execute(select(t1).where(t1.c.name == 'some name 1'))

# # # #             print(result.fetchall())

# # # #     await engine.dispose()


# # # # asyncio.run(async_main())




# # # # #概要-ORM
# from __future__ import annotations

# import asyncio
# import datetime
# from typing import List

# from sqlalchemy import ForeignKey
# from sqlalchemy import func
# from sqlalchemy import select
# #AsyncAttrs：混入 awaitable_attrs，让你在异步里安全访问懒加载属性
# from sqlalchemy.ext.asyncio import AsyncAttrs
# from sqlalchemy.ext.asyncio import async_sessionmaker
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.ext.asyncio import create_async_engine
# #DeclarativeBase：ORM 声明式基类，用来映射 Python 类 ↔ 数据库表。
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import selectinload

# class Base(AsyncAttrs, DeclarativeBase):
#     pass

# class B(Base):
#     __tablename__ = 'b'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     a_id: Mapped[int] = mapped_column(ForeignKey('a.id'))
#     data: Mapped[str]

# class A(Base):
#     __tablename__ = 'a'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     data: Mapped[str]
#     #让数据库生成时间戳
#     create_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
#     bs: Mapped[list[B]] = relationship()

# async def insert_objects(async_session: async_sessionmaker[AsyncSession]) -> None:
#     async with async_session() as session:
#         async with session.begin():
#             #A通过relationship直接挂子对象，数据先加a，拿到自增id，然后加b
#             session.add_all(
#                 [
#                     A(bs=[B(data='b1'), B(data='b2')],data='a1'),
#                     A(bs=[],data='a2'),
#                     A(bs=[B(data='b3'), B(data='b4')],data='a3'),
#                 ]
#             )


# async def select_and_update_objects(
#         async_session: async_sessionmaker[AsyncSession],
# ) -> None:
#     async with async_session() as session:
#         #relationship() 默认 lazy="select"，访问时才发sql，同步属性访问时无法 await，selectinload(A.bs) 预加载
#         stmt = select(A).order_by(A.id).options(selectinload(A.bs))

#         result = await session.execute(stmt)

#         for a in result.scalars():
#             print(a,a.data)
#             print(f'created at: {a.create_date}')
#             for b in a.bs:
#                 print(b,b.data)

#         result = await session.execute(select(A).order_by(A.id).limit(1))

#         a1 = result.scalars().one()

#         a1.data = 'new data'

#         await session.commit()

#         print(a1.data)

# #用 awaitable_attrs 把懒加载变成可 await 的操作；适用于没预加载，但运行时又需要的关系
#         for b1 in await a1.awaitable_attrs.bs:
#             print(b1,b1.data)


# async def async_main() -> None:
#     engine = create_async_engine('sqlite+aiosqlite://',echo=True)

# #默认 commit() 后所有对象属性会过期，下次访问要重新查库（异步下就是 MissingGreenlet）。这里关掉它
#     async_session = async_sessionmaker(engine,expire_on_commit=False)

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     await insert_objects(async_session)
#     await select_and_update_objects(async_session)

#     await engine.dispose()


# asyncio.run(async_main())




# # # # #ORM精简版

# # # # #所有注解变成字符串（PEP 563 延迟求值），
# # # # # 类定义时不解引用，等 SQLAlchemy 后续用 typing.get_type_hints 时才真正解析。
# # # # from __future__ import annotations

# # # # from typing import List

# # # # from sqlalchemy.ext.asyncio import AsyncAttrs
# # # # from sqlalchemy.orm import DeclarativeBase
# # # # from sqlalchemy.orm import Mapped
# # # # from sqlalchemy.orm import relationship

# # # # class Base(AsyncAttrs, DeclarativeBase):
# # # #     pass

# # # # class A(Base):
# # # #     __tablename__ = 'a'

# # # #     bs: Mapped[List[B]] = relationship()
    

# # # # class B(Base):
# # # #     __tablename__ = 'b'

# # # # #AsyncSession.scalars() 是异步方法，调用它只拿到协程，还没执行
# # # # a1 = (await session.scalars(select(A))).one()
# # # # for b1 in await a1.awaitable_attrs.bs:
# # # #     print(b1)





# # # # orm
# from __future__ import annotations

# import asyncio
# import datetime
# from typing import List
# from typing import Optional

# from sqlalchemy import ForeignKey
# from sqlalchemy import func
# from sqlalchemy.ext.asyncio import async_sessionmaker
# from sqlalchemy.ext.asyncio import AsyncAttrs
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.future import select
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import selectinload



# class Base(AsyncAttrs, DeclarativeBase):
#     pass


# class A(Base):
#     __tablename__ = 'a'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     data: Mapped[Optional[str]]
#     create_date: Mapped[datetime.datetime] = mapped_column(
#         server_default=func.now()
#     )
#     bs: Mapped[List[B]] = relationship()


# class B(Base):
#     __tablename__ = 'b'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     a_id: Mapped[int] = mapped_column(ForeignKey('a.id'))
#     data: Mapped[Optional[str]]


# async def async_main():
#     engine = create_async_engine(
#         'postgresql+asyncpg://scott://tiger@localhost/test',
#         echo=True,
#     )

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     async_session = async_sessionmaker(engine, expire_on_commit=False)

#     async with async_session() as session:
#         async with session.begin():
#             session.add_all(
#                 [
#                     A(bs=[B(), B()], data='a1'),
#                     A(bs=[B()], data='a2'),
#                     A(bs=[B(), B()], data='a3'),
#                 ]
#             )        

#     stmt = select(A).options(selectinload(A.bs))

#     result = await session.scalars(stmt)

#     for a1 in result:
#         print(a1)
#         print(f'created at: {a1.create_date}')
#         for b1 in a1.bs:
#             print(b1)

#     result = await session.stream(stmt)

#     async for a1 in result.scalars():
#         print(a1)
#         for b1 in a1.bs:
#             print(b1)

#     result = await session.scalars(select(A).order_by(A.id))

#     a1 = result.first()

#     a1.data = 'new data'

#     await session.commit()

#     for b1 in await a1.awaitable_attrs.bs:
#         print(b1)


# asyncio.run(async_main())        





# # #gather_orm_statements

# # import asyncio
# # import random

# # from sqlalchemy.ext.asyncio import async_sessionmaker
# # from sqlalchemy.ext.asyncio import create_async_engine
# # from sqlalchemy.future import select
# # from sqlalchemy.orm import DeclarativeBase
# # from sqlalchemy.orm import Mapped
# # from sqlalchemy.orm import mapped_column
# # from sqlalchemy.orm import merge_frozen_result


# # class Base(DeclarativeBase):
# #     pass


# # class A(Base):
# #     __tablename__ = 'a'

# #     id: Mapped[int] = mapped_column(primary_key=True)
# #     data: Mapped[str]

# #     def __repr__(self):
# #         id_, data = self.id, self.data
# #         return f'A{id_=}, {data=}'


# # async def run_out_band(async_sessionmaker, statement, merge_results=True):

# #     async with async_sessionmaker() as oob_session:
# #         await oob_session.connection(
# #             execution_options=['isolation_level': 'AUTOCOMMIT']
# #         )    

# #     result = await oob_session.execute(statement)

# #     if merge_results:
# #         return result.freeze()
# #     else:
# #         await result.close()


# # async def async_main():
# #     engine = create_async_engine(
# #         'postgresql+asyncpg://scott:tiger@localhost/test',
# #         echo=True,
# #     )        

# #     async with engine.begin() as conn:
# #         await conn.run_sync(Base.metadata.drop_all)
# #         await conn.run_sync(Base.metadata.create_all)

# #     async_session = async_sessionmaker(engine, expire_on_commit=False)

# #     async with async_session() as session, session.begin():
# #         session.add_all([A(data='a_%d' % i) for i in range(100)])

# #     statements = [
# #         select(A).where(A.data == 'a_%d' % random.choice(range(100)))        
# #     ]

# #     frozen_results = await asyncio.gather(
# #         *(
# #             run_out_of_band(async_session, statement)
# #             for statement in statements
# #         )
# #     )
# #     results = [
# #         (
# #             await session.run_sync(
# #                 merge_frozen_result, statement, result, load=False
# #             )
# #         )()
# #         for statement, result in zip(statements, frozen_results)
# #     ]

# #     print(f'results: {[r.all() for r in results]}')


# # asyncio.run(async_main())    



#创建引擎
# from sqlalchemy import create_engine
#                                             #服务器地址
# engine = create_engine(
#     'postgresql+psycopg://postgres:123456@localhost:5432/postgres',echo=True
#     )



# from sqlalchemy import text

# with engine.connect() as conn:
#     Result = conn.execute(text("select 'hello world'"))
#     print(Result.all())


# with engine.connect() as conn:
#     conn.execute(text('CREATE TABLE some_table(x int, y int)'))
#     conn.execute(                                   #防止数据库注入
#         text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
#         [{'x': 1, 'y': 1}, {'x': 2, 'y': 4}],
#     )
#     conn.commit()


# with engine.begin() as conn:
#     conn.execute(
#         text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
#         [{'x': 6, 'y': 8}, {'x':9, 'y': 10}],
#     )


# with engine.connect() as conn:
#     result = conn.execute(text('SELECT x, y FROM some_table'))
#     for row in result:
#         print(f'x: {row.x} y:{row.y}')


# with engine.connect() as conn:
#     result = conn.execute(text('SELECT x, y FROM some_table WHERE y > :y'), {'y': 2})        
#     for row in result:
#         print(f'x: {row.x} y: {row.y}')


#用会话增删改查ddl
# from sqlalchemy.orm import Session

# # stmt = text('SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y')
# # with Session(engine) as session:
# #     result = session.execute(stmt, {'y': 6})
# #     for row in result:
# #         print(f'x: {row.x} y: {row.y}')


# with Session(engine) as session:
#     result = session.execute(
#         text('UPDATE some_table SET y=:y WHERE x=:x'),
#         [{'x': 9, 'y': 11}, {'x': 13, 'y': 15}],
#     )        
#     session.commit()


#用声明式基类建表，关联
# from sqlalchemy.orm import DeclarativeBase
# from typing import Optional
# from sqlalchemy import (
#     String,
#     ForeignKey, 
#     select,
# )
# from sqlalchemy.orm import (
#     Session,
#     Mapped,
#     mapped_column,
#     relationship,
#     selectinload
# )

# class Base(DeclarativeBase):
#     pass

# class User(Base):
#     __tablename__ = 'user_account'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30))
#     fullname: Mapped[Optional[str]]

#     addresses: Mapped[list['Address']] = relationship(back_populates='user')

#     def __repr__(self) -> str:
#         return f'User(id={self.id,}, name={self.name}, fullname={self.fullname})'

# class Address(Base):
#     __tablename__ = 'address'

#     id: Mapped[int] = mapped_column(primary_key=True) 
#     email_address:Mapped[str]
#     user_id = mapped_column(ForeignKey('user_account.id'))

#     user: Mapped[User] = relationship(back_populates='addresses')   

#     def __repr__(self) -> str:
#         return f'Address(id={self.id}, email_address={self.email_address})'

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


# 插入（瞬态）
# squidward = User(name='squidward', fullname='Squidward Tentacles')
# krabs = User(name='ehkrabs', fullname='Eugene H. Krabs')
# session = Session(engine)
# #挂起状态
# session.add(squidward)
# session.add(krabs)
# #先执行一次,挂起状态flush后持久状态
# session.flush()


# # 事务被回滚,但序列已经前进过了
# # print("squidward.id =", squidward.id)   # 大概率是 3
# # print("krabs.id     =", krabs.id)       # 大概率是 4

# # 再提交，挂起的一并提交
# session.commit()



# 更新
# sandy = User(name='sandy', fullname='sandy Tentacles')
# #挂起状态
# session.add(sandy)
# session.commit()
# #                                     #  WHERE                   准确返回一个标量结果或引发异常。
# sandy = session.execute(select(User).filter_by(name='sandy')).scalar_one()

# sandy.fullname = 'Sandy Squirrel'
# # 重新查询                                              where 只收布尔表达式，不收**kwargs
# sandy_fullname = session.execute(select(User.fullname).where(User.id == 1)).scalar_one()
# print(sandy_fullname)



# 删除
# sandy = session.get(User, 1)
# #挂起状态
# session.delete(sandy)
# # 重新查询
# session.execute(select(User).where(User.id == 1)).first()
# print(sandy in session)



# 回滚
# patrick = User(name='patrick', fullname='patrick-json')
# session.add(patrick)
# session.commit()

# patrick = session.get(User, 1)
# session.delete(patrick)
# #rollback 当前与此 Session 关联的所有对象过期（expire）, 提交无法回滚！
# session.rollback()
# print(patrick in session)



# #游离
# session.close()




#relationship关联
# u1 = User(name='pkrabs', fullname='Pearl Krabs')
# print(u1.addresses)
# a1 = Address(email_address='[email protected]')
# u1.addresses.append(a1)
# print(u1.addresses)

# a2 = Address(email_address='[email protected]', user=u1)
# print(u1.addresses)

# session.add(u1)
# print(u1 in session)
# print(a1 in session)
# print(a2 in session)

# session.commit()



# # # expire_on_commit
# # # 重发select
# # print(u1.id)
# # # 延迟加载
# # print(u1.addresses)



# print(select(Address.email_address).select_from(User).join(User.addresses))

# SELECT address.email_address
# FROM user JOIN address ON user.id = address.user_id


# 加载策略
#selectinload
# for user_obj in session.execute(
#     select(User).options(selectinload(User.addresses))
# ).scalars():
#     user_obj.addresses



# class User(Base):
#     __tablename__ = "user_account"

#     addresses: Mapped[list["Address"]] = relationship(
#         back_populates="user", lazy="selectin"
#     )


# stmt = select(User).options(selectinload(User.addresses)).order_by(User.id)
# for row in session.execute(stmt):
#     print(
#         f'{row.User.name}  ({', '.join(a.email_address for a in row.User.address)})'
#     )



# 隔离
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


eng = create_engine(
    "postgresql+psycopg2://scott:tiger@localhost/test",
    isolation_level='REPEATABLE READ',
)

session = sessionmaker(eng)



eng = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")
autocommit_engine = eng.execution_options(isolation_level='AUTOCOMMIT')

transactional_session = sessionmaker(eng)
autocommit_session = sessionmaker(autocommit_engine)