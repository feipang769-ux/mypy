#1.path and query parameter

# from fastapi import FastAPI
# from enum import Enum

# class ModelName(str,Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

# app = FastAPI()

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message":"Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name,"message":"LeCNN all the images"}

#     return {"model_name":model_name, "message": "Have some residuals"}

# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {"file_path": file_path}

# @app.get("/")   
# async def root():
#     return {"message":"Hello World"}

# @app.get("/items/{item_id}")
# async def read_user_item(
#     item_id: str, needy: str, skip: int = 0, limit: int | None = None
#     ):
#     item = {"item_id":item_id, "needy": needy, "skip": skip, "limit": limit}
#     return item

# @app.get("/users/{user_id}/items/{item_id}")
# async def read_user_item(
#     user_id: int, item_id: str, q: str | None = None, short: bool = False
#     ):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item

# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

# #2.requests body

# from pydantic import BaseModel

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# app = FastAPI()

# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.model_dump()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax":price_with_tax})
#     return item_dict

# @app.put("/items/{item_id}")
# async def update_item(item_id: int,item: Item, q: str | None = None):
#     result = {"item_id":item_id, **item.model_dump()}
#     if q:
#         result.update({"q":q})
#     return result

#3.query parameter and str revise

# from fastapi import Query
# from typing import Annotated

# app = FastAPI()

# # @app.get("/items/")
# # async def read_items(
# #     q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
# #     ] = None,
# #     ):
# #     results = {"items": [{"item_id": "Foo"},{"item_id": "Bar"}]}
# #     if q:
# #         results.update({"q": q})
# #     return results

# # @app.get("/items/")
# # async def read_items(q: Annotated[list[str] | None, Query()] = ["foo", "bar"]):
# #     query_item = {"q": q}
# #     return query_item

# # @app.get("/items/")
# # async def read_items(
# #     q: Annotated[str | None, Query(alias="item-query",
# #                                 title="Query string",
# #                                 description="Query string for the items to search in the database that have a good match",
# #                                 min_length=3,
# #                                 deprecated=True,
# #                             ),
# #                         ] = None,
# #     ):
# #     results = {"items": [{"item_id": "Foo"},{"item_id": "Bar"}]}
# #     if q:
# #         results.update({"q": q})
# #     return results

# @app.get("/items/")
# async def read_items(hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None
# ):
#     if hidden_query:
#         return {"hidden_query": hidden_query}
#     else:
#         return {"hidden_query": "Not found"}

# 4.path parameter and value revaise

# from fastapi import Path, Query
# from typing import Annotated

# app = FastAPI()

# @app.get("/items/{item_id}")
# async def read_items(
#     item_id: Annotated[int, Path(title="The ID of the item to get",ge=1, le=1000)],
#     size: Annotated[float, Query(gt=0,lt=10.5)],
#     q: Annotated[str | None, Query(alias="item-query",deprecated=True)] = None
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q":q})
#     if size:
#         results.update({"size": size})
#     return results

# 5.query parameter model

# from typing import Annotated, Literal

# from fastapi import FastAPI, Query
# from pydantic import BaseModel, Field

# app = FastAPI()

# class FilterParams(BaseModel):
#     model_config = {"extra": "forbid"}

#     limit: int = Field(100, gt=0, le=100)
#     offset: int = Field(0,ge=0)
#     order_by: Literal["created_at", "updated_at"] = "created_at"
#     tags: list[str] = []

# @app.get("/items/")
# async def read_items(filter_query: Annotated[FilterParams, Query()]):
#     return filter_query

# 5. request body - multi parameters

# from typing import Annotated
# from fastapi import Path,Body
# from pydantic import BaseModel

# app = FastAPI()

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# class User(BaseModel):
#     username: str
#     full_name: str | None = None

# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
#     q: str | None = None,
#     item: Item | None = None,
#     user: User | None = None,
#     importance: Annotated[int,Body(gt=0)] = None
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item: 
#         results.update({"item": item})
#     if user:
#         results.update({"user:": user})
#     return results

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
#     results = {"item_id": item_id, "item": item}
#     return results

# 6.request body - Field

# from pydantic import BaseModel, Field
# from fastapi import FastAPI, Body
# from typing import Annotated

# app = FastAPI()

# class Item(BaseModel):
#     name: str
#     description: str | None = Field(
#         default=None, title="The description of the item", max_length=300
#     )
#     price: float = Field(gt=0,description="The price must be greater than zero")
#     tax: float | None = None

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
#     results = {"item_id": item_id, "item": item}
#     return results

# 7.request body - nesting model

# from fastapi import FastAPI
# from pydantic import BaseModel, HttpUrl

# app = FastAPI()

# class Image(BaseModel):
#     url: HttpUrl
#     name: str

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()
#     image: list[Image] | None = None

# class Offer(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     items: list[Item]

# @app.post("/offers/")
# async def create_offer(offer: Offer):
#     return offer

# 8.assert request examples data

# from pydantic import BaseModel, Field
# from fastapi import FastAPI, Body 
# from typing import Annotated

# app = FastAPI()

# # class Item(BaseModel):
# #     name: str 
# #     description: str | None = None
# #     price: float
# #     tax: float | None = None

# #     model_config = {
# #         "json_schema_extra": {
# #             "examples": [
# #                 {
# #                     "name": "Foo",
# #                     "description": "A very nice Item",
# #                     "price": 35.4,
# #                     "tax": 3.2
# #                 }
# #             ]
# #         }
# #     }

# # @app.put("/items/{item_id}")
# # async def update_item(item_id: int, item: Item):
# #     results = {"item_id": item_id, "item": Item}
# #     return results

# class Item(BaseModel):
#     name: str = Field(examples=["Foo"])
#     description: str | None = Field(default=None, examples=["A very nice Item"])
#     price: float = Field(examples=[35.4])
#     tax: float | None = Field(default=None, examples=[3.2])

# # @app.put("/items/{item_id}")
# # async def update_item(item_id: int, item: Item):
# #     results = {"item_id": item_id, "item": Item}
# #     return results

# # @app.put("/items/{item_id}")
# # async def update_item(
# #     item_id: int,
# #     item: Annotated[
# #         Item,
# #         Body(
# #             examples=[
# #                 {
# #                     "name": "Foo",
# #                     "description": "A very nice Item",
# #                     "price": 35.4,
# #                     "tax": 3.2,
# #                 },
# #                 {
# #                 "name": "Bar",
# #                 "price": "35.4",
# #                 },
# #                 {
# #                 "name": "Baz",
# #                 "price": "thirty five point four",
# #                 },
# #             ],
# #         ),
# #     ],
# # ):
# #     results = {"item_id": item_id, "item": item}
# #     return results

# @app.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id: int,
#     item: Annotated[
#         Item,
#         Body(
#             openapi_examples={
#                 "normal": {
#                     "summary": "A normal example",
#                     "description": "A **normal** item works correctly.",
#                     "value": {
#                         "name": "Foo",
#                         "description": "A very nice Item",
#                         "price": 35.4,
#                         "tax": 3.2,
#                     },
#                 },
#                 "converted": {
#                     "summary": "An example with converted data",
#                     "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
#                     "value": {
#                         "name": "Bar",
#                         "price": "35.4",
#                     },
#                 },
#                 "invalid": {
#                     "summary": "Invalid data is rejected with an error",
#                     "value": {
#                         "name": "Baz",
#                         "price": "thirty five point four",
#                     },
#                 },
#             },
#         ),
#     ],
# ):
#     results = {"item_id": item_id, "item": item}
#     return results

# 9.extra data type

# from datetime import datetime, time, timedelta
# from typing import Annotated
# from uuid import UUID
# from fastapi import Body, FastAPI

# app = FastAPI()

# @app.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_datetime: Annotated[datetime, Body()],
#     end_datetime: Annotated[datetime, Body()],
#     process_after: Annotated[timedelta, Body()],
#     repeat_at: Annotated[time | None, Body()] = None
# ):
#     start_process = start_datetime + process_after
#     duration = end_datetime - start_process
#     return {
#         "item_id": item_id,
#         "start_datetime": start_datetime,
#         "end_datetime": end_datetime,
#         "process_after": process_after,
#         "repeat_at": repeat_at,
#         "start_process": start_process,
#         "duration": duration
#     }

# 10.Cookie, Header

# from typing import Annotated
# from fastapi import FastAPI, Cookie, Header

# app = FastAPI()

# # @app.get("/items/")
# # async def read_items(ads_id: Annotated[str | None,  Cookie()] = None):
# #     return {"ads_id": ads_id}

# # @app.get("/items/")
# # async def read_items(user_agent: Annotated[str | None, Header()] = None):
# #     return {"User-Agent": user_agent}

# @app.get("/items/")
# async def read_item(x_token: Annotated[list[str] | None, Header()] = None):
#     return {"X-Token values": x_token}

# 11.Cookie parameter model(被浏览器拦截了)

# from typing import Annotated
# from fastapi import FastAPI, Cookie
# from pydantic import BaseModel

# app = FastAPI()

# class Cookies(BaseModel):
#     model_config = {"extra": "forbid"}
#     session_id: str
#     fatebook_tracker: str | None = None
#     googall_tracker: str | None = None

# @app.get("/items/")
# async def read_items(cookies: Annotated[Cookies,Cookie()]):
#     return cookies

# 12.Header parameter model

# from typing import Annotated
# from fastapi import FastAPI, Header
# from pydantic import BaseModel

# app = FastAPI()

# class CommonHeaders(BaseModel):
#     model_config = {"extra": "forbid"}

#     host: str
#     save_data: bool
#     if_modified_since: str | None = None
#     traceparent: str | None = None
#     x_tag: list[str] = []

# @app.get("/items/")
# async def read_items(headers: Annotated[CommonHeaders, Header(convert_underscores=False)]):
#     return headers

#13.response model - return type

# from typing import Any
# from fastapi import FastAPI
# from pydantic import BaseModel, EmailStr

# app = FastAPI()

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: list[str] = []

# @app.post("/items/",response_model=Item)
# async def create_item(item: Item) -> Any:
#     return item

# @app.get("/items/", response_model=list[Item])
# async def read_items() -> Any:
#     return [
#         {"name":"Portal Gun", "price":42.0},
#         {"name":"Plumbus", "price":32.0},
#     ]

# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None

# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None
    

# @app.post("/user/", response_model=UserOut)
# async def create_user(user: UserIn) -> Any:
#     return user

# class BaseUser(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None

# class UserIn(BaseUser):
#     password: str

# @app.post("/user/")
# async def create_user(user: UserIn) -> BaseUser:
#     return user

# from fastapi import Response
# from fastapi.responses import JSONResponse, RedirectResponse

# @app.get("/portal", response_model=None)
# async def get_portal(teleport: bool = False) -> Response:
#     if teleport:
#         return RedirectResponse(url="https://www.bilibili.com/video/BV154426xEha/?trackid=web_pegasus_0.router-web-pegasus-2479516-gfll4.1791539976346.202&spm_id_from=333.1007.tianma.1-1-1.click&vd_source=78271ca2b9e4d844b1099a09d685ed6c")
#     return JSONResponse(content={"message": "Here's your interdimensional portal."})

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float = 10.5
#     tags: list[str] = []

# items = {
#      "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }    

# @app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
# async def read_item(item_id: str):
#     return items[item_id]

#14. multiple model

# from fastapi import FastAPI
# from pydantic import BaseModel, EmailStr

# app = FastAPI()

# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None

# class UserIn(UserBase):
#     password: str

# class UserOut(UserBase):
#     pass

# class UserInDB(UserBase):
#     hashed_password: str

# def fake_password_hasher(raw_password: str):
#     return "supersecret" + raw_password

# def fake_save_user(user_in: UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.model_dump(),hashed_password=hashed_password)
#     print("User saved! ..not really")
#     return user_in_db

# @app.post("/user/",response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved

# class BaseItem(BaseModel):
#     description: str
#     type: str

# class CarItem(BaseItem):
#     type: str = "car"

# class PlaneItem(BaseItem):
#     type: str = "plane"
#     size: int

# items = {
#     "item1": {"description": "All my friends drive a low rider", "type": "car"},
#     "item2": {
#         "description": "Music is my aeroplane, it's my aeroplane",
#         "type": "plane",
#         "size": 5,
#     },
# }

# @app.get("/items/{item_id}", response_model=PlaneItem | CarItem)
# async def read_item(item_id: str):
#     return items[item_id]

# class Item(BaseModel):
#     name: str
#     description: str

# items = [
#     {"name": "Foo", "description": "There comes my hero"},
#     {"name": "Red", "description": "It's my aeroplane"},
# ]

# @app.get("/items/", response_model=list[Item])
# async def read_items():
#     return items

#15. response status_code

# from fastapi import FastAPI, status

# app = FastAPI()

# @app.post("/items/", status_code=status.HTTP_201_CREATED)
# async def create_item(name: str):
#     return {"name": name}

# 16.Form data

# from typing import Annotated
# from fastapi import FastAPI, Form

# app = FastAPI()

# @app.post("/login/")
# async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
#     return {"username": username}

# 17.Form model
# from typing import Annotated
# from fastapi import FastAPI, Form
# from pydantic import BaseModel

# app = FastAPI()

# class FormData(BaseModel):
#     model_config =  {"extra": "forbid"}
#     username: str
#     password: str

# @app.post("/login/")
# async def login(data: Annotated[FormData, Form()]):
#     return data

# 18.requests File

# from fastapi import FastAPI, File, UploadFile
# from typing import Annotated

# from fastapi.responses import HTMLResponse

# app = FastAPI()

# @app.post("/file/")
# async def create_file(file: Annotated[bytes | None, File(description="A file read as bytes")] = None):
#     if not file:
#         return {"message": "No file sent"}
#     else:
#         return {"file_size": len(file)}

# @app.post("/uploadfile/")
# async def create_upload_file(
#     file: Annotated[UploadFile | None, File(description="A file read as UploadFile")] = None,
#     ):
#     if not file:
#         return {"message": "No upload file sent"}
#     else:
#         return {"filename": file.filename}

# @app.post("/files/")
# async def create_files(files: Annotated[list[bytes], File()]):
#     return {"file_sizes": [len(file) for file in files]}

# @app.post("/uploadfiles/")
# async def create_upload_files(files: list[UploadFile]):
#     return {"filenames": [file.filename for file in files]}

# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)

# 19.requests form and file

# from fastapi import FastAPI, File, Form, UploadFile
# from typing import Annotated

# app = FastAPI()

# @app.post("/files/")
# async def create_file(
#     file: Annotated[bytes, File()],
#     fileb: Annotated[UploadFile, File()],
#     token: Annotated[str, Form()],
# ):
#     return {
#         "file_size": len(file),
#         "token": token,
#         "fileb_conten_type": fileb.content_type,
#     }

# 20.handing errors

# from fastapi import FastAPI, HTTPException, Request
# from fastapi.responses import JSONResponse, PlainTextResponse
# from fastapi.exceptions import RequestValidationError
# from starlette.exceptions import HTTPException as StarletteHTTPException
# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel
# from fastapi.exception_handlers import (
#     http_exception_handler,
#     request_validation_exception_handler,
# )

# app = FastAPI()

# items = {"foo": "The Foo wrestlers."}

# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(
#             status_code=404, 
#             detail="Item not found",
#             headers={"X-ERROR": "There goes my error"}
#             )
#     return {"item": items[item_id]}

# class UnicornException(Exception):
#     def __init__(self, name: str):
#         self.name = name

# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
#     )

# @app.get("/unicorns/{name}")
# async def read_unicorn(name: str):
#     if name == "yolo":
#         raise UnicornException(name=name)
#     return {"unicorn_name": name}

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc: RequestValidationError):
#     message = "Validation errors:"
#     for error in exc.errors():
#         message += f"\nField: {error['loc']}, Error: {error['msg']}"
#     return PlainTextResponse(message, status_code=400)


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
#     return {"item_id": item_id}

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=422,
#         content=jsonable_encoder({"detail": exc.errors(), "body":exc.body}),
#     )

# class Item(BaseModel):
#     title: str
#     size: int

# @app.post("/items/")
# async def create_item(item: Item):
#     return item

# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     print(f"OMG! An HTTP error!: {repr(exc)}")
#     return await http_exception_handler(request, exc)

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     print(f"OMG! The client sent invalid data!: {exc}")
#     return await request_validation_exception_handler(request, exc)

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
#     return {"item_id": item_id}

# 21. path operation config

# from fastapi import status, FastAPI
# from pydantic import BaseModel
# from enum import Enum

# app = FastAPI()

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()

# class Tags(Enum):
#     items = "items"
#     user = "users"

# @app.post("/items/", tags=["Tags.items"])
# async def create_item(item: Item) -> Item:
#     return item

# @app.get("/items/", tags=["Tags.items"])
# async def read_items():
#     return [{"name": "foo", "price": 42}]

# @app.get("/users/", tags=["Tags.users"])
# async def read_users():
#     return [{"username": "johndoe"}]

# @app.post("/items/", 
#           summary="Create an item",
#           description="Create an item with all the information, name, description, price, tax and a set of unique tags",
# )
# async def create_item(item: Item) -> Item:
#     return item

# @app.post("/items/", 
#           summary="Create an item",
#           response_description="The created item",
#           )
# async def create_item(item: Item) -> Item:
#     """
#     这是一个文档字符串
#     - Create an item with all the information:

#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax**: if the item doesn't have tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
#     return item

# @app.get("/elements/", deprecated=True)
# async def read_elements():
#     return [{"item_id": "foo"}]

# 22. json compatible encoder

# from datetime import datetime, timezone
# from fastapi import FastAPI
# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel

# fake_db = {}

# class Item(BaseModel):
#     title: str
#     timestamp: datetime
#     description: str | None = None

# app = FastAPI()

# @app.put("/items/{id}")
# def update_item(id: str, item: Item):
#     if item.timestamp.tzinfo is None:
#         item.timestamp = item.timestamp.replace(tzinfo=timezone.utc)
#     else:
#         item.timestamp = item.timestamp.astimezone(timezone.utc)
#     json_compatible_item_data = jsonable_encoder(item)
#     fake_db[id] = json_compatible_item_data

# 23. requests body - update data 

# from fastapi import FastAPI
# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel

# app = FastAPI()

# class Item(BaseModel):
#     name: str | None = None
#     description: str | None = None
#     price: float | None = None
#     tax: float = 10.5
#     tags: list[str] = []

# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }

# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items[item_id]

# # @app.put("/items/{item_id}", response_model=Item)
# # async def update_item(item_id: str, item: Item):
# #     update_item_encoded = jsonable_encoder(item)
# #     items[item_id] = update_item_encoded
# #     return update_item_encoded

# @app.patch("/items/{item_id}")
# async def update_item(item_id: str, item: Item) -> Item:
#     stored_item_data = items[item_id]
#     stored_item_model = Item(**stored_item_data)
#     update_data = item.model_dump(exclude_unset=True)
#     update_item = stored_item_model.model_copy(update=update_data)
#     items[item_id] = jsonable_encoder(update_item)
#     return update_item

# 24.dependencies

# from typing import Annotated
# from fastapi import Depends, FastAPI

# app = FastAPI()

# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
#     return {"q": q, "skip": skip, "limit": limit}

# @app.get("/items/")
# async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons

# @app.get("/users/")
# async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons

# 25.classes as dependencies

# from fastapi import Depends, FastAPI
# from typing import Annotated

# app = FastAPI()

# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# class CommonqueryParams:
#     def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
#         self.q = q 
#         self.skip = skip
#         self.limit = limit

# @app.get("/items/")
# async def read_items(commons: Annotated[CommonqueryParams, Depends(CommonqueryParams)]):
#     response = {}
#     if commons.q:
#         response.update({"q": commons.q})
#     items = fake_items_db[commons.skip : commons.skip + commons.limit]
#     response.update({"items": items})
#     return response

# 26. sub dependencies

# from typing import Annotated
# from fastapi import Cookie, Depends, FastAPI

# app = FastAPI()

# def query_extractor(q: str | None = None):
#     return q 

# def query_or_cookie_extractor(
#         q: Annotated[str, Depends(query_extractor)],
#         last_query: Annotated[str | None, Cookie()] = None,
# ):
#     if not q:
#         return last_query
#     return q

# @app.get("/items/")
# async def read_query(
#     query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
# ):
#     return {"q_or_cookie": query_or_default}

# 27.dependencies in path operation decorators
# 28.global dependencies

# from typing import Annotated
# from fastapi import Depends, FastAPI, Header, HTTPException

# async def verify_token(x_token: Annotated[str, Header()]):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400,detail="X-Token header invalid")

# async def verify_key(x_key: Annotated[str, Header()]):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key

# app = FastAPI(dependencies=[Depends(verify_key), Depends(verify_token)])

# @app.get("/items")
# async def read_item():
#     return [{"item": "Foo"}, {"item": "Bar"}]

# @app.get("/users/")
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]

# 29. dependencies with yield
# insure one dependencies use one yield

# from typing import Annotated
# from fastapi import Depends, FastAPI, HTTPException

# app = FastAPI()

# data = {
#         "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
#     "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
# }

# class OwnerError(Exception):
#     pass

# def get_username():
#     try:
#         yield "Rick"
#     except OwnerError as e:
#         raise HTTPException(status_code=400, detail=f"Owner error: {e}")

# @app.get("/items/{item_id}")
# def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
#     if item_id not in data:
#         raise HTTPException(status_code=404, detail="Item not found")
#     item = data[item_id]
#     if item["owner"] != username:
#         raise OwnerError(username)
#     return item

# def get_username():
#     try: 
#         yield "Rick"
#     finally:
#         print("Cleanup up before response is sent")

# @app.get("/users/me")
# def get_user_me(username: Annotated[str, Depends(get_username, scope="function")]):
#     return username

# 30.first-steps security

# from typing import Annotated

# from fastapi import Depends, FastAPI
# from fastapi.security import OAuth2PasswordBearer

# app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

# 31.get current user

# from typing import Annotated
# from fastapi import Depends, FastAPI
# from fastapi.security import OAuth2PasswordBearer
# from pydantic import BaseModel

# app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None

# def fake_decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="john doe"
#     )

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     return user

# @app.get("/users/me")
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user

# 32.simple oauth2

# from typing import Annotated
# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }

# app = FastAPI()

# def fake_hash_password(password: str):
#     return "fakehashed" + password

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None

# class UserInDB(User):
#     hashed_password: str

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)

# def fake_decode_token(token):
#     user = get_user(fake_users_db)
#     return user

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user

# async def get_current_active_user(
#         current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# @app.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": user.username, "token_type": "bearer"}


# @app.get("/users/me")
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user

# 33.oauth2 jwt , json web tokens

# from datetime import datetime, timedelta, timezone
# from typing import Annotated

# import jwt
# from fastapi import Depends, FastAPI, HTTPException, status 
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError
# from pwdlib import PasswordHash
# from pydantic import BaseModel

# SECRET_KEY = "b395ba54e32be24fae3c2779585febea7761320e314d1af96c5d1c2d6c300b9c"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
#         "disabled": False,
#     }
# }

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: str | None = None

# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None

# class UserInDB(User):
#     hashed_password: str

# password_hash = PasswordHash.recommended()

# DUMMY_HASH = password_hash.hash("dummypassword")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# app = FastAPI()

# def verify_password(plain_password, hashed_password):
#     return password_hash.verify(plain_password,hashed_password)

# def get_password_hash(password):
#     return password_hash.hash(password)

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)

# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         verify_password(password, DUMMY_HASH)
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = get_user(fake_users_db,username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

# async def get_current_active_user(
#         current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# @app.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token,token_type="bearer")

# @app.get("/users/me/")
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ) -> User:
#     return current_user

# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return [{"item-id": "Foo", "owner": current_user.username}]

# 34.middleware

# import time
# from fastapi import FastAPI, Request

# app = FastAPI()

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.perf_counter()
#     response = await call_next(request)
#     process_time = time.perf_counter() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

# 35. CORS

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# async def main():
#     return {"message": "Hellow World"}

# 36. sql databases

# from typing import Annotated
# from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Field, Session, SQLModel, create_engine, select
# from contextlib import asynccontextmanager

# # class Hero(SQLModel, table=True):
# #     id: int | None = Field(default=None, primary_key=True)
# #     name: str = Field(index=True)
# #     age: int | None = Field(default=None, index=True)
# #     secret_name: str

# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

# connect_args = {"check_same_thread":False}
# engine = create_engine(sqlite_url, connect_args=connect_args)

# def get_session():
#     with Session(engine) as session:
#         yield session

# SessionDep = Annotated[Session, Depends(get_session)]

# app = FastAPI()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     create_db_and_tables()

# # @app.post("/heroes/")
# # def create_hero(hero: Hero, session: SessionDep) -> Hero:
# #     session.add(hero)
# #     session.commit()
# #     session.refresh(hero)
# #     return hero

# # @app.get("/heroes")
# # def read_heroes(
# #     session: SessionDep,
# #     offset: int = 0,
# #     limit: Annotated[int, Query(le=100)] = 100,
# # ) -> list[Hero]:
# #     heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
# #     return heroes

# # @app.get("/heroes/{hero_id}")
# # def read_hero(hero_id: int, session: SessionDep) -> Hero:
# #     hero = session.get(Hero, hero_id)
# #     if not hero:
# #         raise HTTPException(status_code=404, detail="Hero not found")
# #     return hero

# # @app.delete("/heroes/{hero_id}")
# # def delete_hero(hero_id: int, session: SessionDep):
# #     hero = session.get(Hero, hero_id)
# #     if not hero:
# #         raise HTTPException(status_code=404, detail="Hero not found")
# #     session.delete(hero)
# #     session.commit()
# #     return {"ok": True}

# class HeroBase(SQLModel):
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)

# class Hero(HeroBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     secret_name: str

# class HeroPublic(HeroBase):
#     id: int

# class HeroCreate(HeroBase):
#     secret_name: str

# class HeroUpdate(HeroBase):
#     name: str | None = None
#     age: int | None = None
#     secret_name: str | None = None

# @app.post("/heroes/", response_model=HeroPublic)
# def create_hero(hero: HeroCreate, session: SessionDep):
#     db_hero = Hero.model_validate(hero)
#     session.add(db_hero)
#     session.commit()
#     session.refresh(db_hero)
#     return db_hero

# @app.get("/heroes/", response_model=list[HeroPublic])
# def read_heroes(
#     session: SessionDep,
#     offfset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ):
#     heroes = session.exec(select(Hero.offset(offfset).limit(limit))).all()
#     return heroes

# @app.get("/heroes/{hero_id}", response_model=HeroPublic)
# def read_hero(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     return hero

# @app.patch("/heroes/{hero_id}", response_model=HeroPublic)
# def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
#     hero_db = session.get(Hero, hero_id)
#     if not hero_db:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     hero_data = hero.model_dump(exclude_unset=True)
#     hero_db.sqlmodel_update(hero_data)
#     session.add(hero_db)
#     session.commit()
#     session.refresh(hero_db)
#     return hero_db

# @app.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int, session: SessionDep):
#     hero = session.get(Hero,hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}

# 37.bigger applications

# 38.stream json line

# from collections.abc import AsyncIterable, Iterable
# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class Item(BaseModel):
#     name: str
#     description: str | None

# items = [
#     Item(name="Plumbus", description="A multi-purpose household device."),
#     Item(name="Portal Gun", description="A portal opening device."),
#     Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
# ]

# @app.get("/items/stream")
# async def stream_items() -> AsyncIterable[Item]:
#     for item in items:
#         yield item

# @app.get("/items/stream-no-async")
# def stream_items_no_async() -> Iterable[Item]:
#     for item in items:
#         yield item

# 39.server sent events

# from collections.abc import AsyncIterable, Iterable
# from fastapi import FastAPI, Header
# from fastapi.sse import EventSourceResponse, ServerSentEvent
# from pydantic import BaseModel
# from typing import Annotated

# app = FastAPI()

# class Item(BaseModel):
#     name: str
#     description: str | None

# items = [
#     Item(name="Plumbus", description="A multi-purpose household device."),
#     Item(name="Portal Gun", description="A portal opening device."),
#     Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
# ]

# @app.get("/items/stream", response_class=EventSourceResponse)
# async def sse_items() -> AsyncIterable[Item]:
#     for item in items:
#         yield item

# @app.get("/items/stream", response_class=EventSourceResponse)
# def sse_items_no_async() -> Iterable[Item]:
#     for item in items:
#         yield item        

# @app.get("/items/stream", response_class=EventSourceResponse)
# async def sse_items():
#     for item in items:
#         yield item

# class Item(BaseModel):
#     name: str
#     price: float


# items = [
#     Item(name="Plumbus", price=32.99),
#     Item(name="Portal Gun", price=999.99),
#     Item(name="Meeseeks Box", price=49.99),
# ]        

# @app.get("/items/stream", response_class=EventSourceResponse)
# async def sse_items() -> AsyncIterable[ServerSentEvent]:
#     yield ServerSentEvent(comment="stream of item updates")
#     for i, item in enumerate(items):
#         yield ServerSentEvent(data=item, event="item_update,", id=str(i + 1), retry=5000)        

# @app.get("/logs/stream", response_class=EventSourceResponse)
# async def stream_logs() -> AsyncIterable[ServerSentEvent]:
#     logs = [
#         "2025-01-01 INFO  Application started",
#         "2025-01-01 DEBUG Connected to database",
#         "2025-01-01 WARN  High memory usage detected",
#     ]
#     for log_line in logs:
#         yield ServerSentEvent(raw_data=log_line)

# @app.get("/items/stream", response_class=EventSourceResponse)        
# async def stream_items(
#     last_event_id: Annotated[int | None, Header()] = None,
# ) -> AsyncIterable[ServerSentEvent]:
#     start = last_event_id + 1 if last_event_id is not None else 0
#     for i, item in enumerate(items):
#         if i < start:
#             continue
#         yield ServerSentEvent(data=item, id=str(i))

#MCP

# class Prompt(BaseModel):
#     text: str

# @app.post("/chat/stream", response_class=EventSourceResponse)
# async def stream_chat(prompt: Prompt) -> AsyncIterable[ServerSentEvent]:
#     words = prompt.text.split()
#     for word in words:
#         yield ServerSentEvent(data=word, event="token")
#     yield ServerSentEvent(raw_data="[DONE]", event="done")

# 40.background tasks

# from fastapi import BackgroundTasks, FastAPI

# app = FastAPI()

# def write_notification(email: str, message=""):
#     with open("log.txt", mode="w") as email_file:
#         content = f"notification for {email}: {message}"
#         email_file.write(content)

# @app.post("/send-notification/{email}")
# async def send_notification(email: str, background_tasks: BackgroundTasks):
#     background_tasks.add_task(write_notification, email, message="some notification")
#     return {"message": "Notification sent in the background"}        

# 41.metadata and document URL

# from fastapi import FastAPI

# description = """
# ChimichangApp API helps you do awesome stuff. 🚀

# ## Items

# You can **read items**.

# ## Users

# You will be able to:

# * **Create users** (_not implemented_).
# * **Read users** (_not implemented_).
# """

# app = FastAPI(
#     title="ChimichangApp",
#     description=description,
#     summary="Deadpool's favorite app. Nuff said.",
#     version="0.0.1",
#     terms_of_service="http://example.com/terms/",
#     contact={
#         "name": "Deadpoolio the Amazing",
#         "url": "http://x-force.example.com/contact/",
#         "email": "dp@x-force.example.com",
#     },
#     license_info={
#         "name": "Apache 2.0",
#         "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
#         "identifier": "Apache-2.0",
#     },
# )


# @app.get("/items/")
# async def read_items():
#     return [{"name": "Katana"}]

# tags_metadata = [
#     {
#         "name": "users",
#         "description": "Operations with users. The **login** logic is also here.",
#     },
#     {
#         "name": "items",
#         "description": "Manage items. So _fancy_ they have their own docs.",
#         "externalDocs": {
#             "description": "Items external docs",
#             "url": "https://fastapi.tiangolo.com/",
#         },
#     },
# ]

# app = FastAPI(openapi_tags=tags_metadata)


# @app.get("/users/", tags=["users"])
# async def get_users():
#     return [{"name": "Harry"}, {"name": "Ron"}]


# @app.get("/items/", tags=["items"])
# async def get_items():
#     return [{"name": "wand"}, {"name": "flying broom"}]

# app = FastAPI(openapi_url=None)


# @app.get("/items/")
# async def read_items():
#     return [{"name": "Foo"}]

# 42.frontend
# 43.static file 

# 44.testing

# from fastapi.testclient import TestClient

# from .main import app

# client = TestClient(app)


# def test_read_item():
#     response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
#     assert response.status_code == 200
#     assert response.json() == {
#         "id": "foo",
#         "title": "Foo",
#         "description": "There goes my hero",
#     }


# def test_read_item_bad_token():
#     response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid X-Token header"}


# def test_read_nonexistent_item():
#     response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Item not found"}


# def test_create_item():
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "coneofsilence"},
#         json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "id": "foobar",
#         "title": "Foo Bar",
#         "description": "The Foo Barters",
#     }


# def test_create_item_bad_token():
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "hailhydra"},
#         json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid X-Token header"}


# def test_create_existing_item():
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "coneofsilence"},
#         json={
#             "id": "foo",
#             "title": "The Foo ID Stealers",
#             "description": "There goes my stealer",
#         },
#     )
#     assert response.status_code == 409
#     assert response.json() == {"detail": "Item already exists"}

# 45.debugging

# import uvicorn
# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def root():
#     a = "a"
#     b = "b" + a
#     return {"hello world": b}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)