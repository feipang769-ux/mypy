# # python -m venv .venv

# uv add alembic --dev 

# uv run alembic init -t async migrations

# migrations/env.py配置:
# 1. 
# from myapi.models import Base
# target_metadata = base.metadata

# 2. 配置异步URL或覆盖(不把数据库 URL 明文写进 alembic.ini)
# from myapi.config import get_settings
# config.set_main_option("sqlalchemy.url",str(get_settings().database.url))


#  校订                                           备注
# uv run alembic revision --autogenerate -m "create users"

# #升级，迁移到数据库
# uv run alembic upgrade head

# # 确认当前数据库版本
# uv run alembic current

#回滚，把数据库回退
# uv run alembic downgrade -1


