from envparse import Env

env = Env()

SECRET_KEY = env.str(
    "SECRET_KEY",
    default="09d25e094faa6ca2556c8985sa454x57as5wda7099f6f0f4caa6cf63b88e8d3e7"
)

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:1234@localhost:5433/postgres"
)

TEST_DB_URL = env.str(
    "TEST_DB_URL",
    default="postgresql+asyncpg://postgres:1234@localhost:5433/test_db"
)


