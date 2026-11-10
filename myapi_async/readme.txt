#建表
 uv run python -m myapi.init_db

# run
uv run .venv\Scripts\python.exe -m uvicorn myapi.main:app --reload

#跑测试
 uv run pytest -v


