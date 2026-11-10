from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, Field
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix='MYAPI_')
    
    database_url: PostgresDsn
    debug: bool = False
# dataclass的默认值在类定义时求值一次，所有Settings实例共享一个list，
# default_factory=list每次实例化都调用一个空列表
    cors_origins: list[str] = Field(default_factory=list)


#Settings 对象只会在第一次调用时创建一次
@lru_cache
def get_settings():
    return Settings()

