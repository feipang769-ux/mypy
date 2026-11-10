import pytest
from httpx import AsyncClient
import uuid

#放到事件循环执行
@pytest.mark.anyio      #使用相同名字参数使fixture找到
async def test_create(client: AsyncClient) -> None:
    unique_title = str(uuid.uuid4())

    create_test = await client.post(
        "/Task",
        json={"title": unique_title, "description": "测试描述", "priority": "medium"}
    )

    assert create_test.status_code == 201
    data = create_test.json()
    assert data["title"] == unique_title
    assert data["status"] == "pending"

    ...
