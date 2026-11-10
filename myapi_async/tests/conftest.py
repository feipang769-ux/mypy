from asgi_lifespan import LifespanManager
from myapi.main import app
from httpx import AsyncClient, ASGITransport
import pytest 

#准备测试环境并注入数据
#@pytest.fixture依赖注入与生命周期管理
@pytest.fixture
async def client():
    #测试开始前
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
                                ) as ac:
            yield ac
            #测试开始后