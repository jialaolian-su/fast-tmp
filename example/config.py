from pydantic import BaseSettings


class __Settings(BaseSettings):
    API_SECRET: str
    ADMIN_SECRET: str
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str
    DB_NAME: str
    DB_PASSWORD: str
    SERVER_URL: str
    DEBUG: bool = False
    PROJECT_CODE: str = "AUDIT"

    class Config:
        env_file = '.env'


settings = __Settings()

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": settings.DB_HOST,
                "port": settings.DB_PORT,
                "user": settings.DB_USER,
                "password": settings.DB_PASSWORD,
                "database": settings.DB_NAME,
                "echo": os.getenv("DB_ECHO") == "True",
                "maxsize": 10,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["example.models", "aerich.models", "fast_tmp.models"],
            "default_connection": "default",
        },
    },
}

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

REDIS = {
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "password": REDIS_PASSWORD,
    "db": 2,
    "encoding": "utf-8",
}

REARQ = {
    "redis_host": REDIS_HOST,
    "redis_port": REDIS_PORT,
    "redis_password": REDIS_PASSWORD,
    "redis_db": 1,
}

# logging
LOGGER = logging.getLogger("example")
if DEBUG:
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
LOGGER.addHandler(sh)

SERVER_HOST = os.getenv("SERVER_HOST")
