from asyncpg import connect
from data import DB_DSN

async def get_conn():
    conn = await connect(dsn=DB_DSN)
    return conn