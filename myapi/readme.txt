#建数据库与表
 uv run python -m myapi.init_db

# run
uv run .venv\Scripts\python.exe -m uvicorn myapi.main:app --reload

#跑测试，目前未配置
 uv run pytest -v



