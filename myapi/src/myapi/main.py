from fastapi import FastAPI
from .config import get_settings
from myapi.routers import users
from fastapi.openapi.docs import get_swagger_ui_html





#工厂模式允许测试代码在需要时创建新的 app 实例
def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title='schedule',
        debug=settings.debug,
        docs_url=None,
    )
    app.include_router(users.router)

    # 自定义 docs 路由，替换为国内 CDN
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            # 使用国内的 BootCDN 加速
            swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.9.0/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.9.0/swagger-ui.css",
        )
    return app

#函数赋值给变量，让Uvicorn找到
app = create_app()