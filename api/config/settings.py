from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:1234@localhost:5432/postgres"
)

TEST_DB_URL = env.str(
    "TEST_DB_URL",
    default="postgresql+asyncpg://postgres:1234@localhost:5432/test_db"
)


